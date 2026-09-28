"""Run the leakage-free synthetic tabular benchmark.

This is a new v2 analysis. It does not reproduce or overwrite historical notebook results.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from src.data import load_ansur, prepare_target_frame
from src.downstream import build_models
from src.evaluation import (
    evaluate_classifier,
    exact_duplicate_rate,
    sdmetrics_quality,
    standardised_wasserstein_mean,
)
from src.features import apply_feature_list, select_correlated_features_train_only
from src.generators import GeneratorSettings, fit_sample_ctdgan, fit_sample_ctgan


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def split_target(frame: pd.DataFrame, target: str, test_size: float, seed: int):
    train, test = train_test_split(
        frame,
        test_size=test_size,
        random_state=seed,
        stratify=frame[target],
    )
    return train.copy(), test.copy()


def run(config: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    full = load_ansur(config.get("cache_dir"))
    utility_rows: list[dict] = []
    quality_rows: list[dict] = []

    settings = GeneratorSettings(**config["generator_settings"])

    for target in config["targets"]:
        target_frame = prepare_target_frame(full, target).data
        for seed in config["seeds"]:
            train, test = split_target(target_frame, target, config["test_size"], seed)

            X_train = train.drop(columns=[target])
            X_test = test.drop(columns=[target])
            y_train = train[target].astype(str)
            y_test = test[target].astype(str)

            selected_features = list(X_train.columns)
            if target == "Age_Group":
                selected_features = select_correlated_features_train_only(
                    X_train,
                    y_train,
                    fraction=config["age_feature_fraction"],
                )
                X_train = apply_feature_list(X_train, selected_features)
                X_test = apply_feature_list(X_test, selected_features)
                train = pd.concat([X_train, y_train.rename(target)], axis=1)

            for model_name, model in build_models(seed).items():
                metrics = evaluate_classifier(model, X_train, y_train, X_test, y_test)
                utility_rows.append(
                    {
                        "target": target,
                        "seed": seed,
                        "generator": "REAL",
                        "regime": "TRTR",
                        "model": model_name,
                        **metrics,
                    }
                )

            for generator_name, generator_fn in (
                ("CTGAN", fit_sample_ctgan),
                ("ctdGAN", fit_sample_ctdgan),
            ):
                synthetic = generator_fn(
                    train=train,
                    target=target,
                    n_per_class=config["synthetic_rows_per_class"],
                    seed=seed,
                    settings=settings,
                )
                synthetic[target] = synthetic[target].astype(str)
                X_synth = synthetic.drop(columns=[target])
                y_synth = synthetic[target]

                quality = sdmetrics_quality(train, synthetic, target)
                quality_rows.append(
                    {
                        "target": target,
                        "seed": seed,
                        "generator": generator_name,
                        "n_real_train": len(train),
                        "n_synthetic": len(synthetic),
                        "n_features": len(selected_features),
                        **quality,
                        "mean_standardised_wasserstein": standardised_wasserstein_mean(
                            train.drop(columns=[target]), X_synth
                        ),
                        "exact_duplicate_rate": exact_duplicate_rate(train, synthetic),
                    }
                )

                for model_name, model in build_models(seed).items():
                    metrics = evaluate_classifier(model, X_synth, y_synth, X_test, y_test)
                    utility_rows.append(
                        {
                            "target": target,
                            "seed": seed,
                            "generator": generator_name,
                            "regime": "TSTR",
                            "model": model_name,
                            **metrics,
                        }
                    )

    pd.DataFrame(utility_rows).to_csv(output_dir / "utility_by_seed.csv", index=False)
    pd.DataFrame(quality_rows).to_csv(output_dir / "quality_by_seed.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("config.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    args = parser.parse_args()
    run(load_config(args.config), args.output_dir)
