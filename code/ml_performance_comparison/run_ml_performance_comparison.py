from pathlib import Path
import pandas as pd
from joblib import load

import bootstrap_metric_comparison as bmc

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
CLASSIFICATION_DATA_DIR = DATA_DIR / "classification"
ML_PERFORMANCE_RESULTS_DIR = ROOT / "results" / "classification_performance" 
MODEL_DIR = ML_PERFORMANCE_RESULTS_DIR / "models"

OUTPUT_DIR = ML_PERFORMANCE_RESULTS_DIR / "performance_metrics"

TEST_SET_PATHS = {
    "c0": CLASSIFICATION_DATA_DIR / "test_c0.csv",
    "c1": CLASSIFICATION_DATA_DIR / "test_c1.csv",
    "s0": CLASSIFICATION_DATA_DIR / "test_s0.csv",
    "s1_lr": CLASSIFICATION_DATA_DIR / "test_s1_lr.csv",
    "s1_rf": CLASSIFICATION_DATA_DIR / "test_s1_rf.csv",
}

MODEL_PATHS = {
    "c0": {
        "logistic_regression" : MODEL_DIR / "c0_logistic_regression.joblib",
        "random_forest" : MODEL_DIR / "c0_random_forest.joblib",
    },

    "c1": {
        "logistic_regression" : MODEL_DIR / "c1_logistic_regression.joblib",
        "random_forest" : MODEL_DIR / "c1_random_forest.joblib",
    },

    "s0": {
        "logistic_regression" : MODEL_DIR / "s0_logistic_regression.joblib",
        "random_forest" : MODEL_DIR / "s0_random_forest.joblib",
    },

    "s1_lr": {
        "logistic_regression" : MODEL_DIR / "s1_logistic_regression.joblib",
    },

    "s1_rf": {
        "random_forest" : MODEL_DIR / "s1_random_forest.joblib",
    }
}


datasets = {
    dataset_id : pd.read_csv(path)
    for dataset_id, path in TEST_SET_PATHS.items()
}


models = {
    dataset_id: {
        model_name : load(model_path)
        for model_name, model_path in model_paths.items()
    }
    for dataset_id, model_paths in MODEL_PATHS.items()
}


def run_ml_performance_comparison():

    results_df = bmc.run_comparisons(
        datasets=datasets,
        models=models
    )

    results_df.to_csv(
        OUTPUT_DIR / "bootstrap_comparison_ci.csv",
        index=False
    )

if __name__ == "__main__":
    run_ml_performance_comparison()