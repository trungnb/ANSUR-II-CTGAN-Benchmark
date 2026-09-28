import pandas as pd

from src.features import apply_feature_list, select_correlated_features_train_only


def test_feature_selection_uses_training_input_only():
    X_train = pd.DataFrame(
        {
            "signal": [0, 0, 1, 1, 2, 2, 3, 3],
            "noise": [1, 0, 1, 0, 1, 0, 1, 0],
            "other": [2, 4, 1, 3, 5, 7, 6, 8],
            "other2": [8, 1, 7, 2, 6, 3, 5, 4],
        }
    )
    y_train = pd.Series(["a", "a", "b", "b", "c", "c", "d", "d"])
    selected = select_correlated_features_train_only(X_train, y_train, fraction=0.25)
    assert selected == ["signal"]


def test_apply_feature_list_preserves_order():
    X = pd.DataFrame({"b": [1], "a": [2], "c": [3]})
    out = apply_feature_list(X, ["a", "c"])
    assert list(out.columns) == ["a", "c"]
