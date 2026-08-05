import discovery_utils as disc
import dag_falsification as dfal
from itertools import product

EXOGENOUS_VARS = ["age", "sex"]
SINK_VARS = ["disease"]
N_BOOTSTRAPS = 800

TARGET = "disease"
FALSIFICATION_PERMUTATIONS = 1000
FALSIFICATION_ALPHA = 0.05

REFUTATION_METHODS = {
    name: disc.REFUTATION_METHODS[name]
    for name in ["bootstrap", "placebo", "rcc"]
}

def dmr_level_discovery(data):
    
    variables = data.columns.tolist()
    dmrs = [dmr for dmr in variables if "DMR" in dmr]
    forbidden_edges = list(product(dmrs, dmrs))

    edge_freq, edge_avg_weights, variables = disc.bootstrap_discovery(
        data=data,
        n_bootstraps=N_BOOTSTRAPS,
        exogenous_vars=EXOGENOUS_VARS,
        sink_vars=SINK_VARS,
        forbidden_edges=forbidden_edges
    )

    candidate_df = disc.retain_edges_by_causal_score(
        edge_freq=edge_freq,
        edge_avg_weights=edge_avg_weights,
        variables=variables
    )

    robust_edges = disc.resolve_directional_ambiguity(
        candidate_df=candidate_df,
        edge_freq=edge_freq,
        edge_avg_weights=edge_avg_weights,
        variables=variables
    )

    graph = disc.construct_graph_from_edges(
        variables=variables,
        robust_edges=robust_edges
    )

    return graph

def falsify_dag(graph, dmr_matrix):

    results = dfal.falsify(
        graph=graph,
        data=dmr_matrix,
        n_permutations=FALSIFICATION_PERMUTATIONS,
        alpha=FALSIFICATION_ALPHA
    )

    return results 

def modify_dag(graph, falsification_results):
    """
    Placeholder.

    Inspect the falsification report and manually implement any
    graph modifications suggested by causal minimality or other
    diagnostics before continuing.
    """
    raise NotImplementedError(
        "Modify the DAG according to the falsification results."
    )

def ace_estimation_refutation(graph, dmr_matrix):

    edge_df = disc.ace_estimation(
        data=dmr_matrix,
        G=graph
    )

    edge_df_refuted = disc.apply_refutations(
        ace_df=edge_df,
        refutation_methods=REFUTATION_METHODS
    )

    return edge_df_refuted

def run_dmr_level_stage(dmr_matrix):
    graph = dmr_level_discovery(data=dmr_matrix)
    results = falsify_dag(
        graph=graph,
        dmr_matrix=dmr_matrix
    )
    modified_graph = modify_dag(
        graph=graph,
        falsification_results=results
    )
    edge_df = ace_estimation_refutation(
        graph=modified_graph,
        dmr_matrix=dmr_matrix
    )

    return graph, results, modified_graph, edge_df