from .. import dsl
from ..std.graphs import unwrap

# --------------------------------------------------
# Ego network
# --------------------------------------------------
def ego_network(graph, node, hops):
    a, b = dsl.create_vars(2)
    dsl.global_ns.graphlib_experimental.ego_network(graph, unwrap(node), hops, a, b)
    la = graph.compute._lookup(a)
    lb = graph.compute._lookup(b)
    return (la, lb)
