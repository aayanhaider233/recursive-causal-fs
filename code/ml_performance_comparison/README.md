# ML Performance Comparison



This stage performs the bootstrap comparison of the differences in metric values for the models trained using the different feature set configurations.





### Input



* `data/classification/test_*.csv`
* `results/classification_performance/*.joblib`





### Output



* `results\classification_performance\performance_metrics\bootstrap_comparison_ci.csv`





### Execution



Run the stage driver:



```bash

python run_ml_performance_comparison.py

```



Or run the full project pipeline from code/:



```bash

python main.py

```





### Structure



|**Order**|**Module**|**Description**|
|-|-|-|
|01|`bootstrap_metric_comparison.py`|Functions to perform the bootstrap metric difference comparison|
|02|`run_ml_performance_comparison.py`|Stage driver for the entire ML performance comparison workflow|





### Workflow



1. Compute differences in metric values for each metric for the specified number of bootstraps
2. Construct 95% confidence interval for each metric and dataset comparison pair





#### Notes



* The metrics used to evaluate each model are: accuracy, precision, recall, F1 score, F2 score, and ROC-AUC.
* The metric parameters, dataset comparison pairs, and metric parameters are defined under `METRICS`, `COMPARISONS`, and `METRICS`, respectively, in `bootstrap_metric_comparison.py` and can be configured as needed.


