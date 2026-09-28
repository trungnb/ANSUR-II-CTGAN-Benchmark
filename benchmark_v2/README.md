# Benchmark v2 — AI-assisted methodological development

This directory contains the second phase of the project. It does **not** overwrite or
retroactively correct the historical V1 notebooks in `../notebooks/`.

## Development model

V2 was developed with AI assistance for methodological audit, code inspection, refactoring,
test design, CI orchestration and reproducibility checks. The research question, original V1
experiments, methodological decisions and interpretation remain under the author's review.

The purpose of V2 is to turn the exploratory V1 workflow into a more reproducible benchmark,
not to relabel the original experiments as AI-generated work.

## Why v2 exists

The V1 prototype established the workflow but had several limitations:

- Age-group feature selection occurred before the train/holdout split;
- CTGAN and ctdGAN used materially different training settings;
- Logistic Regression emitted convergence warnings;
- LR/SVM were evaluated without explicit scaling;
- each generator was represented by one stochastic run;
- the custom percentage "trust score" had no calibrated interpretation.

V2 addresses these issues with train-only feature selection, matched headline architecture
and training budget, scaled LR/SVM pipelines, a dummy baseline, five pre-specified seeds,
pinned input provenance and an untouched real holdout.

## Completed run

The first complete successful benchmark is GitHub Actions
[run #3](https://github.com/trungnb/Medical-CTGAN-Synthesis/actions/runs/36395443027).

- 15/15 target-seed jobs: success
- aggregate job: success
- targets: Gender, Age_Group, DODRace
- generators: CTGAN, ctdGAN
- seeds: 11, 23, 37, 53, 71

### Headline results

| Generator | Target | SDMetrics mean | TSTR macro-F1 range* |
|---|---|---:|---:|
| ctdGAN | Gender | 90.42% | 0.8981–0.9690 |
| CTGAN | Gender | 79.61% | 0.8441–0.8648 |
| ctdGAN | Age_Group | 92.28% | 0.2126–0.2334 |
| CTGAN | Age_Group | 87.77% | 0.1820–0.2048 |
| ctdGAN | DODRace | 91.07% | 0.1855–0.2251 |
| CTGAN | DODRace | 82.34% | 0.1019–0.1147 |

*Range of the five-seed mean macro-F1 values across the four downstream models.

Published summaries are in [`results/`](results/).

## What changed relative to V1

The controlled redesign reduces the apparent CTGAN–ctdGAN gap for Gender: CTGAN improves
substantially when given the same training budget and corrected downstream preprocessing.
ctdGAN nevertheless retains higher mean quality and TSTR utility across all three targets.

Age_Group remains a difficult downstream task even with real training data, so low absolute
TSTR scores should not be interpreted in isolation. DODRace shows why statistical fidelity
and predictive utility must be evaluated separately.

## Data provenance

ANSUR II is loaded from commit
`da756f4cf2561eb049459232f5fe376f214f8c0a` rather than a mutable branch. Git blob IDs
are recorded in `src/data.py`. The combined dataset contains 6,068 rows.

## Run locally

```bash
cd benchmark_v2
python -m pip install -e '.[dev]'
pytest
python run_benchmark.py --config config.json --output-dir results
```

## Interpretation and limitations

1. SDMetrics quality describes statistical similarity; it does not establish privacy.
2. Exact duplicate rate is a sanity check, not a privacy guarantee.
3. DODRace is retained only as a dataset-inherited technical stress test.
4. V1 and V2 results come from different designs and should not be pooled.
5. The intended synthetic sampling policy was aligned, but ARTSyn ctdGAN returned slightly
   fewer than the requested rows for some multiclass seeds; realised counts are published.
6. Confidence intervals are descriptive across five seeds, not evidence of external validity.
