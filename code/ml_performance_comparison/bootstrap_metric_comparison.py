import numpy as np
import pandas as pd

from sklearn.metrics import (
    roc_auc_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    fbeta_score,
)


BOOTSTRAPS = 1000

OUTCOME = "disease"

METRICS = {
    "accuracy": {
        "func": accuracy_score,
        "prob": False,
    },

    "precision": {
        "func": lambda y, p: precision_score(
            y,
            p,
            zero_division=0,
        ),
        "prob": False,
    },

    "recall": {
        "func": lambda y, p: recall_score(
            y,
            p,
            zero_division=0,
        ),
        "prob": False,
    },

    "f1_score": {
        "func": lambda y, p: f1_score(
            y,
            p,
            zero_division=0,
        ),
        "prob": False,
    },

    "f2_score": {
        "func": lambda y, p: fbeta_score(
            y,
            p,
            beta=2,
            zero_division=0,
        ),
        "prob": False,
    },

    "roc_auc": {
        "func": roc_auc_score,
        "prob": True,
    },
}

COMPARISONS = {
    "c0_c1_lr": {
        "dataset_comparison_pair": "(c0,c1)",
        "model": "logistic_regression",
        "pair": ["c0", "c1"],
    },

    "c1_s0_lr": {
        "dataset_comparison_pair": "(c1,s0)",
        "model": "logistic_regression",
        "pair": ["c1", "s0"],
    },

    "c1_s1_lr": {
        "dataset_comparison_pair": "(c1,s1)",
        "model": "logistic_regression",
        "pair": ["c1", "s1_lr"],
    },

    "c0_c1_rf": {
        "dataset_comparison_pair": "(c0,c1)",
        "model": "random_forest",
        "pair": ["c0", "c1"],
    },

    "c1_s0_rf": {
        "dataset_comparison_pair": "(c1,s0)",
        "model": "random_forest",
        "pair": ["c1", "s0"],
    },

    "c1_s1_rf": {
        "dataset_comparison_pair": "(c1,s1)",
        "model": "random_forest",
        "pair": ["c1", "s1_rf"],
    },
}

def bootstrap_delta_metric(
    y_true,
    pred1,
    pred2,
    metric_func,
    seed=42,
):
    rng = np.random.default_rng(seed)

    n = len(y_true)
    deltas = np.empty(BOOTSTRAPS)

    for b in range(BOOTSTRAPS):

        idx = rng.integers(0, n, n)

        deltas[b] = (
            metric_func(y_true[idx], pred2[idx])
            - metric_func(y_true[idx], pred1[idx])
        )

    ci_low, ci_high = np.percentile(
        deltas,
        [2.5, 97.5],
    )

    delta_obs = (
        metric_func(y_true, pred2)
        - metric_func(y_true, pred1)
    )

    return (
        float(delta_obs),
        float(ci_low),
        float(ci_high),
    )

def probs_to_labels(probs, threshold=0.5):
    return (probs >= threshold).astype(int)

def prepare_test_set(model, test_set):
    X_test = test_set.drop(columns=["sample_id", OUTCOME])

    expected_features = model.feature_names_in_

    missing_features = set(expected_features) - set(X_test.columns)

    if missing_features:
        raise ValueError(
            f"Test set is missing features required by the model: "
            f"{missing_features}"
        )

    X_test = X_test.loc[:, expected_features]

    return X_test

def compare_datasets(
    dataset1,
    dataset2,
    model1,
    model2,
):
    X1 = prepare_test_set(model1, dataset1)
    X2 = prepare_test_set(model2, dataset2)

    y1 = dataset1[OUTCOME].to_numpy()
    y2 = dataset2[OUTCOME].to_numpy()

    if not np.array_equal(y1, y2):
        raise ValueError(
            "Label mismatch between the two datasets."
        )

    y_true = y1

    prob1 = model1.predict_proba(X1)[:, 1]
    prob2 = model2.predict_proba(X2)[:, 1]

    class1 = probs_to_labels(prob1)
    class2 = probs_to_labels(prob2)

    results = {}

    for metric_name, config in METRICS.items():

        if config["prob"]:
            pred1 = prob1
            pred2 = prob2
        else:
            pred1 = class1
            pred2 = class2

        _, ci_low, ci_high = bootstrap_delta_metric(
            y_true=y_true,
            pred1=pred1,
            pred2=pred2,
            metric_func=config["func"],
        )

        results[metric_name] = [
            ci_low,
            ci_high,
        ]

    return results


def run_comparisons(datasets, models):

    rows = []

    for config in COMPARISONS.values():

        dataset_pair = config["pair"]
        model_name = config["model"]

        dataset1_id = dataset_pair[0]
        dataset2_id = dataset_pair[1]

        dataset1 = datasets[dataset1_id]
        dataset2 = datasets[dataset2_id]

        model1 = models[dataset1_id][model_name]
        model2 = models[dataset2_id][model_name]

        metric_results = compare_datasets(
            dataset1=dataset1,
            dataset2=dataset2,
            model1=model1,
            model2=model2,
        )

        row = {
            "dataset_comparison_pair":
                config["dataset_comparison_pair"],

            "model":
                model_name,
        }

        for metric_name in METRICS:

            row[f"{metric_name}_ci"] = metric_results[
                metric_name
            ]

        rows.append(row)

    return pd.DataFrame(rows)