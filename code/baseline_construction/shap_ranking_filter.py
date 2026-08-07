import pandas as pd

SHAP_THRESHOLD = 0.8

def select_top_shap_features(shap_df):

    shap_df['cumulative_relative_SHAP'] = pd.to_numeric(
        shap_df['cumulative_relative_SHAP'], 
        errors='coerce'
    )

    top_features_df = shap_df[
        shap_df['cumulative_relative_SHAP'] <= SHAP_THRESHOLD
    ].copy()

    top_features_df = top_features_df.sort_values(
        'abs_SHAP', 
        ascending=False
    )

    return top_features_df["feature"].astype(str).tolist()

def subset_train_test_sets(top_features, train_set, test_set):

    features = train_set.columns.tolist()

    metadata_cols = [
        c for c in features 
        if "DMR" not in c
    ]

    final_features = metadata_cols + [
        f for f in top_features 
        if f not in metadata_cols
    ]

    missing_train = set(final_features) - set(train_set.columns)
    missing_test = set(final_features) - set(test_set.columns)

    if missing_train:
        raise ValueError(f"Missing columns in TRAIN set: {missing_train}")

    if missing_test:
        raise ValueError(f"Missing columns in TEST set: {missing_test}")

    final_train_set = train_set[final_features]
    final_test_set = test_set[final_features]
    
    return final_train_set, final_test_set