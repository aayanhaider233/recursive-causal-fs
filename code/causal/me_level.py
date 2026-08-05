import discovery_utils as disc
import me_gene_intermediate as mgi

from joblib import dump

EXOGENOUS_VARS = ["age", "sex"]
SINK_VARS = ["disease"]
N_BOOTSTRAPS = 200

TARGET = "disease"
EDGE_FREQ_THRESHOLD = 0.8

KME_SCORING_ALPHA = 0.5
TOP_N_SCORED_GENES = 200

QUANTILE = 0.9

def me_level_discovery(data):

    edge_freq, edge_avg_weights, variables = disc.bootstrap_discovery(
        data=data,
        n_bootstraps=N_BOOTSTRAPS,
        exogenous_vars=EXOGENOUS_VARS,
        sink_vars=SINK_VARS
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

    edge_df = disc.ace_estimation(
        data=data,
        G=graph
    )

    return graph, edge_df

def me_level_post_processing(
    edge_df, 
    gene_module_assignments, 
    gene_go_map, 
    gene_module_membership, 
    gene_methylation_data, 
    metadata
):

    top_genes = mgi.filter_top_genes_by_me(
        edges=edge_df,
        gene_modules=gene_module_assignments,
        edge_frequency_threshold=EDGE_FREQ_THRESHOLD,
        target=TARGET
    )

    go_relevant_genes = mgi.filter_genes_by_go_terms(
        genes=top_genes,
        gene_go_map=gene_go_map
    )

    me_edges = edge_df[
        (edge_df["target"] == "disease") &
        (edge_df["source"].str.startswith("ME"))
    ].copy()

    _, top_scored_genes = mgi.filter_genes_by_kme_scored(
        genes=go_relevant_genes,
        gene_module_membership=gene_module_membership,
        me_edges=me_edges,
        alpha=KME_SCORING_ALPHA,
        n_total=TOP_N_SCORED_GENES
    )

    pruned_genes = mgi.prune_genes_by_correlation(
        gene_methylation_data=gene_methylation_data,
        top_genes=top_scored_genes,
        quantile=QUANTILE
    )

    final_gene_df = mgi.subset_data_by_gene(
        gene_methylation_data=gene_methylation_data,
        traits=metadata,
        genes=pruned_genes
    )

    return final_gene_df


def run_me_level_stage(
        me_matrix, 
        gene_module_assignments, 
        gene_go_map, 
        gene_module_membership, 
        gene_methylation_data, 
        metadata 
    ): 

    graph, edge_df = me_level_discovery(data=me_matrix)

    final_gene_df = me_level_post_processing(
        edge_df=edge_df, 
        gene_module_assignments=gene_module_assignments,
        gene_go_map=gene_go_map,
        gene_module_membership=gene_module_membership,
        gene_methylation_data=gene_methylation_data,
        metadata=metadata
    )

    return graph, edge_df, final_gene_df