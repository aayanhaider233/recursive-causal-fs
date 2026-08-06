# Metadata files



`train_metadata.csv` and `test_metadata.csv` contain covariates used throughout the study.





### Variables



|**Name**|**Description**|
|-|-|
|`sample_id`|Unique identifier constructed from the original barcode and batch pair.|
|`age`|Chronological age in years.|
|`sex`|0 = Male, 1 = Female|
|`disease`|0 = Control, 1 = Schizophrenia|
|`horvath2013_EAA`|Horvath epigenetic age acceleration|
|`hannum_EAA`|Hannum epigenetic age acceleration|
|`grimage2_EAA`|GrimAge epigenetic age acceleration|





#### Notes



* Batch and barcode are not retained after sample_id construction.
* All feature-selection methods were applied to the methylation features; covariates remained unchanged.

