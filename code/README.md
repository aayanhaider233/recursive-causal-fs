# Code

This directory contains the source code implementing the analytical workflow described in the study.

The project is organized into separate modules corresponding to the major stages of the analysis. Each subdirectory contains its own `README.md` with detailed documentation of the corresponding workflow, inputs, outputs, execution instructions, and module structure.

---

## Structure

```text
code/
│
├── baseline_construction/
│   └── README.md
│
├── causal_feature_set_construction/
│   └── README.md
│
├── causal_pipeline/
│   └── README.md
│
├── classification/
│   └── README.md
│
├── gene_ontology/
│   └── README.md
│
├── hierarchical_aggregation/
│   └── README.md
│
├── ml_performance_comparison/
│   └── README.md
│
├── preprocessing/
│   └── README.md
│
├── main.py
└── README.md
```

---

## Main Pipeline

The primary pipeline is coordinated by:

```text
main.py
```

This coordinates the principal stages in their required execution order.

---

## Analytical Modules

### Preprocessing

```text
code/preprocessing/
```

Contains the preprocessing and quality-control procedures applied to the CpG-level DNA methylation data.

See [`preprocessing/README.md`](preprocessing/README.md) for detailed documentation.

### Hierarchical Aggregation

```text
code/hierarchical_aggregation/
```

Contains scripts for DMR detection and aggregation, DMR-to-gene mapping, and WGCNA.

See [`hierarchical_aggregation/README.md`](hierarchical_aggregation/README.md) for detailed documentation.

### Gene Ontology

```text
code/gene_ontology/
```

Contains the gene ontology enrichment analysis and keyword-based term set filtering implementations.

See [`gene_ontology/README.md`](gene_ontology/README.md) for detailed documentation.

### Causal Pipeline

```text
code/causal_pipeline/
```

Contains the hierarchical causal-discovery workflow, including module-, gene-, and DMR-level analyses.

See [`causal_pipeline/README.md`](causal_pipeline/README.md) for detailed documentation.

### Baseline Construction

```text
code/baseline_construction/
```

Constructs the statistical and SHAP-derived baseline datasets used for classification-performance comparison.

See [`baseline_construction/README.md`](baseline_construction/README.md) for detailed documentation.

### Causal Feature Set Construction

```text
code/causal_feature_set_construction/
```

Contains scripts to construct the core and enhanced causal sets for classification.

See [`causal_feature_set_construction/README.md`](causal_feature_set_construction/README.md) for detailed documentation.

### Classification

```text
code/classification/
```

Contains model training and model evaluation scripts.

See [`classification/README.md`](classification/README.md) for detailed documentation.

### ML Performance Comparison

```text
code/ml_performance_comparison/
```

Contains scripts for the bootstrapped comparison of the difference in metric values for each trained model.

See [`ml_performance_comparison/README.md`](ml_performance_comparison/README.md) for detailed documentation.

---

## Execution

The complete workflow can be executed through:

```bash
python main.py
```

Individual stages can be executed independently using the stage-specific driver scripts documented in their respective README files.

For reproducibility, the required Python dependencies are specified in the project root-level:

```text
requirements.txt
```

Install them using:

```bash
pip install -r requirements.txt
```