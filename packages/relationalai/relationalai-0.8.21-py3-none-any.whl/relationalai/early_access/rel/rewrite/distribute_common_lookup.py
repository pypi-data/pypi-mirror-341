from __future__ import annotations
from typing import cast

from relationalai.early_access.metamodel import ir, factory as f
from relationalai.early_access.metamodel.compiler import Pass, group_tasks
from relationalai.early_access.metamodel.util import OrderedSet
from relationalai.early_access.rel import metamodel_utils

class DistributeCommonLookup(Pass):
    """
    Distribute a common lookup into nested logicals if they are going to be extracted as
    their own "rules" later.

    From:
        Logical
            Logical
                lookup
                Logical
                    x
                Logical
                    y
    To:
        Logical
            Logical
                lookup
                Logical
                    lookup
                    x
                Logical
                    lookup
                    y

    Or (in special cases where the lookup is *not* needed in the original Logical):
        Logical
            Logical
                Logical
                    lookup
                    x
                Logical
                    lookup
                    y
    """

    def rewrite(self, model: ir.Model, cache) -> ir.Model:
        if isinstance(model.root, ir.Logical):
            new_body = []
            changes = False
            for child in model.root.body:
                if isinstance(child, ir.Logical):
                    groups = group_tasks(child.body, {
                        "lookups": ir.Lookup,
                        "logicals": ir.Logical,
                        "aggregates": ir.Aggregate,
                        "output": ir.Output,
                    })
                    # can only distribute a single lookup, when there are no aggs, and no other tasks
                    # (but maybe an output).
                    if len(groups["lookups"]) == 1 and not groups["aggregates"] and not groups["other"]:
                        # distribution is and only needed if
                        # 1. there are logicals with effects, or
                        effective_logicals = metamodel_utils.effective_logicals(groups["logicals"])
                        # 2. there are logicals with null defaults.
                        nullable_logicals = metamodel_utils.nullable_logicals(groups["logicals"])
                        if effective_logicals or nullable_logicals:
                            changes = True
                            new_body.append(self._rewrite(child, effective_logicals, nullable_logicals, groups))
                        else:
                            new_body.append(child)
                    else:
                        new_body.append(child)
            if changes:
                return ir.Model(
                    model.engines,
                    model.relations,
                    model.types,
                    f.logical(new_body)
                )
        return model

    def _rewrite(self, node: ir.Logical, effective_logicals: OrderedSet[ir.Logical], nullable_logicals: OrderedSet[ir.Logical], groups: dict[str, OrderedSet[ir.Task]]):
        """ Rewrite this node such that its lookup child is pushed into its nested logicals. """

        # we know there's a single lookup to be distributed
        lookup = groups["lookups"].some()

        # check if we can use an outer join
        prefix = metamodel_utils.outer_join_prefix(nullable_logicals, groups)

        new_body = []
        if prefix:
            # outer join is possible, so we distribute the lookup, adjust hoisted vars to
            # contain the prefixes and remove the original lookup
            for task in groups["logicals"]:
                logical = cast(ir.Logical, task)
                # adds the prefix to hoisted
                new_hoisted = cast(list[ir.VarOrDefault], prefix.copy())
                new_hoisted.extend(logical.hoisted)

                # create a new logical that adds the lookup
                new_body.append(
                    ir.Logical(
                        logical.engine,
                        tuple(new_hoisted),
                        tuple([lookup] + list(logical.body))
                    )
                )
        else:
            # outer join is not possible, so we distribute the lookup across the nested logicals

            # if all logicals are effective, they will all be extracted as their own rules,
            # so we don't need the original lookup; otherwise keep it
            if len(effective_logicals) != len(groups["logicals"]):
                new_body.append(lookup)

            # distribute the lookup
            for task in groups["logicals"]:
                logical = cast(ir.Logical, task)
                # create a new logical that adds the lookup
                new_body.append(
                    ir.Logical(
                        logical.engine,
                        logical.hoisted,
                        tuple([lookup] + list(logical.body))
                    )
                )
            pass

        # just keep the outputs and other tasks from the original logical
        if "other" in groups:
            new_body.extend(groups["other"])
        if "output" in groups:
            new_body.extend(groups["output"])
        return f.logical(new_body)
