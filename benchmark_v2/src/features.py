"""Leakage-safe feature selection helpers."""

from __future__ import annotations

import math

import pandas as pd
from sklearn.preprocessing import LabelEncoder


def select_correlated_features_train_only(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    fraction: float = 0.25,
) -> list[str]:
    """Select top absolute-correlation features using training data only.

    This reproduces the intent of the historical Age_Group experiment while
    preventing holdout information from entering feature selection.
    """
    if not 0 < fraction <= 1:
        raise ValueError("fraction must be in (0, 1].")
    if not X_train.index.equals(y_train.index):
        y_train = y_train.reindex(X_train.index)
    if y_train.isna().any():
        raise ValueError("y_train contains missing values after index alignment.")

    numeric = X_train.select_dtypes(include="number")
    if numeric.shape[1] == 0:
        raise ValueError("No numeric features available for correlation selection.")

    encoder = LabelEncoder()
    y_encoded = pd.Series(encoder.fit_transform(y_train.astype(str)), index=y_train.index)
    correlations = numeric.apply(lambda col: col.corr(y_encoded)).abs().fillna(0.0)
    n_keep = max(1, math.floor(len(correlations) * fraction))
    return correlations.nlargest(n_keep).index.tolist()


def apply_feature_list(X: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    missing = [column for column in features if column not in X.columns]
    if missing:
        raise ValueError(f"Missing selected features: {missing}")
    return X.loc[:, features].copy()
