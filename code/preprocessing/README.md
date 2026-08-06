# Preprocessing



This stage performs data harmonisation, quality control, epigenetic age estimation, probe filtering, dataset concatenation, M-value conversion, batch effect correction, train-test partitioning, and epigenetic age acceleration computation.





### Input



* `data/raw/*_series_matrix.txt.gz`
* `data/raw/*.csv.gz`
* `annotations/methylation/`





### Output



* `data/intermediate/batch_info.csv`
* `data/methylation/cpg_mval_matrix_full_corrected.csv` 
* `data/methylation/train_cpg_mval_corrected.csv`
* `data/methylation/test_cpg_mval_corrected.csv`
* `data/metadata/train_metadata.csv`
* `data/metadata/test_metadata.csv`





### Execution



Run the stage driver:



```bash

python run_preprocessing.py

```



Or run the full project pipeline from code/:



```bash

python main.py

```





### Structure



|**Order**|**Module**|**Description**|
|-|-|-|
|01|`metadata_harmonisation.py`|Parse and harmonise GEO metadata|
|02|`probe_quality_control.py`|Initial probe filter, QC and, detection p-value filtering|
|03|`epigenetic_age.py`|Generate epigenetic age estimates (Horvath, Hannum, and GrimAge)|
|04|`probe_filter.py`|Remove sex-chromosome, cross-reactive, and multi-mapping probes|
|05|`concatenate_datasets.py`|Merge cohorts and generate batch information|
|06|`methylation_beta_to_M.py`|Convert methylation beta-values to M-values|
|07|`batch_effect_correction.py`|Batch effect correction|
|08|`partition_data.py`|Stratified train-test split|
|09|`epigenetic_age_acceleration.py`|Compute epigenetic age acceleration (EAA)|
|10|`run_preprocessing.py`|Stage driver for the complete preprocessing workflow|





### Workflow



1. Metadata harmonization
2. Non-CpG probe removal and quality control
3. Epigenetic age estimation
4. Annotation-based probe filtering
5. Cohort concatenation and batch information generation
6. Beta-to-M value conversion
7. Batch effect correction
8. Train-test partitioning
9. Epigenetic age acceleration computation
10. Save processed datasets





#### Notes



* Epigenetic ages are computed before annotation-based probe filtering to preserve clock-specific CpG sites.
* Batch correction is performed on the full M-value matrix before train/test partitioning.
* EAA models are fitted on the training set only and applied to the test set to avoid information leakage.
* Epigenetic age features are replaced by their corresponding EAA features.


