# Reproducible benchmark v2

This directory contains a **new analysis pipeline**. It does not alter or retrospectively
correct the historical notebooks in `../notebooks/` or their saved outputs.

## Why v2 exists

The historical prototype established the workflow but has four limitations that prevent a
controlled generator comparison: Age-group feature selection occurred before the split;
CTGAN and ctdGAN used different epoch/sample settings; downstream Logistic Regression emitted
non-convergence warnings; and each generator was represented by a single stochastic run.

V2 addresses those issues by:

- splitting before all target-dependent feature selection;
- using the same headline architecture, 150 epochs, batch size, synthetic class counts and
  real train/test split for CTGAN and ctdGAN;
- scaling Logistic Regression and SVM while leaving tree models unscaled;
- adding a most-frequent dummy baseline;
- repeating each target across five pre-specified seeds;
- keeping the real test partition untouched by generator fitting, feature selection and
  downstream training;
- reporting SDMetrics quality, raw standardised Wasserstein distance, exact duplicate rate,
  and TRTR/TSTR utility without converting distances into an unvalidated percentage "trust" score.

## Data provenance

The source mirror is pinned to commit
`da756f4cf2561eb049459232f5fe376f214f8c0a` rather than a mutable branch.
Git blob identifiers are recorded in `src/data.py`. The benchmark expects 6,068 combined rows.
This remains an anthropometric dataset, not a clinical patient cohort.

## Run

```bash
cd benchmark_v2
python -m pip install -e '.[dev]'
pytest
python run_benchmark.py --config config.json --output-dir results
```

The default full run fits 2 generators × 3 targets × 5 seeds and can be computationally
expensive. Results are deliberately not committed until a complete run and review have been
performed.

## Interpretation rules

1. Generator comparisons are descriptive unless uncertainty across seeds is reported.
2. SDMetrics quality measures statistical similarity; it does not establish privacy.
3. Exact duplicate rate is only a basic memorisation check, not a privacy guarantee.
4. DODRace is retained solely as a dataset-inherited technical stress test; results must not be
   interpreted as biological or clinical claims about race.
5. Historical notebook results and v2 results must never be pooled as if they came from one design.
