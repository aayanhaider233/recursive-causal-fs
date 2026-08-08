import construct_causal_sets as concausal

import pandas as pd
from pathlib import Path 

ROOT = Path(__file__).resolve.parents[2]
DATA_DIR = ROOT / "data"
METHYLATION_DATA_DIR = DATA_DIR / "methylation"
METADATA_DIR = DATA_DIR / "metadata"
EAA_DATA_DIR = DATA_DIR / "eaa"
CAUSAL_METHYLATION_INPUT_DIR = DATA_DIR / "causal_methylation_inputs"
CLASSIFICATION_DATA_DIR = DATA_DIR / "classification"

CAUSAL_TRAIN_SET_PATH = CAUSAL_METHYLATION_INPUT_DIR / "dmr_matrix.csv"
TEST_DMR_PATH = METHYLATION_DATA_DIR / "test_dmr_matrix.csv"
TEST_METADATA_PATH = METADATA_DIR / "test_metadata.csv"
TRAIN_EAA_PATH = EAA_DATA_DIR / "train_eaa.csv"
TEST_EAA_PATH = EAA_DATA_DIR / "test_eaa.csv"

causal_train_set = pd.read_csv(CAUSAL_TRAIN_SET_PATH)
test_dmr_matrix = pd.read_csv(TEST_DMR_PATH)
test_metadata = pd.read_csv(TEST_METADATA_PATH)
train_eaa = pd.read_csv(TRAIN_EAA_PATH)
test_eaa = pd.read_csv(TEST_EAA_PATH)

def run_causal_feature_set_construction():

    datasets = {}

    core_train_set, core_test_set = concausal.construct_core_causal_sets(
        core_train_set=causal_train_set,
        test_dmr_matrix=test_dmr_matrix,
        test_metadata=test_metadata
    )

    datasets["train_c0"] = core_train_set
    datasets["test_c0"] = core_test_set

    enhanced_train_set, enhanced_test_set = concausal.construct_enhanced_causal_sets(
        core_train_set=core_train_set,
        core_test_set=core_test_set,
        train_eaa=train_eaa,
        test_eaa=test_eaa
    )

    datasets["train_c1"] = enhanced_train_set
    datasets["test_c1"] = enhanced_test_set

    for name, df in datasets.items():
        df.to_csv(
            CLASSIFICATION_DATA_DIR / f"{name}.csv",
            index=False
        )

if __name__ == "__main__":
    run_causal_feature_set_construction()