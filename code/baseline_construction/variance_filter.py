QUANTILE = 0.3

def variance_filter(train_dmr_matrix, test_dmr_matrix):
    dmr_vars = train_dmr_matrix.drop("sample_id", axis=1).var(axis=0)

    var_threshold = dmr_vars.quantile(QUANTILE)

    dmrs_to_keep = dmr_vars[dmr_vars > var_threshold].index.tolist()

    train_dmr_matrix_filtered = train_dmr_matrix[["sample_id"] + dmrs_to_keep]
    test_dmr_matrix_filtered = test_dmr_matrix[["sample_id"] + dmrs_to_keep]

    return train_dmr_matrix_filtered, test_dmr_matrix_filtered