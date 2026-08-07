import pandas as pd
import numpy as np
import networkx as nx

CORR_THRESHOLD = 0.8

def construct_correlation_network(train_dmr_matrix):
    dmr_cols = train_dmr_matrix.drop("sample_id", axis=1).columns.tolist()
    corr_matrix = train_dmr_matrix[dmr_cols].corr().abs()

    G = nx.Graph()
    G.add_nodes_from(dmr_cols)

    dmr_array = np.array(dmr_cols)
    for i in range(len(dmr_array)):
        for j in range(i + 1, len(dmr_array)):
            if corr_matrix.iloc[i, j] >= CORR_THRESHOLD:
                G.add_edge(dmr_array[i], dmr_array[j])

    components = list(nx.connected_components(G))

    return components 

def prune_components(train_dmr_matrix, test_dmr_matrix):
    dmr_vars = train_dmr_matrix.drop("sample_id", axis=1).var(axis=0)
    dmrs_to_keep = []

    components = construct_correlation_network(train_dmr_matrix=train_dmr_matrix)

    for _, component in enumerate(components, start=1):
        component_vars = dmr_vars[list(component)]
        rep = component_vars.idxmax()
        dmrs_to_keep.append(rep)

    train_dmr_matrix_pruned = train_dmr_matrix[["sample_id"] + dmrs_to_keep]
    test_dmr_matrix_pruned = test_dmr_matrix[["sample_id"] + dmrs_to_keep]

    return train_dmr_matrix_pruned, test_dmr_matrix_pruned