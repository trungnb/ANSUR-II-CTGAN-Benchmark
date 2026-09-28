import pandas as pd

from src.evaluation import exact_duplicate_rate, make_metadata


def test_exact_duplicate_rate():
    real = pd.DataFrame({"x": [1, 2], "target": ["a", "b"]})
    synth = pd.DataFrame({"x": [1, 3], "target": ["a", "b"]})
    assert exact_duplicate_rate(real, synth) == 0.5


def test_metadata_marks_target_categorical():
    frame = pd.DataFrame({"x": [1.0], "target": ["a"]})
    metadata = make_metadata(frame, "target")
    assert metadata["columns"]["x"]["sdtype"] == "numerical"
    assert metadata["columns"]["target"]["sdtype"] == "categorical"
