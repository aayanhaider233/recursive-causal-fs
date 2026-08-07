# Epigenetic Age Acceleration (EAA) files



`train_eaa.csv` and `test_eaa.csv` contain the EAA values used throughout the study.





### Variables



|**Name**|**Description**|
|-|-|
|`sample_id`|Unique identifier constructed from the original barcode and batch pair.|
|`horvath2013_EAA`|Horvath epigenetic age acceleration|
|`hannum_EAA`|Hannum epigenetic age acceleration|
|`grimage2_EAA`|GrimAge epigenetic age acceleration|





#### Notes



* Batch and barcode are not retained after sample_id construction.
* All feature-selection methods were applied to the methylation features; covariates remained unchanged.

