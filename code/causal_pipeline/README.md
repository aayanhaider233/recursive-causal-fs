# Causal Pipeline



This stage performs the main hierarchical recursive causal feature selection followed by the DMR-level causal discovery and validation for biological interpretation.





### Input



* `data/causal_methylation_inputs/me_matrix.csv`
* `data/intermediate/gene_methylation_matrix.csv`
* `data/methylation/train_dmr_matrix.csv`
* `data/metadata/train_metadata.csv`
* `data/intermediate/gene_GO_term_map_filtered.csv`
* `data/intermediate/dmr_gene_map.csv`
* `data/intermediate/gene_module_assignments.csv`
* `data/intermediate/gene_module_kme_matrix.csv`



### Output


* `results/causal_pipeline/graphs/module_eigengenes_causal_graph_dag.pkl`
* `results/causal_pipeline/graphs/genes_causal_graph_dag.pkl`
* `results/causal_pipeline/graphs/dmrs_causal_graph_dag.pkl`
* `results/causal_pipeline/edge_lists/module_eigengenes_causal_graph_edges.csv`
* `results/causal_pipeline/edge_lists/genes_causal_graph_edges.csv`
* `results/causal_pipeline/edge_lists/dmrs_causal_graph_edges.csv`
* `results/causal_pipeline/falsification_results.txt`
* `data/causal_methylation_inputs/gene_matrix.csv`
* `data/causal_methylation_inputs/dmr_matrix.csv`





### Execution



Run the stage driver:



```bash

python run_causal_pipeline.py

```



Or run the full project pipeline from code/:



```bash

python main.py

```





### Structure



|**Order**|**Module**|**Description**|
|-|-|-|
|01|`discovery_utils.py`|Common functions across all causal discovery stages|
|02|`me_gene_intermediate.py`|Intermediate ME-parent set refinement, ME-to-gene reverse-mapping, candidate gene set refinement, and gene-level methylation data subset|
|03|`me_level.py`|Driver for ME-level stage|
|04|`gene_dmr_intermediate.py`|Intermediate gene-to-DMR reverse-mapping and DMR-level methylation data subset|
|05|`gene_level.py`|Driver for gene-level stage|
|06|`dag_falsification.py`|DMR-level DAG falsification test and causal minimality suggestion report generation function|
|07|`dmr_level.py`|Driver for DMR-level stage|
|08|`run_causal_pipeline.py`|Stage driver for entire causal feature selection and validation workflow|


### Workflow



1. ME-level causal discovery
2. ME-parent set extraction and refinement 
3. ME-to-gene reverse-mapping
4. Candidate gene set refinement (Gene Ontology, kME-based scoring, correlation pruning) 
5. Subset full gene methylation data
6. Gene-level causal discovery
7. Gene-to-DMR reverse-mapping
8. Subset full DMR methylation data
9. DMR-level causal discovery
10. DMR-level DAG falsification test
11. DMR-level DAG modification to enforce causal minimality
12. DMR-level modified DAG falsification test





#### Notes


* The pipeline assumes that all input datasets contain the same samples in the same order where corresponding matrices are used together. Sample identifiers should be consistent across all preprocessing stages.
* Module eigengene construction, DMR identification, WGCNA, GO enrichment, and metadata preprocessing are performed in earlier stages of the project and are not part of this pipeline.
* The DMR-level DAG falsification stage produces a causal minimality report. Any suggested graph modifications must be reviewed and implemented manually by the user through the placeholder DAG modification function before the final DMR-level ACE estimation and refutation analyses are performed.
* Refutation analyses are configurable through the `REFUTATION_METHODS` setting in `discovery_utils.py`. By default, the pipeline supports bootstrap, placebo, and random common cause refuters.
* Prior knowledge constraints (exogenous variables, sink variables, forbidden edges, number of bootstraps, and other thresholds) are defined near the top of each stage driver and can be modified without changing the underlying discovery utilities.
* Graphs are stored as NetworkX `DiGraph` pickle (`.pkl`) files and edge lists are exported as CSV files for downstream analysis.
