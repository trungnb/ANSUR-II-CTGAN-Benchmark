"""Generator adapters with matched headline settings for benchmark v2."""

from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np
import pandas as pd


def set_global_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass


@dataclass(frozen=True)
class GeneratorSettings:
    epochs: int = 150
    batch_size: int = 100
    embedding_dim: int = 128
    generator_dim: tuple[int, int] = (256, 256)
    discriminator_dim: tuple[int, int] = (256, 256)
    pac: int = 10


def fit_sample_ctgan(
    train: pd.DataFrame,
    target: str,
    n_per_class: int,
    seed: int,
    settings: GeneratorSettings,
) -> pd.DataFrame:
    """Fit CTGAN and obtain an exactly class-balanced synthetic table."""
    from ctgan import CTGAN

    set_global_seed(seed)
    model = CTGAN(
        epochs=settings.epochs,
        batch_size=settings.batch_size,
        embedding_dim=settings.embedding_dim,
        generator_dim=settings.generator_dim,
        discriminator_dim=settings.discriminator_dim,
        pac=settings.pac,
        verbose=False,
        enable_gpu=True,
    )
    model.fit(train, discrete_columns=[target])

    pieces: list[pd.DataFrame] = []
    for value in sorted(train[target].astype(str).unique().tolist()):
        accepted: list[pd.DataFrame] = []
        remaining = n_per_class
        attempts = 0
        while remaining > 0 and attempts < 30:
            attempts += 1
            # Keep a large conditioned batch even when only a few rows remain.
            # Rare categories can otherwise stall when the request shrinks to a
            # tiny batch and CTGAN returns a handful of label mismatches.
            request_n = max(settings.batch_size, n_per_class * 2)
            sample = model.sample(
                request_n, condition_column=target, condition_value=value
            )
            sample[target] = sample[target].astype(str)
            matched = sample.loc[sample[target] == value]
            if not matched.empty:
                take = matched.head(remaining)
                accepted.append(take)
                remaining -= len(take)
        if remaining > 0:
            raise RuntimeError(
                f"CTGAN could not obtain {n_per_class} rows for class {value}; "
                f"{remaining} rows remain after rejection sampling."
            )
        pieces.append(pd.concat(accepted, ignore_index=True))

    return pd.concat(pieces, ignore_index=True)[train.columns]


def fit_sample_ctdgan(
    train: pd.DataFrame,
    target: str,
    n_per_class: int,
    seed: int,
    settings: GeneratorSettings,
) -> pd.DataFrame:
    """Fit ARTSyn ctdGAN and sample the same number of rows per class as CTGAN."""
    from artsyn.generators import ctd_gan
    from sklearn.preprocessing import LabelEncoder

    set_global_seed(seed)
    X = train.drop(columns=[target])
    encoder = LabelEncoder()
    y = encoder.fit_transform(train[target].astype(str))

    model = ctd_gan.ctdGAN(
        discriminator=settings.discriminator_dim,
        generator=settings.generator_dim,
        epochs=settings.epochs,
        batch_size=settings.batch_size,
        pac=settings.pac,
        embedding_dim=settings.embedding_dim,
        max_clusters=10,
        cluster_method="kmeans",
        scaler="mms11",
        sampling_strategy="create-new",
        random_state=seed,
    )
    model.fit(X.to_numpy(), y)

    pieces: list[pd.DataFrame] = []
    for encoded, label in enumerate(encoder.classes_):
        sampled = model.sample(n_per_class, encoded)
        block = pd.DataFrame(sampled, columns=X.columns)
        block[target] = str(label)
        pieces.append(block)
    return pd.concat(pieces, ignore_index=True)[train.columns]
