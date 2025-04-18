"""
Helpers to analyze the metamodel IR in ways that are specific to Rel generation.
"""
from __future__ import annotations

from typing import cast, Tuple
from relationalai.early_access.metamodel import ir, util, visitor, builtins
from relationalai.early_access.metamodel.util import OrderedSet


def is_external(relation: ir.Relation):
   return builtins.external_annotation in relation.annotations

def effective_logicals(tasks: OrderedSet[ir.Task]) -> OrderedSet[ir.Logical]:
    return util.OrderedSet.from_iterable(filter(lambda t: is_effective_logical(t), tasks))

def is_effective_logical(n: ir.Task):
    return isinstance(n, ir.Logical) and len(visitor.collect_by_type(ir.Update, n)) > 0

def nullable_logicals(tasks: OrderedSet[ir.Task]) -> OrderedSet[ir.Logical]:
    return util.OrderedSet.from_iterable(filter(lambda t: is_nullable_logical(t), tasks))

def is_nullable_logical(n: ir.Task):
    return isinstance(n, ir.Logical) and any(isinstance(v, ir.Default) and v.value is None for v in n.hoisted)

def hoisted_vars(hoisted: Tuple[ir.VarOrDefault, ...]) -> list[ir.Var]:
    return [v.var if isinstance(v, ir.Default) else v for v in hoisted]

def vars(args: Tuple[ir.Value, ...]) -> list[ir.Var]:
    return cast(list[ir.Var], list(filter(lambda v: isinstance(v, ir.Var), args)))

def outer_join_prefix(nullable_logicals: OrderedSet[ir.Logical], groups: dict[str, OrderedSet[ir.Task]]) -> list[ir.Var]:
    """ Check if it is possible to use an outer join on the logical that has these nullable
    logicals and these groups of tasks. This function returns a list of prefix variables
    for the outer join.

    There are several requirements to use the outer join. If some is not met, the
    function returns an empty list
    """
    # all nested logicals must be nullable
    if len(nullable_logicals) != len(groups["logicals"]):
        return []

    # at this point, all nested logicals are nullable, but they should only have a single hoisted variable
    for logical in nullable_logicals:
        if len(logical.hoisted) != 1:
            return []

    # outer joins only work on outputs
    if "output" not in groups or len(groups["output"]) != 1:
        return []
    output = cast(ir.Output, groups["output"].some())

    # the output variables must be a prefix + nullable variables; the length of the
    # prefix is the number of extra aliases in the output
    prefix_length = len(output.aliases) - len(nullable_logicals)
    if prefix_length < 1:
        return []

    # get the hoisted vars from the nullable logicals, a bit messy
    logical_hoisted_vars = OrderedSet.from_iterable([cast(ir.Default, logical.hoisted[0]).var for logical in nullable_logicals])
    prefix=[]
    i = 0
    for _, var in output.aliases:
        if i < prefix_length:
            # the first prefix_length aliases are the prefix variables
            prefix.append(var)
            i += 1
        else:
            # the remaining output variables should be exposed one by one by the logicals
            if var not in logical_hoisted_vars:
                return []
            logical_hoisted_vars.remove(var)
    # basically an assertion as this should be empty if we got here
    if logical_hoisted_vars:
        return []

    # all nullable logicals must join with all the prefix variables
    for logical in nullable_logicals:
        vars = visitor.collect_implicit_vars(logical)
        for prefix_var in prefix:
            if prefix_var not in vars:
                return []

    return prefix
