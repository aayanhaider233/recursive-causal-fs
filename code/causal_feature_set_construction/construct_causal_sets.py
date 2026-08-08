import pandas as pd

def construct_core_causal_sets(core_train_set, test_dmr_matrix, test_metadata):
    selected_features = core_train_set.drop("sample_id", axis=1).columns.tolist()
    test_set = pd.merge(test_metadata, test_dmr_matrix, on="sample_id", how="inner")

    core_test_set = test_set[["sample_id"] + selected_features]

    return core_train_set, core_test_set

def construct_enhanced_causal_sets(core_train_set, core_test_set, train_eaa, test_eaa):
    enhanced_train_set = pd.merge(train_eaa, core_train_set, on="sample_id", how="inner")
    enhanced_test_set = pd.merge(test_eaa, core_test_set, on="sample_id", how="inner")

    return enhanced_train_set, enhanced_test_set