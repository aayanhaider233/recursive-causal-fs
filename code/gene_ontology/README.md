# Gene Ontology



This stage performs Gene Ontology enrichment analysis and filters the gene-GO term map obtained using specified keywords.





### Input



* `data/intermediate/dmr_gene_map.csv`
* `annotations/gene_ontology/go-basic.obo`





### Output



* `data/intermediate/gene_GO_term_map.csv`
* `data/intermediate/gene_GO_term_map_filtered.csv`





### Execution



Run the stage driver:



```bash

python run_gene_ontology.py

```



Or run the full project pipeline from code/:



```bash

python main.py

```





### Structure



|**Order**|**Module**|**Description**|
|-|-|-|
|01|`enrichment_analysis.py`|Performs GO enrichment analysis and maps term IDs to readable term names|
|02|`keyword_filter.py`|Filters the gene-GO term map using specified keywords relevant to the study|
|03|`run_gene_ontology.py`|Stage driver for the entire GO workflow|





### Workflow



1. GO enrichment analysis
2. Map term IDs to term names using `go-basic.obo`
3. Filter gene-GO term map using specified keywords





#### Notes



* The enrichment analysis queries the sub-ontology of biological processes (`GO:BP`) only for this study.
* The FDR threshold used for enrichment analysis is defined near the top of `enrichment_analysis.py` and can be modified as required.
* The keywords used for filtering is defined near the top of `keyword_filter.py` and can be modified as required.


