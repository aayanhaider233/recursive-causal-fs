import pre_shap_processing_training as preshap
import shap_computation as sc
import shap_ranking_filter as srfilter

import pandas as pd

MODEL_CONFIGS = preshap.MODEL_CONFIGS
SHAP_CONFIGS = sc.SHAP_CONFIGS

def construct_shap_baseline(train_dmr_matrix, test_dmr_matrix, train_metadata, test_metadata):

    train_set = pd.merge(train_dmr_matrix, train_metadata, on="sample_id", how="inner").drop("sample_id", axis=1)
    test_set = pd.merge(test_dmr_matrix, test_metadata, on="sample_id", how="inner").drop("sample_id", axis=1)

    selected_dmrs = preshap.select_top_n_dmrs_by_variance(
        train_dmr_matrix=train_dmr_matrix
    )

    shap_train_set = preshap.subset_datasets(
        train_set=train_set,
        selected_dmrs=selected_dmrs
    )

    shap_test_set = preshap.subset_datasets(
        train_set=test_set,
        selected_dmrs=selected_dmrs
    )


    lr_model = preshap.train_model(
        config=MODEL_CONFIGS["logistic_regression"],
        train_set=shap_train_set
    )

    lr_shap = sc.compute_shap(
        model=lr_model,
        train_set=shap_train_set,
        config=SHAP_CONFIGS["logistic_regression"]
    )

    lr_top_features = srfilter.select_top_shap_features(
        shap_df=lr_shap
    )

    lr_final_train, lr_final_test = srfilter.subset_train_test_sets(
        top_features=lr_top_features,
        train_set=shap_train_set,
        test_set=shap_test_set
    )


    rf_model = preshap.train_model(
        config=MODEL_CONFIGS["random_forest"],
        train_set=shap_train_set
    )

    rf_shap = sc.compute_shap(
        model=rf_model,
        train_set=shap_train_set,
        config=SHAP_CONFIGS["random_forest"]
    )

    rf_top_features = srfilter.select_top_shap_features(
        shap_df=rf_shap
    )

    rf_final_train, rf_final_test = srfilter.subset_train_test_sets(
        top_features=rf_top_features,
        train_set=shap_train_set,
        test_set=shap_test_set
    )

    return (
        lr_final_train, 
        lr_final_test,
        rf_final_train,
        rf_final_test
    )