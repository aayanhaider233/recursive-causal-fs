import enrichment_analysis as ea
import keyword_filter as kf

import pandas as pd
from goatools.obo_parser import GODag
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
INTERMEDIATE_DIR = DATA_DIR / "intermediate"
ANNOTATIONS_DIR = ROOT / "annotations" / "gene_ontology"

DMR_GENE_MAP = INTERMEDIATE_DIR / "dmr_gene_map.csv"
GO_BASIC_PATH = ANNOTATIONS_DIR / "go-basic.obo"

dmr_gene_map = pd.read_csv(DMR_GENE_MAP)
go_dag = GODag(GO_BASIC_PATH)

def run_gene_ontology():
    gene_go_term_map = ea.go_enrichment_analysis(
        dmr_gene_map=dmr_gene_map,
        go_dag=go_dag
    )

    gene_go_term_map.to_csv(
        INTERMEDIATE_DIR / "gene_GO_term_map.csv",
        index=False
    )

    filtered_map = kf.keyword_filter(
        gene_go_term_map=gene_go_term_map
    )

    filtered_map.to_csv(
        INTERMEDIATE_DIR / "gene_GO_term_map_filtered.csv",
        index=False
    )

if __name__ == "__main__":
    run_gene_ontology()