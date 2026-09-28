"""Quality, utility and simple privacy-oriented evaluation."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    roc_auc_score,
)
from sklearn.preprocessing import LabelEncoder, StandardScaler


def make_metadata(frame: pd.DataFrame, target: str) -> dict:
    columns = {
        column: {"sdtype": "numerical"}
        for column in frame.columns
        if column != target
    }
    columns[target] = {"sdtype": "categorical"}
    return {"columns": columns}


def sdmetrics_quality(real_train: pd.DataFrame, synthetic: pd.DataFrame, target: str) -> dict:
    from sdmetrics.reports.single_table import QualityReport

    report = QualityReport()
    report.generate(real_train, synthetic, make_metadata(real_train, target))
    properties = report.get_properties().set_index("Property")["Score"].to_dict()
    return {
        "sdmetrics_overall": float(report.get_score()),
        "column_shapes": float(properties.get("Column Shapes", np.nan)),
        "column_pair_trends": float(properties.get("Column Pair Trends", np.nan)),
    }


def standardised_wasserstein_mean(real: pd.DataFrame, synthetic: pd.DataFrame) -> float:
    from scipy.stats import wasserstein_distance

    scaler = StandardScaler()
    real_scaled = scaler.fit_transform(real)
    synth_scaled = scaler.transform(synthetic)
    distances = [
        wasserstein_distance(real_scaled[:, i], synth_scaled[:, i])
        for i in range(real_scaled.shape[1])
    ]
    return float(np.mean(distances))


def exact_duplicate_rate(real_train: pd.DataFrame, synthetic: pd.DataFrame) -> float:
    merged = synthetic.merge(real_train.drop_duplicates(), how="inner")
    return float(len(merged) / len(synthetic)) if len(synthetic) else float("nan")


def _probability_matrix(model: object, X: pd.DataFrame) -> np.ndarray | None:
    if hasattr(model, "predict_proba"):
        return np.asarray(model.predict_proba(X))
    if hasattr(model, "decision_function"):
        return np.asarray(model.decision_function(X))
    return None


def evaluate_classifier(
    model: object,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict:
    encoder = LabelEncoder()
    encoder.fit(pd.concat([y_train.astype(str), y_test.astype(str)], ignore_index=True))
    y_train_enc = encoder.transform(y_train.astype(str))
    y_test_enc = encoder.transform(y_test.astype(str))

    model.fit(X_train, y_train_enc)
    pred = model.predict(X_test)
    scores = _probability_matrix(model, X_test)

    auc = np.nan
    if scores is not None and len(encoder.classes_) == 2:
        auc = roc_auc_score(y_test_enc, scores[:, 1] if scores.ndim == 2 else scores)
    elif scores is not None and scores.ndim == 2 and scores.shape[1] == len(encoder.classes_):
        auc = roc_auc_score(y_test_enc, scores, multi_class="ovr", average="macro")

    return {
        "accuracy": float(accuracy_score(y_test_enc, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_test_enc, pred)),
        "macro_f1": float(f1_score(y_test_enc, pred, average="macro", zero_division=0)),
        "macro_auc_ovr": float(auc),
    }
