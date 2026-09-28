# Saved results and figures

| File | Contents |
|---|---|
| [fidelity.csv](fidelity.csv) | Saved SDMetrics percentage and separately labeled custom score, with source notebook and cell index |
| [downstream_metrics.csv](downstream_metrics.csv) | Twenty rows: four classifiers for each of five experiments; saved TRTR / TSTR accuracy, macro-F1 and AUC |
| [experiment_summary.csv](experiment_summary.csv) | Five experiment summaries; descriptive macro-F1 ranges |
| [Output excerpts](saved-output-excerpts/) | Original text from aggregate report cells, including warnings |
| [Overview PNG](figures/prototype-overview.png) / [SVG](figures/prototype-overview.svg) | SDMetrics bars and TSTR macro-F1 heatmap |
| [Baseline comparison PNG](figures/downstream-baselines.png) / [SVG](figures/downstream-baselines.svg) | TSTR macro-F1 with each run's saved TRTR baseline |

`*_Real` denotes real training / real holdout evaluation. `*_Synth` denotes synthetic
training / real holdout evaluation. `F1_*` is macro-F1. Cell references are zero-based.
The original notebook reports are the numerical source; displayed decimal precision
is preserved in the CSV values. Charts add no newly fitted models or recomputed scores.
