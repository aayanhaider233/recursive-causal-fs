import pandas as pd
import numpy as np
import shap

SHAP_CONFIGS = {
    "logistic_regression": {
        "explainer": shap.LinearExplainer,
        "pipeline": True,
        "model_step": "model",
        "feature_perturbation": "interventional",
    },

    "random_forest": {
        "explainer": shap.TreeExplainer,
        "pipeline": False,
        "feature_perturbation": "interventional",
        "positive_class_only": True,
    }
}

def compute_shap(model, train_set, config):
    X_train = train_set.drop(columns=["sample_id", "disease"])
    if config["pipeline"]:

        scaler = model.named_steps["scaler"]
        model = model.named_steps[config["model_step"]]

        X_used = scaler.transform(X_train)

        explainer = config["explainer"](
            model,
            X_used,
            feature_perturbation=config["feature_perturbation"],
        )

    else:

        model = model
        X_used = X_train

        explainer = config["explainer"](
            model,
            feature_perturbation=config["feature_perturbation"],
        )

    shap_values = explainer.shap_values(X_used)

    if config.get("positive_class_only", False):
        shap_values = shap_values[1]

    mean_shap = shap_values.mean(axis=0)

    shap_df = pd.DataFrame({
        "feature": X_train.columns,
        "SHAP": mean_shap,
        "abs_SHAP": np.abs(mean_shap),
    })

    shap_df = shap_df.sort_values(
        "abs_SHAP",
        ascending=False
    ).reset_index(drop=True)

    shap_df["cumulative_SHAP"] = shap_df["abs_SHAP"].cumsum()

    total_shap = shap_df["abs_SHAP"].sum()

    shap_df["cumulative_relative_SHAP"] = (
        shap_df["cumulative_SHAP"] / total_shap
    )

    return shap_df
