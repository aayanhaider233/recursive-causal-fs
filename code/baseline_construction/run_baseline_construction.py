import construct_statistical_baseline as constat
import construct_shap_baseline as conshap

def run_baseline_construction(train_dmr_matrix, test_dmr_matrix, train_metadata, test_metadata):

    cluster_info, train_dmr_matrix_pruned, test_dmr_matrix_pruned = constat.construct_statistical_baseline(
        train_dmr_matrix=train_dmr_matrix,
        test_dmr_matrix=test_dmr_matrix
    )

    lr_final_train, lr_final_test, rf_final_train, rf_final_test = conshap.construct_shap_baseline(
        train_dmr_matrix=train_dmr_matrix_pruned, 
        test_dmr_matrix=test_dmr_matrix_pruned, 
        train_metadata=train_metadata, 
        test_metadata=test_metadata
    )