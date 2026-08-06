from preprocessing.run_preprocessing import run_preprocessing 
from hierarchical_aggregation.run_aggregation import run_aggregation 
from causal_pipeline.run_causal_pipeline import run_causal_pipeline

def main():
    print("=== Starting full pipeline ===")

    run_preprocessing()
    run_aggregation()
    run_causal_pipeline()

    print("=== Pipeline complete ===")

if __name__ == "__main__":
    main()