# --------------------------------------------------
# Imports
# --------------------------------------------------

import me_level as mel
import gene_level as genel
import dmr_level as dmrl
import pandas as pd
from pathlib import Path
import pickle

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
CAUSAL_METHYLATION_INPUT_DIR = DATA / "causal_methylation_inputs"
INTERMEDIATE_DATA_DIR = DATA / "intermediate"
METADATA_DIR = DATA / "metadata"
DMR_METHYLATION_DIR = DATA / "methylation"

ME_MATRIX_PATH = CAUSAL_METHYLATION_INPUT_DIR / "me_matrix.csv"
GENE_MODULE_ASSIGNMENTS_PATH = INTERMEDIATE_DATA_DIR / "gene_module_assignments.csv"
GENE_GO_MAP_PATH = INTERMEDIATE_DATA_DIR / "gene_GO_term_map_filtered.csv"
GENE_MODULE_MEMBERSHIP_PATH = INTERMEDIATE_DATA_DIR / "gene_module_kme_matrix.csv"
GENE_METHYLATION_MATRIX_PATH = INTERMEDIATE_DATA_DIR / "gene_methylation_matrix.csv"
DMR_GENE_MAP_PATH = INTERMEDIATE_DATA_DIR / "dmr_gene_map.csv"
METADATA_PATH = METADATA_DIR / "train_metadata.csv"
DMR_METHYLATION_DATA_PATH = DMR_METHYLATION_DIR / "train_dmr_matrix.csv"

RESULTS_DIR = ROOT / "results"
CAUSAL_OUTPUT_DIR = RESULTS_DIR / "causal_pipeline"
EDGE_LISTS_DIR = CAUSAL_OUTPUT_DIR / "edge_lists"
GRAPHS_DIR = CAUSAL_OUTPUT_DIR / "graphs"

me_matrix = pd.read_csv(ME_MATRIX_PATH)
gene_module_assignments = pd.read_csv(GENE_MODULE_ASSIGNMENTS_PATH)
gene_go_map = pd.read_csv(GENE_GO_MAP_PATH)
gene_module_membership = pd.read_csv(GENE_MODULE_MEMBERSHIP_PATH)
gene_methylation_data = pd.read_csv(GENE_METHYLATION_MATRIX_PATH)
metadata = pd.read_csv(METADATA_PATH)
dmr_gene_map = pd.read_csv(DMR_GENE_MAP_PATH)
dmr_methylation_data = pd.read_csv(DMR_METHYLATION_DATA_PATH)

def run_causal_pipeline():

    me_input_matrix = pd.merge(me_matrix, metadata, on='sample_id', how='inner')

    me_graph, me_edges, gene_matrix = mel.run_me_level_stage(
        me_matrix=me_input_matrix,
        gene_module_assignments=gene_module_assignments, 
        gene_go_map=gene_go_map, 
        gene_module_membership=gene_module_membership, 
        gene_methylation_data=gene_methylation_data, 
        metadata=metadata, 
    )

    with open(GRAPHS_DIR / "module_eigengenes_causal_graph_dag.pkl", "wb") as f:
        pickle.dump(me_graph, f)

    me_edges.to_csv(
        EDGE_LISTS_DIR / "module_eigengenes_causal_graph_edges.csv", 
        index=False
    )

    gene_matrix.to_csv(
        CAUSAL_METHYLATION_INPUT_DIR / "gene_matrix.csv", 
        index=False
    )

    gene_graph, gene_edges, dmr_matrix = genel.run_gene_level_stage(
        gene_matrix=gene_matrix,
        dmr_gene_map=dmr_gene_map,
        dmr_methylation_data=dmr_methylation_data,
        metadata=metadata,
    )

    with open(GRAPHS_DIR / "genes_causal_graph_dag.pkl", "wb") as f:
        pickle.dump(gene_graph, f)

    gene_edges.to_csv(
        EDGE_LISTS_DIR / "genes_causal_graph_edges.csv", 
        index=False
    )

    dmr_matrix.to_csv(
        CAUSAL_METHYLATION_INPUT_DIR / "dmr_matrix.csv", 
        index=False
    )

    graph, falsification_results, modified_graph, dmr_edges = dmrl.run_dmr_level_stage(dmr_matrix=dmr_matrix)

    if modified_graph:
        with open(GRAPHS_DIR / "dmrs_causal_graph_dag.pkl", "wb") as f:
            pickle.dump(modified_graph, f)
    else:
        with open(GRAPHS_DIR / "dmrs_causal_graph_dag.pkl", "wb") as f:
            pickle.dump(graph, f)

    with open(CAUSAL_OUTPUT_DIR / "falsification_results.txt", "a") as f:
        f.write("\n" + "=" * 80 + "\n\n")
        print(falsification_results, file=f)

    dmr_edges.to_csv(
        EDGE_LISTS_DIR / "dmrs_causal_graph_edges.csv", 
        index=False
    )

if __name__ == "__main__":
    run_causal_pipeline()