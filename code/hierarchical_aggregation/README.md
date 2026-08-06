# Hierarchical aggregation



This stage performs DMR detection, CpG-to-DMR aggregation, DMR-to-gene mapping, DMR-to-gene aggregation, and WGCNA.





### Input



* `data/methylation/*_cpg_mval_matrix_corrected.csv`
* `data/metadata/train_metadata.csv`
* `annotations/methylation/humanmethylation450_15017482_v1-2.csv`





### Output



* `data/intermediate/dmr_groups.rds`
* `data/intermediate/dmr_cpg_map.csv`
* `data/intermediate/dmr_gene_map.csv`
* `data/intermediate/gene_methylation_matrix.csv`
* `data/intermediate/gene_module_assignments.csv`
* `data/intermediate/gene_module_kme_matrix.csv`
* `data/methylation/train_dmr_matrix.csv` 
* `data/methylation/test_dmr_matrix.csv`
* `data/methylation/test_cpg_mval_corrected.csv`
* `data/causal_methylation_inputs/me_matrix.csv`





### Execution



Run the stage driver:



```bash

python run_aggregation.py

```



Or run the full project pipeline from code/:



```bash

python main.py

```





### Structure



|**Order**|**Module**|**Description**|
|-|-|-|
|01|`dmr_detection.R`|Detect DMRs from CpG methylation and disease status data|
|02|`dmr_aggregation.R`|Construct aggregated DMR methylation matrix from CpG methylation matrix|
|03|`dmr_to_gene_mapping.py`|Construct DMR-gene map|
|04|`gene_aggregation.py`|Construct aggregated gene methylation matrix from DMR methylation matrix|
|05|`wgcna.R`|Perform WGCNA to obtain ME matrix, gene-module assignments, and gene-module membership matrix|
|06|`run_aggregation.py`|Stage driver for the complete hierarchical aggregation workflow|




### Workflow



1. DMR detection
2. CpG-to-DMR aggregation 
3. DMR-to-gene assignment
4. DMR-to-gene aggregation 
5. WGCNA
6. Save aggregated methylation datasets and relevant intermediate data





#### Notes



* DMR detection is performed on the training set only. The resulting DMR definitions are reused for aggregation of both the training and test sets to avoid information leakage.
* Only autosomal probes (chromosomes 1–22) are considered during DMR detection.
* CpG-to-DMR aggregation uses the mean M-value of all CpGs belonging to a detected DMR.
* DMR-to-gene mapping follows a hierarchical strategy: constituent CpG annotation → promoter overlap (TSS −2000 bp to +500 bp) → nearest gene based on the minimum distance between a TSS and the DMR's endpoints.
* DMR-to-gene aggregation uses the mean methylation value across all DMRs assigned to the same gene.
* WGCNA is performed on the gene-level methylation matrix using an unsigned network with a minimum module size of 30 and module merging at eigengene correlation r ≥ 0.75 (mergeCutHeight = 0.25).
* The final ME matrix is intended as the primary methylation input for downstream causal discovery and causal effect estimation.


