import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.utils import resample
from lingam import DirectLiNGAM
from lingam.utils import make_prior_knowledge
from dowhy import CausalModel
import networkx as nx
import statsmodels.api as sm
from itertools import product

REFUTATION_METHODS = {
    "bootstrap": {
        "method_name": "bootstrap_refuter",
        "column": "bootstrap_refutation",
        "kwargs": {
            "num_simulations": 50
        }
    },
    "placebo": {
        "method_name": "placebo_refuter",
        "column": "placebo_refutation",
        "kwargs": {
            "placebo_type": "permute"
        }
    },
    "rcc": {
        "method_name": "random_common_cause",
        "column": "random_common_cause_refutation",
        "kwargs": {}
    }
}

def define_prior_knowledge(variables, exogenous_vars=[], sink_vars=[], forbidden_edges=[]):

    n = len(variables)
    var_idx = {var: i for i, var in enumerate(variables)}
    prior_matrix = make_prior_knowledge(n_variables=n)
    for var in exogenous_vars:
        prior_matrix[:, var_idx[var]] = 0
    for xi, xj in product(exogenous_vars, exogenous_vars):
        if xi != xj:
            prior_matrix[var_idx[xi], var_idx[xj]] = 0
    for sink in sink_vars:
        prior_matrix[var_idx[sink], :] = 0
    for src, tgt in forbidden_edges:
        prior_matrix[var_idx[src], var_idx[tgt]] = 0
    np.fill_diagonal(prior_matrix, -1)

    return prior_matrix

def bootstrap_discovery(
    data,
    n_bootstraps,
    exogenous_vars=None,
    sink_vars=None,
    forbidden_edges=None,
    seed=42
):

    if "sample_id" in data.columns.tolist():
        input_matrix = data.drop("sample_id", axis=1)
    else: 
        input_matrix = data
    
    exogenous_vars = exogenous_vars or []
    sink_vars = sink_vars or []
    forbidden_edges = forbidden_edges or []

    input_scaled = StandardScaler().fit_transform(input_matrix.values)
    variables = input_matrix.columns.tolist()
    n = len(variables)

    edge_counts = np.zeros((n, n))
    edge_weights_sum = np.zeros((n, n))

    for b in range(n_bootstraps):

        prior_matrix = define_prior_knowledge(
            variables=variables,
            exogenous_vars=exogenous_vars,
            sink_vars=sink_vars,
            forbidden_edges=forbidden_edges
        )

        input_resampled = resample(
            input_scaled, 
            random_state=seed + b
        )

        model = DirectLiNGAM(prior_knowledge=prior_matrix)

        model.fit(input_resampled)

        B = model.adjacency_matrix_

        edge_counts += (B != 0).astype(int)
        edge_weights_sum += B

    edge_freq = edge_counts / n_bootstraps
    edge_avg_weights = edge_weights_sum / n_bootstraps

    return edge_freq, edge_avg_weights, variables

def retain_edges_by_causal_score(
    edge_freq,
    edge_avg_weights,
    variables,
    edge_threshold=0.75,
    score_quantile=0.60
):

    median_abs_weight = np.median(
        np.abs(edge_avg_weights[edge_avg_weights != 0])
    )

    stability_rows = []

    n = len(variables)

    for i in range(n):
        for j in range(n):

            if i == j:
                continue

            freq = edge_freq[i, j]
            weight = edge_avg_weights[i, j]
            abs_weight = abs(weight)
            causal_score = freq * abs_weight

            if freq >= 0.80 and abs_weight >= median_abs_weight:
                edge_type = "strong_stable"
            elif freq >= 0.80:
                edge_type = "weak_stable"
            elif freq >= edge_threshold:
                edge_type = "moderate"
            else:
                edge_type = "unstable"

            stability_rows.append({
                "source": variables[i],
                "target": variables[j],
                "bootstrap_freq": freq,
                "causal_estimate": weight,
                "abs_weight": abs_weight,
                "causal_score": causal_score,
                "edge_type": edge_type
            })

    stability_df = pd.DataFrame(stability_rows)

    score_threshold = stability_df["causal_score"].quantile(score_quantile)

    candidate_df = stability_df[
        (stability_df["bootstrap_freq"] >= edge_threshold) &
        (stability_df["causal_score"] >= score_threshold)
    ].reset_index(drop=True)

    return candidate_df

