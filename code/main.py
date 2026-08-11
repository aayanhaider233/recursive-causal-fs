from preprocessing.run_preprocessing import run_preprocessing 
from hierarchical_aggregation.run_aggregation import run_aggregation 
from gene_ontology.run_gene_ontology import run_gene_ontology
from causal_pipeline.run_causal_pipeline import run_causal_pipeline
from baseline_construction.run_baseline_construction import run_baseline_construction
from causal_feature_set_construction.run_causal_feature_set_construction import run_causal_feature_set_construction
from classification.run_classification import run_classification
from ml_performance_comparison.run_ml_performance_comparison import run_ml_performance_comparison

def main():
    print("=== Starting full pipeline ===")

    run_preprocessing()
    run_aggregation()
    run_gene_ontology()
    run_causal_pipeline()
    run_baseline_construction()
    run_causal_feature_set_construction()
    run_classification()
    run_ml_performance_comparison()

    print("=== Pipeline complete ===")

if __name__ == "__main__":
    main()