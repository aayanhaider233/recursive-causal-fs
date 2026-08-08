import model_training as mtrain
import model_testing as mtest

import pandas as pd
from joblib import dump
from pathlib import Path


MODEL_CONFIGS = mtrain.MODEL_CONFIGS

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
CLASSIFICATION_DATA_DIR = DATA_DIR / "classification"
RESULTS_DIR = ROOT / "results"
CLASSIFICATION_OUTPUT_DIR = RESULTS_DIR / "classification_performance"

MODEL_OUTPUT_PATH = CLASSIFICATION_OUTPUT_DIR / "models"
METRIC_OUTPUT_PATH = CLASSIFICATION_OUTPUT_DIR / "performance_metrics"

DATASET_IDS = {
    "S0": ["s0"],
    "S1": ["s1_lr", "s1_rf"],
    "C0": ["c0"],
    "C1": ["c1"],
}

TRAIN_SET_PATHS = {
    suffix: CLASSIFICATION_DATA_DIR / f"train_{suffix}.csv"
    for suffixes in DATASET_IDS.values()
    for suffix in suffixes
}

TEST_SET_PATHS = {
    suffix: CLASSIFICATION_DATA_DIR / f"test_{suffix}.csv"
    for suffixes in DATASET_IDS.values()
    for suffix in suffixes
}


TRAIN_SETS = {
    suffix: pd.read_csv(path)
    for suffix, path in TRAIN_SET_PATHS.items()
}

TEST_SETS = {
    suffix: pd.read_csv(path)
    for suffix, path in TEST_SET_PATHS.items()
}

MODEL_FOR_DATASET = {
    "s0": ["logistic_regression", "random_forest"],
    "s1_lr": ["logistic_regression"],
    "s1_rf": ["random_forest"],
    "c0": ["logistic_regression", "random_forest"],
    "c1": ["logistic_regression", "random_forest"],
}

def run_classification():

    fitted_models = {}
    results = []

    for dataset_id, model_names in MODEL_FOR_DATASET.items():

        train_set = TRAIN_SETS[dataset_id]
        test_set = TEST_SETS[dataset_id]

        fitted_models[dataset_id] = {}

        for model_name in model_names:

            model = mtrain.train_model(
                config=MODEL_CONFIGS[model_name],
                train_set=train_set,
            )

            result_dataset_id = (
                "s1"
                if dataset_id in ["s1_lr", "s1_rf"]
                else dataset_id
            )

            dump(
                model, 
                MODEL_OUTPUT_PATH / f"{result_dataset_id}_{model_name}.joblib"
            )

            fitted_models[dataset_id][model_name] = model

            metrics = mtest.evaluate_model(
                model=model,
                test_set=test_set,
            )

            results.append({
                "dataset": result_dataset_id,
                "model": model_name,
                "accuracy": metrics["accuracy"],
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1_score": metrics["f1_score"],
                "f2_score": metrics["f2_score"],
                "ROC-AUC": metrics["ROC-AUC"],
            })

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        METRIC_OUTPUT_PATH / "test_performances.csv",
        index=False
    )

if __name__ == "__main__":
    run_classification()