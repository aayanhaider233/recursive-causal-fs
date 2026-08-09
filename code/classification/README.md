# Classification



This stage performs machine learning (ML) model training and testing.





### Input



* All files in `data/classification/`, excluding `data/classification/train_s0_prime.csv`





### Output



* `results/classification_performance/models/*.joblib`
* `results/classification_performance/performance_metrics/test_performances.csv`





### Execution



Run the stage driver:



```bash

python run_classification.py

```



Or run the full project pipeline from code/:



```bash

python main.py

```





### Structure



|**Order**|**Module**|**Description**|
|-|-|-|
|01|`model_training.py`|Functions to train logistic regression and random forest models|
|02|`model_testing.py`|Functions to evaluate trained models|
|03|`run_classification.py`|Stage driver for the entire classification workflow|





### Workflow



* For each dataset configuration:
    1. Train logistic regression model
    2. Evaluate logistic regression model
    3. Train random forest model
    4. Evaluate random forest model





#### Notes



* Stratified cross-validation with 5 folds is used throughout the implementation and this can be configured from the `model_training.py` module using the definition `CV`.
* `GridSearchCV` is used for both model classes and the defined grid remains unchanged. This can also be configured from `model_training.py` using `param_grid` defined within the nested dictionary `MODEL_CONFIGS`.
* Other model parameters not included in `param_grid` can either be manually added or adjusted using `estimator` defined within `MODEL_CONFIGS`.
* The metrics used to evaluate each model are: accuracy, precision, recall, F1 score, F2 score, and ROC-AUC.
* Metric parameters can be configures from `model_testing.py` using the defined nested dictionary `METRICS`.