def resolve_directional_ambiguity(
    candidate_df,
    edge_freq,
    edge_avg_weights,
    variables,
    edge_threshold=0.75,
    ambiguity_threshold=0.20
):

    var_idx = {v: i for i, v in enumerate(variables)}

    robust_edges = []

    for _, row in candidate_df.iterrows():

        source = row["source"]
        target = row["target"]

        i = var_idx[source]
        j = var_idx[target]

        f_ij = edge_freq[i, j]
        f_ji = edge_freq[j, i]

        if max(f_ij, f_ji) < edge_threshold:
            continue

        diff = f_ij - f_ji
        total = f_ij + f_ji + 1e-8
        norm_diff = diff / total

        if abs(norm_diff) < ambiguity_threshold:
            continue

        if diff > 0:
            robust_edges.append({
                "source": source,
                "target": target,
                "freq": f_ij,
                "weight": edge_avg_weights[i, j],
                "score": f_ij * abs(edge_avg_weights[i, j])
            })
        else:
            robust_edges.append({
                "source": target,
                "target": source,
                "freq": f_ji,
                "weight": edge_avg_weights[j, i],
                "score": f_ji * abs(edge_avg_weights[j, i])
            })

    return robust_edges

def construct_graph_from_edges(variables, robust_edges):
    G = nx.DiGraph()
    G.add_nodes_from(variables)
    for e in robust_edges:
        G.add_edge(
            e["source"],
            e["target"],
            weight=e["weight"],
            freq=e["freq"],
            score=e["score"]
        )
    return G

def ace_estimation(data, G):

    parent_map = {
        node: list(G.predecessors(node))
        for node in G.nodes
    }

    results = []

    for source, target, attrs in G.edges(data=True):

        adjustment_set = [
            parent
            for parent in parent_map[target]
            if parent != source
        ]

        df = data[[source, target] + adjustment_set].copy()

        model = CausalModel(
            data=df,
            treatment=source,
            outcome=target,
            common_causes=adjustment_set
        )

        estimand = model.identify_effect()

        glm_family = (
            sm.families.Binomial()
            if df[target].nunique() == 2
            else sm.families.Gaussian()
        )

        estimate = model.estimate_effect(
            estimand,
            method_name="backdoor.generalized_linear_model",
            method_params={
                "glm_family": glm_family
            }
        )

        results.append({
            "source": source,
            "target": target,
            "average_causal_effect_estimate": estimate.value,
            "bootstrap_edge_frequency": attrs["freq"],
            "_model": model,
            "_estimand": estimand,
            "_estimate": estimate
        })

    return pd.DataFrame(results)

def apply_refutations(
    ace_df,
    refutation_methods=None
):

    ace_df = ace_df.copy()

    if refutation_methods is None:

        return ace_df.drop(
            columns=["_model", "_estimand", "_estimate"]
        )

    for config in refutation_methods.values():
        ace_df[config["column"]] = np.nan

    for idx, row in ace_df.iterrows():

        model = row["_model"]
        estimand = row["_estimand"]
        estimate = row["_estimate"]

        for config in refutation_methods.values():

            refutation = model.refute_estimate(
                estimand,
                estimate,
                method_name=config["method_name"],
                **config["kwargs"]
            )

            ace_df.loc[idx, config["column"]] = refutation.new_effect

    return ace_df.drop(
        columns=["_model", "_estimand", "_estimate"]
    )
