import construct_statistical_baseline as constat
import construct_shap_baseline as conshap

import pandas as pd
from functools import reduce
from pathlib import Path 

ROOT = Path(__file__).resolve.parents[2]
DATA_DIR = ROOT / "data"
METHYLATION_DATA_DIR = DATA_DIR / "methylation"
METADATA_DIR = DATA_DIR / "metadata"
EAA_DATA_DIR = DATA_DIR / "eaa"
CLASSIFICATION_DATA_DIR = DATA_DIR / "classification"

TRAIN_DMR_PATH = METHYLATION_DATA_DIR / "train_dmr_matrix.csv"
TEST_DMR_PATH = METHYLATION_DATA_DIR / "test_dmr_matrix.csv"
TRAIN_METADATA_PATH = METADATA_DIR / "train_metadata.csv"
TEST_METADATA_PATH = METADATA_DIR / "test_metadata.csv"
TRAIN_EAA_PATH = EAA_DATA_DIR / "train_eaa.csv"
TEST_EAA_PATH = EAA_DATA_DIR / "test_eaa.csv"

train_dmr_matrix = pd.read_csv(TRAIN_DMR_PATH)
test_dmr_matrix = pd.read_csv(TEST_DMR_PATH)
train_metadata = pd.read_csv(TRAIN_METADATA_PATH)
test_metadata = pd.read_csv(TEST_METADATA_PATH)
train_eaa = pd.read_csv(TRAIN_EAA_PATH)
test_eaa = pd.read_csv(TEST_EAA_PATH)

def run_baseline_construction():

    datasets = {}

    train_dmr_matrix_pruned, test_dmr_matrix_pruned = constat.construct_statistical_baseline(
        train_dmr_matrix=train_dmr_matrix,
        test_dmr_matrix=test_dmr_matrix
    )

    train_set_pruned = reduce(
        lambda left, right: pd.merge(left, right, on="sample_id", how="inner"),
        [train_dmr_matrix_pruned, train_metadata, train_eaa]
    )

    test_set_pruned = reduce(
        lambda left, right: pd.merge(left, right, on="sample_id", how="inner"),
        [test_dmr_matrix_pruned, test_metadata, test_eaa]
    )


    shap_train_set, shap_test_set, lr_final_train, lr_final_test, rf_final_train, rf_final_test = conshap.construct_shap_baseline(
        train_set=train_set_pruned, 
        test_set=test_set_pruned
    )

    datasets["train_s0"] = train_set_pruned
    datasets["test_s0"] = test_set_pruned
    datasets["train_s0_prime"] = shap_train_set
    # datasets["test_s0_prime"] = shap_test_set
    datasets["train_s1_lr"] = lr_final_train
    datasets["test_s1_lr"] = lr_final_test
    datasets["train_s1_rf"] = rf_final_train
    datasets["test_s1_rf"] = rf_final_test

    for name, df in datasets.items():
        df.to_csv(
            CLASSIFICATION_DATA_DIR / f"{name}.csv",
            index=False
        )

if __name__ == "__main__":
    run_baseline_construction()