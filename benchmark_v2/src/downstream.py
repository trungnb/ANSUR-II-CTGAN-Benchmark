"""Fixed downstream pipelines for TRTR and TSTR evaluation."""

from __future__ import annotations

from collections.abc import Mapping

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from xgboost import XGBClassifier


def build_models(seed: int) -> Mapping[str, object]:
    """Return fixed models; only scale algorithms that are scale-sensitive."""
    return {
        "Dummy": DummyClassifier(strategy="most_frequent"),
        "XGBoost": XGBClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=seed,
            eval_metric="logloss",
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=seed,
            n_jobs=-1,
        ),
        "Logistic Regression": Pipeline(
            [
                ("scale", StandardScaler()),
                (
                    "model",
                    LogisticRegression(max_iter=5000, random_state=seed),
                ),
            ]
        ),
        "SVM": Pipeline(
            [
                ("scale", StandardScaler()),
                ("model", SVC(kernel="rbf", probability=True, random_state=seed)),
            ]
        ),
    }
