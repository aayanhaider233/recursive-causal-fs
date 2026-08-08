import pandas as pd
from joblib import load
from pathlib import Path

import model_testing as mtest


# --------------------------------------------------
# Paths
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
CLASSIFICATION_DATA_DIR = DATA_DIR / "classification"

RESULTS_DIR = ROOT / "results"
CLASSIFICATION_OUTPUT_DIR = (
    RESULTS_DIR / "classification_performance"
)

MODEL_OUTPUT_PATH = (
    CLASSIFICATION_OUTPUT_DIR / "models"
)

METRIC_OUTPUT_PATH = (
    CLASSIFICATION_OUTPUT_DIR / "performance_metrics"
)


# --------------------------------------------------
# Model / test-set mapping
# --------------------------------------------------

MODEL_TEST_MAPPING = {
    "s0_logistic_regression": {
        "model": "s0_logistic_regression.joblib",
        "test": "test_s0.csv",
        "dataset": "s0",
        "model_name": "logistic_regression",
    },

    "s0_random_forest": {
        "model": "s0_random_forest.joblib",
        "test": "test_s0.csv",
        "dataset": "s0",
        "model_name": "random_forest",
    },

    "s1_logistic_regression": {
        "model": "s1_logistic_regression.joblib",
        "test": "test_s1_lr.csv",
        "dataset": "s1",
        "model_name": "logistic_regression",
    },

    "s1_random_forest": {
        "model": "s1_random_forest.joblib",
        "test": "test_s1_rf.csv",
        "dataset": "s1",
        "model_name": "random_forest",
    },

    "c0_logistic_regression": {
        "model": "c0_logistic_regression.joblib",
        "test": "test_c0.csv",
        "dataset": "c0",
        "model_name": "logistic_regression",
    },

    "c0_random_forest": {
        "model": "c0_random_forest.joblib",
        "test": "test_c0.csv",
        "dataset": "c0",
        "model_name": "random_forest",
    },

    "c1_logistic_regression": {
        "model": "c1_logistic_regression.joblib",
        "test": "test_c1.csv",
        "dataset": "c1",
        "model_name": "logistic_regression",
    },

    "c1_random_forest": {
        "model": "c1_random_forest.joblib",
        "test": "test_c1.csv",
        "dataset": "c1",
        "model_name": "random_forest",
    },
}


# --------------------------------------------------
# Testing
# --------------------------------------------------

def run_model_testing():

    METRIC_OUTPUT_PATH.mkdir(
        parents=True,
        exist_ok=True,
    )

    results = []

    for config in MODEL_TEST_MAPPING.values():

        model = load(
            MODEL_OUTPUT_PATH / config["model"]
        )

        test_set = pd.read_csv(
            CLASSIFICATION_DATA_DIR / config["test"]
        )

        metrics = mtest.evaluate_model(
            model=model,
            test_set=test_set,
        )

        results.append({
            "dataset": config["dataset"],
            "model": config["model_name"],
            "accuracy": metrics["accuracy"],
            "precision": metrics["precision"],
            "recall": metrics["recall"],
            "f1_score": metrics["f1_score"],
            "f2_score": metrics["f2_score"],
            "ROC-AUC": metrics["ROC-AUC"],
        })

    results_df = pd.DataFrame(results)

    output_path = (
        METRIC_OUTPUT_PATH / "test_performances.csv"
    )

    results_df.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Test performance results saved to: {output_path}"
    )

    return results_df


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":
    run_model_testing()