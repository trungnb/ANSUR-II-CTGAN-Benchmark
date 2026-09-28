"""Pinned ANSUR II loading and target preparation for benchmark v2."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

ANSUR_REPO_COMMIT = "da756f4cf2561eb049459232f5fe376f214f8c0a"
FEMALE_BLOB_SHA = "11aa789be390f5575a9ebc3f6a399da586ef3a1a"
MALE_BLOB_SHA = "6010f0431a657a6f444e3e0b8b9d91cbd76ee21e"
BASE_RAW = f"https://raw.githubusercontent.com/senihberkay/US-Army-ANSUR-II/{ANSUR_REPO_COMMIT}"
FEMALE_URL = f"{BASE_RAW}/ANSUR%20II%20FEMALE%20Public.csv"
MALE_URL = f"{BASE_RAW}/ANSUR%20II%20MALE%20Public.csv"
EXPECTED_ROWS = 6068

COMMON_ADMIN = [
    "Date",
    "Installation",
    "Component",
    "Branch",
    "PrimaryMOS",
    "SubjectsBirthLocation",
    "SubjectNumericRace",
    "Ethnicity",
    "Heightin",
    "Weightlbs",
    "WritingPreference",
]

AGE_LABELS = ["10-19", "20-29", "30-39", "40-49", "50-59"]
AGE_BINS = [10, 19, 29, 39, 49, 59]


@dataclass(frozen=True)
class TargetFrame:
    data: pd.DataFrame
    target: str
    discrete_columns: tuple[str, ...]


def _read_csv(url: str, cache_path: Path | None = None) -> pd.DataFrame:
    if cache_path is not None and cache_path.exists():
        return pd.read_csv(cache_path, encoding="latin1")
    df = pd.read_csv(url, encoding="latin1")
    if cache_path is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cache_path, index=False)
    return df


def load_ansur(cache_dir: str | Path | None = None) -> pd.DataFrame:
    """Load ANSUR II from immutable commit-pinned URLs.

    Git blob SHAs are documented above so the source files can be independently
    verified against the selected upstream commit.
    """
    cache = Path(cache_dir) if cache_dir is not None else None
    female = _read_csv(FEMALE_URL, cache / "female.csv" if cache else None)
    male = _read_csv(MALE_URL, cache / "male.csv" if cache else None)
    male = male.rename(columns={"subjectid": "SubjectId"})

    if list(female.columns) != list(male.columns):
        raise ValueError("Male and female ANSUR tables do not have identical columns.")

    df = pd.concat([female, male], ignore_index=True)
    if len(df) != EXPECTED_ROWS:
        raise ValueError(f"Expected {EXPECTED_ROWS} ANSUR rows, found {len(df)}.")
    if df["SubjectId"].duplicated().any():
        raise ValueError("SubjectId is not unique in the combined ANSUR table.")
    return df.set_index("SubjectId")


def prepare_target_frame(df: pd.DataFrame, target: str) -> TargetFrame:
    """Prepare a target-specific table without any train/test-dependent transforms."""
    target = str(target)
    work = df.copy()

    if target == "Gender":
        drop = COMMON_ADMIN + ["DODRace", "Age"]
        work = work.drop(columns=drop)
        return TargetFrame(work, target, (target,))

    if target == "Age_Group":
        drop = COMMON_ADMIN + ["DODRace", "Gender"]
        work = work.drop(columns=drop)
        work[target] = pd.cut(
            work["Age"], bins=AGE_BINS, labels=AGE_LABELS, right=True, include_lowest=True
        )
        if work[target].isna().any():
            bad = work.loc[work[target].isna(), "Age"].unique().tolist()
            raise ValueError(f"Age values outside predefined bins: {bad}")
        work = work.drop(columns=["Age"])
        work[target] = work[target].astype(str)
        return TargetFrame(work, target, (target,))

    if target == "DODRace":
        drop = COMMON_ADMIN + ["Age", "Gender"]
        work = work.drop(columns=drop)
        work[target] = work[target].astype(str)
        return TargetFrame(work, target, (target,))

    raise ValueError(f"Unsupported target: {target}")
