import pandas as pd

def extract_parent_genes(edges, traits, target="disease"):
    trait_columns = traits.drop("sample_id", axis=1).columns.tolist()
    genes = (
        edges.loc[edges["target"] == target, "source"]
        .loc[lambda s: ~s.isin(trait_columns)]
        .drop_duplicates()
        .tolist()
    )

    return genes


def reverse_map_genes_to_dmrs(parent_genes, dmr_gene_map):
    dmr_map = (
        dmr_gene_map[
            dmr_gene_map["Gene"].isin(parent_genes)
        ][["Gene", "DMR"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    return dmr_map


def subset_dmr_dataset(
    dmr_methylation_data,
    dmr_map
):

    dmrs = dmr_map["DMR"].unique().tolist()

    filtered_dmr_df = dmr_methylation_data[["sample_id"] + dmrs].copy()

    return filtered_dmr_df