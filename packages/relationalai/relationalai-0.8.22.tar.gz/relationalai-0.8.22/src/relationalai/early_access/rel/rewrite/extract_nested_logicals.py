from __future__ import annotations
from typing import cast

from relationalai.early_access.metamodel import ir, factory as f, util, visitor
from relationalai.early_access.metamodel.compiler import Pass, group_tasks, VarMap, ReplaceVars
from relationalai.early_access.metamodel.util import OrderedSet
from relationalai.early_access.rel import metamodel_utils, builtins as rel_bt

class ExtractNestedLogicals(Pass):
    """
    Extracts nested logicals in the body of a logical as new logicals that derive into a
    temporary relation.

    From:
        Logical
            Logical
                Logical
                    x
                    y
                Logical
                    z
                    w
                ^derive foo
    To:
        Logical
            Logical
                x
                y
                ^derive tmp1
            Logical
                z
                w
                ^derive tmp2
            Logical
                tmp1
                tmp2
                ^derive foo
    """

    def rewrite(self, model: ir.Model, cache) -> ir.Model:
        if isinstance(model.root, ir.Logical):
            new_body = []
            new_relations:list[ir.Relation] = []
            for child in model.root.body:
                if isinstance(child, ir.Logical):
                    groups = group_tasks(child.body, {
                        "logicals": ir.Logical,
                        "output": ir.Output,
                    })
                    # we need to extract all nullable logicals and logicals that have effects
                    effective_logicals = metamodel_utils.effective_logicals(groups["logicals"])
                    nullable_logicals = metamodel_utils.nullable_logicals(groups["logicals"])
                    # TODO: assert no aggregations?
                    if effective_logicals or nullable_logicals:
                        new_logicals, new_relations = self._rewrite(child, effective_logicals, nullable_logicals, groups)
                        new_body.extend(new_logicals)
                        new_relations.extend(new_relations)
                    else:
                        new_body.append(child)

            if new_relations:
                new_relations.extend(model.relations)
                return ir.Model(
                    model.engines,
                    util.FrozenOrderedSet.from_iterable(new_relations),
                    model.types,
                    f.logical(new_body)
                )
        return model

    def _rewrite(self, node: ir.Logical, effective_logicals: OrderedSet[ir.Logical], nullable_logicals: OrderedSet[ir.Logical], groups: dict[str, OrderedSet[ir.Task]]):
        result = []

        # collect vars used by other tasks; they need to be exposed by the extracted
        outer_vars = util.ordered_set()
        for task in node.body:
            if task not in groups["logicals"]:
                outer_vars.update(visitor.collect_vars(task))

        # check if we can use an outer join
        prefix = metamodel_utils.outer_join_prefix(nullable_logicals, groups)

        new_body = []
        new_relations = []
        # just keep the other tasks from the original logical
        if "other" in groups:
            new_body.extend(groups["other"])
        # extract each logical and append a reference to it in the new body
        for logical in effective_logicals:
            extracted, reference, relation = self._extract_nested_logical(cast(ir.Logical, logical), outer_vars, prefix, False)
            result.append(extracted)
            new_body.append(reference)
            new_relations.append(relation)

        for logical in nullable_logicals:
            extracted, reference, relation = self._extract_nested_logical(cast(ir.Logical, logical), outer_vars, prefix, True)
            result.append(extracted)
            new_body.append(reference)
            new_relations.append(relation)

        # keep the outputs last for nicer code
        if "output" in groups:
            new_body.extend(groups["output"])
        result.append(f.logical(new_body))
        return result, new_relations

    def _extract_nested_logical(self,
            logical: ir.Logical,
            outer_vars: OrderedSet[ir.Var],
            prefix: list[ir.Var],
            nullable: bool):
        """ Create a new "extracted" logical from this logical, together with a lookup that
        references the extracted logical. """

        # compute which vars the extracted logical needs to expose; these are the ones that
        # are used both in the extracted logical as well as in the outer vars
        hoisted_vars = [v.var if isinstance(v, ir.Default) else v for v in logical.hoisted]
        exposed_hoisted = util.ordered_set()
        exposed_vars = []
        for v in visitor.collect_implicit_vars(logical):
            if v in outer_vars and v not in hoisted_vars:
                exposed_hoisted.add(v)
                exposed_vars.append(v)
        # ensure the hoisted are last
        exposed_hoisted.update(logical.hoisted)
        exposed_vars.extend(hoisted_vars)

        # the extracted relation has fields for the exposed vars
        relation = f.relation(f"nested_{logical.id}", [f.field(v.name, v.type) for v in exposed_vars])

        # create the extracted logical, making sure we use new vars
        vars = VarMap()
        replacer = ReplaceVars(vars)
        extracted_exposed_vars = vars.get_many(exposed_vars)
        extracted_body = []
        extracted_body.extend(replacer.walk_list(logical.body))

        if prefix:
            # using outer join support; add @no_inline annotation on extracted logicals (defs)
            extracted_body.append(f.derive(relation, extracted_exposed_vars, [f.annotation(rel_bt.no_inline, [])]))
        else:
            extracted_body.append(f.derive(relation, extracted_exposed_vars))

        if nullable and not prefix:
            # TODO: nullable without outer join, inject a check for Missing
            reference = f.logical([f.lookup(relation, exposed_vars)], exposed_hoisted.list)
        else:
            reference = f.logical([f.lookup(relation, exposed_vars)], exposed_hoisted.list)

        return f.logical(extracted_body), reference, relation
