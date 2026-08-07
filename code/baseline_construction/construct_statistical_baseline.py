import variance_filter as vf
import correlation_network_pruning as cnp

def construct_statistical_baseline(train_dmr_matrix, test_dmr_matrix):

    train_dmr_matrix_filtered, test_dmr_matrix_filtered = vf.variance_filter(
        train_dmr_matrix=train_dmr_matrix,
        test_dmr_matrix=test_dmr_matrix
    )

    cluster_info, train_dmr_matrix_pruned, test_dmr_matrix_pruned = cnp.prune_components(
        train_dmr_matrix=train_dmr_matrix_filtered,
        test_dmr_matrix=test_dmr_matrix_filtered
    )

    return cluster_info, train_dmr_matrix_pruned, test_dmr_matrix_pruned