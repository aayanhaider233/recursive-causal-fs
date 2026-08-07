import pandas as pd
from gprofiler import GProfiler

FDR_THRESHOLD = 0.05

def load_go_term_names(go_dag):

    return {
        go_id: term.name
        for go_id, term in go_dag.items()
    }


def extract_query_genes(result):
    for field in (
        "intersections",
        "intersection",
        "genes",
        "query_genes",
        "gene_list",
    ):
        if field in result and result[field]:
            return result[field]

    return []


def go_enrichment_analysis(
    dmr_gene_map,
    go_dag
):
    gp = GProfiler(return_dataframe=False)

    unique_genes = (
        dmr_gene_map["Gene"]
        .dropna()
        .unique()
        .tolist()
    )

    results = gp.profile(
        organism="hsapiens",
        query=unique_genes,
        sources=["GO:BP"],
        no_evidences=False,
    )

    go_name_map = load_go_term_names(go_dag)

    mappings = []

    for result in results:

        if result.get("p_value", 1.0) > FDR_THRESHOLD:
            continue

        term_id = result["native"]
        term_name = go_name_map.get(term_id, "")

        genes = extract_query_genes(result)

        for gene in genes:
            mappings.append({
                "Gene": gene,
                "term_id": term_id,
                "term_name": term_name,
            })

    return pd.DataFrame(mappings)