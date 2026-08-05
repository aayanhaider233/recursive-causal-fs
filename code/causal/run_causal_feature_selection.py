# --------------------------------------------------
# Imports
# --------------------------------------------------

import me_level as mel
import gene_level as genel
import pandas as pd
from pathlib import Path
from joblib import dump 

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CAUSAL_METHYLATION_INPUT_DIR = DATA / "causal_methylation_inputs"
INTERMEDIATE_DATA_DIR = DATA / "intermediate"
METADATA_DIR = DATA / "metadata"

ME_MATRIX_PATH = CAUSAL_METHYLATION_INPUT_DIR / "me_matrix.csv"
GENE_MODULE_ASSIGNMENTS_PATH = INTERMEDIATE_DATA_DIR / "gene_module_assignments.csv"
GENE_GO_MAP_PATH = INTERMEDIATE_DATA_DIR / "gene_GO_term_map_filtered.csv"
GENE_MODULE_MEMBERSHIP_PATH = INTERMEDIATE_DATA_DIR / "gene_module_kme_matrix.csv"
GENE_METHYLATION_MATRIX_PATH = INTERMEDIATE_DATA_DIR / "gene_methylation_matrix.csv"
METADATA_PATH = METADATA_DIR / "train_metadata.csv"

RESULTS_DIR = ROOT / "results"
CAUSAL_OUTPUT_DIR = RESULTS_DIR / "causal_discovery"
EDGE_LISTS_DIR = CAUSAL_OUTPUT_DIR / "edge_lists"
GRAPHS_DIR = CAUSAL_OUTPUT_DIR / "graphs"

me_matrix = pd.read_csv(ME_MATRIX_PATH)
gene_module_assignments = pd.read_csv(GENE_MODULE_ASSIGNMENTS_PATH)
gene_go_map = pd.read_csv(GENE_GO_MAP_PATH)
gene_module_membership = pd.read_csv(GENE_MODULE_MEMBERSHIP_PATH)
gene_methylation_data = pd.read_csv(GENE_METHYLATION_MATRIX_PATH)
metadata = pd.read_csv(METADATA_PATH)

def run_causal_feature_selection():

    me_graph, edge_df, final_gene_df = mel.run_me_level_stage(
        me_matrix=me_matrix,
        gene_module_assignments=gene_module_assignments, 
        gene_go_map=gene_go_map, 
        gene_module_membership=gene_module_membership, 
        gene_methylation_data=gene_methylation_data, 
        metadata=metadata, 
    )

    dump(
        me_graph, 
        GRAPHS_DIR / "module_eigengenes_causal_graph_dag.joblib"
    )

    edge_df.to_csv(
        EDGE_LISTS_DIR / "module_eigengenes_causal_graph_edges.csv", 
        index=False
    )

    final_gene_df.to_csv(
        CAUSAL_METHYLATION_INPUT_DIR / "gene_matrix.csv", 
        index=False
    )

    

if __name__ == "__main__":
    run_causal_feature_selection()