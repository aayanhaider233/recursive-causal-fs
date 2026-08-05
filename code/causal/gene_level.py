import discovery_utils as disc
import gene_dmr_intermediate as gdi

EXOGENOUS_VARS = ["age", "sex"]
SINK_VARS = ["disease"]
N_BOOTSTRAPS = 400

TARGET = "disease"

def gene_level_discovery(data):

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

def gene_level_post_processing(edge_df, metadata, dmr_gene_map, dmr_methylation_data):

    parent_genes = gdi.extract_parent_genes(
        edges=edge_df,
        traits=metadata,
        target=TARGET
    )

    dmr_map = gdi.reverse_map_genes_to_dmrs(
        parent_genes=parent_genes,
        dmr_gene_map=dmr_gene_map
    )

    final_dmr_df = gdi.subset_dmr_dataset(
        dmr_methylation_data=dmr_methylation_data,
        dmr_map=dmr_map
    )

    return final_dmr_df

def run_gene_level_stage(
        gene_matrix,
        dmr_gene_map, 
        dmr_methylation_data, 
        metadata 
    ): 

    graph, edge_df = gene_level_discovery(data=gene_matrix)

    final_dmr_df = gene_level_post_processing(
        edge_df=edge_df, 
        metadata=metadata,
        dmr_gene_map=dmr_gene_map,
        dmr_methylation_data=dmr_methylation_data
    )

    return graph, edge_df, final_dmr_df