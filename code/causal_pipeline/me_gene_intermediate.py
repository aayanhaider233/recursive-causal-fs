import pandas as pd
import numpy as np

def filter_top_genes_by_me(
    edges,
    gene_modules,
    edge_frequency_threshold=0.8,
    target='disease',
):

    df = edges[
        (edges['target'] == target) &
        (edges['source'].str.startswith('ME'))
    ].copy()

    if df.empty:
        raise ValueError(f"No (ME, {target}) edges found.")

    df['abs_ace_estimate'] = df['average_causal_effect_estimate'].abs()

    ace_median = df['abs_ace_estimate'].median()
    df = df[df['bootstrap_edge_frequency'] >= edge_frequency_threshold]
    df = df[df['abs_ace_estimate'] >= ace_median]

    if df.empty:
        raise ValueError("All MEs filtered out. Consider relaxing thresholds.")

    selected_mes = df['source'].tolist()

    top_labels = [int(me.replace("ME", "")) for me in selected_mes]

    top_genes = gene_modules[
        gene_modules['ModuleLabel'].isin(top_labels)
    ].sort_values('ModuleLabel')

    return top_genes


def filter_genes_by_go_terms(genes, gene_go_map):

    filtered_genes = genes[
        genes['Gene'].isin(gene_go_map['Gene'].unique())
    ].copy()

    filtered_genes = filtered_genes.sort_values('ModuleLabel')

    return filtered_genes


def filter_genes_by_kme_scored(genes, gene_module_membership, me_edges, alpha, n_total):

    genes_in_kme = genes[genes['Gene'].isin(gene_module_membership.index)].copy()

    me_edges = me_edges.copy()

    me_edges["causal_score"] = (
        me_edges["bootstrap_edge_frequency"]
        * me_edges["average_causal_effect_estimate"].abs()
    )

    me_effect = me_edges.set_index('source')['causal_score'].to_dict()

    scored_blocks = []

    for label in genes_in_kme['ModuleLabel'].unique():

        kme_col = f'kME{label}'
        if kme_col not in gene_module_membership.columns:
            continue

        block = genes_in_kme[
            genes_in_kme['ModuleLabel'] == label
        ].copy()

        block['kME'] = block['Gene'].map(gene_module_membership[kme_col])
        block['abs_kME'] = block['kME'].abs()

        me_name = f'ME{label}'
        me_score = me_effect.get(me_name, 0.0)

        block['score'] = (block['abs_kME'] ** alpha) * me_score / len(block)
        block['ME'] = me_name

        scored_blocks.append(block)

    all_genes = pd.concat(scored_blocks)
    all_genes = all_genes.sort_values('score', ascending=False)
    top = all_genes.head(n_total)

    return all_genes, top

def prune_genes_by_correlation(gene_methylation_data, top_genes, quantile):

    genes_to_keep = top_genes["Gene"].unique()

    gene_df = gene_methylation_data.loc[:, gene_methylation_data.columns.intersection(genes_to_keep)]

    corr_matrix = gene_df.corr(method="pearson")
    corr_abs = corr_matrix.abs()

    upper = corr_abs.where(
        np.triu(np.ones(corr_abs.shape), k=1).astype(bool)
    )

    corr_values = upper.values.flatten()
    corr_values = corr_values[~np.isnan(corr_values)]
    corr_values = corr_values[corr_values > 0]

    corr_threshold = np.quantile(corr_values, quantile)

    high_corr_pairs = []

    for col in upper.columns:

        high_corr = upper[col][upper[col] >= corr_threshold]

        for row, value in high_corr.items():

            high_corr_pairs.append({
                "Gene1": row,
                "Gene2": col,
                "Correlation": value
            })

    high_corr_df = pd.DataFrame(high_corr_pairs)

    high_corr_df = high_corr_df.sort_values(
        "Correlation",
        ascending=False
    )

    to_drop = set()

    for _, row in high_corr_df.iterrows():

        gene2 = row["Gene2"]

        if gene2 not in to_drop:
            to_drop.add(gene2)

    retained_genes = [
        g for g in gene_df.columns
        if g not in to_drop
    ]

    retained_gene_df = pd.DataFrame({
        "Gene": retained_genes
    })

    return retained_gene_df

def subset_data_by_gene(data, genes):

    genes_to_keep = genes['Gene'].unique().tolist()

    filtered_gene_data = data[["sample_id"] + genes_to_keep]

    return filtered_gene_data

    