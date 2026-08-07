
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline

N_TOP = 2000

MODEL_CONFIGS = {
    "logistic_regression": {
        "estimator": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(
                max_iter=5000,
                class_weight="balanced",
                random_state=42
            ))
        ]),
        "param_grid": {
            "model__C": [0.0001, 0.001, 0.01, 0.1, 1, 10],
            "model__penalty": ["l2"],
            "model__solver": ["lbfgs"],
        }
    },

    "random_forest": {
        "estimator": RandomForestClassifier(
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
        "param_grid": {
            "n_estimators": [300, 400, 500],
            "max_depth": [10, 12, 15],
            "max_features": [0.2, 0.25, 0.3],
            "min_samples_split": [2, 4],
            "min_samples_leaf": [1, 2],
        }
    }
}

CV = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

def select_top_n_dmrs_by_variance(train_dmr_matrix):

    dmr_vars = train_dmr_matrix.drop("sample_id", axis=1).var(axis=0)
    selected_dmrs = dmr_vars.sort_values(ascending=False).head(N_TOP).index.tolist()

    return selected_dmrs

def subset_datasets(train_set, selected_dmrs):

    metadata = [
        c for c in train_set.columns
        if "DMR" not in c
    ]

    return train_set[selected_dmrs + metadata]

def train_model(config, train_set):
    X_train = train_set.drop(columns=["sample_id", "disease"])
    y_train = train_set["disease"]

    grid = GridSearchCV(
        estimator=config["estimator"],
        param_grid=config["param_grid"],
        scoring="roc_auc",
        cv=CV,
        n_jobs=-1,
        verbose=2,
    )

    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_

    return best_model