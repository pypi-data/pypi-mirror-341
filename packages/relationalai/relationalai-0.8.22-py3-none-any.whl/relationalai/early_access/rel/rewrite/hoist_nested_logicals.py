from __future__ import annotations

from relationalai.early_access.metamodel import ir, factory as f
from relationalai.early_access.metamodel.compiler import Pass

class HoistNestedLogicals(Pass):
    """
    If a Logical has only nested Logicals and is child of a Logical, its children can be hoisted.

    From:
        Logical
            Logical
                Logical
                    x
                Logical
                    y
    To:
        Logical
            Logical
                x
            Logical
                y
    """
    def rewrite(self, model: ir.Model, cache) -> ir.Model:
        if isinstance(model.root, ir.Logical):
            new_body = []
            changes = False
            for child in model.root.body:
                if isinstance(child, ir.Logical):
                    if all(isinstance(c, ir.Logical) for c in child.body):
                        changes = True
                        new_body.extend(child.body)
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
