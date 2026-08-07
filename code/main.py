from preprocessing.run_preprocessing import run_preprocessing 
from hierarchical_aggregation.run_aggregation import run_aggregation 
from gene_ontology.run_gene_ontology import run_gene_ontology
from causal_pipeline.run_causal_pipeline import run_causal_pipeline

def main():
    print("=== Starting full pipeline ===")

    run_preprocessing()
    run_aggregation()
    run_gene_ontology()
    run_causal_pipeline()

    print("=== Pipeline complete ===")

if __name__ == "__main__":
    main()