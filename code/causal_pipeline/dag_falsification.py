import networkx as nx

from dowhy.gcm.falsify import (
    FalsifyConst,
    falsify_graph,
)
from dowhy.gcm.util.general import set_random_seed

set_random_seed(42)

def falsify(graph, data, n_permutations, alpha):
    zero_degree_nodes = [n for n in list(graph.nodes()) if graph.degree(n) == 0]

    if zero_degree_nodes:
        graph.remove_nodes_from(zero_degree_nodes)

    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("graphraph must be a DAgraph after pruning!")

    missing_nodes = [node for node in graph.nodes if node not in data.columns]
    if missing_nodes:
        raise ValueError(f"Missing columns: {missing_nodes}")

    data = data[list(graph.nodes)].copy().astype("float64")

    result = falsify_graph(
        graph,
        data,
        n_permutations=n_permutations,
        significance_level=alpha,
        suggestions=True
    )

    return result