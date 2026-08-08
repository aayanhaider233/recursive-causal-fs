import pandas as pd

from sklearn.metrics import (
    roc_auc_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    fbeta_score,
)


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

    "ROC-AUC": {
        "func": roc_auc_score,
        "prob": True,
    },
}

def compute_metric(model, test_set, metric):

    X_test = test_set.drop(
        columns=["sample_id", OUTCOME]
    )

    y_test = test_set[OUTCOME]

    config = METRICS[metric]

    if config["prob"]:
        predictions = model.predict_proba(X_test)[:, 1]
    else:
        predictions = model.predict(X_test)

    return config["func"](
        y_test,
        predictions,
    )


def evaluate_model(model, test_set):

    results = {}

    for metric in METRICS:

        results[metric] = compute_metric(
            model=model,
            test_set=test_set,
            metric=metric,
        )

    return results
