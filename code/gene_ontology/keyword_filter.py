import pandas as pd

KEYWORDS = [
    # Neurodevelopment / neurons / brain
    'neuron', 'neurogenesis', 'nervous system', 'brain development', 
    # Synaptic / signaling
    'synapse', 'transmission', 'vesicle', 'signal transduction', 
    # Cognition / behavior
    'cognition', 'behavior', 'learning', 'memory', 
    # Epigenetic / methylation
    'methylation', 'chromatin', 'histone modification', 'gene expression', 'epigenetic', 
    # Immune / inflammation
    'immune', 'inflammatory', 'cytokine', 'response to stress'
]

def contains_keyword(term_name, parents):
    term_name_lower = str(term_name).lower()
    if any(k in term_name_lower for k in KEYWORDS):
        return True
    if pd.notna(parents):
        for parent in str(parents).split(','):
            if any(k in parent.lower() for k in KEYWORDS):
                return True
    return False

def keyword_filter(gene_go_term_map):

    filtered_map = gene_go_term_map[
        gene_go_term_map.apply(
            lambda row: contains_keyword(
                row['term_name'], 
                row['parents']
            ), 
            axis=1
        )
    ]

    return filtered_map