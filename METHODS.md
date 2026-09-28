# Methods and provenance

## Data

Both phases use the public ANSUR II anthropometric tables: 4,082 male and 1,986 female records (6,068 total). No raw rows or synthetic row-level tables are committed.

V1 notebooks reference a GitHub mirror through its mutable `master` branch, so the exact historical input revision is unknown. V2 pins the mirror to commit `da756f4cf2561eb049459232f5fe376f214f8c0a`; source blob IDs are recorded in `benchmark_v2/src/data.py`.

Targets are **Gender**, **Age_Group** and **DODRace**. DODRace is included only as a dataset-inherited technical stress test, not as a biological or clinical inference task.

## V1 — original exploratory experiments

The five notebooks are preserved as historical analysis artifacts.

- Stratified split: `test_size=0.7`, `random_state=42` → 1,820 train / 4,248 holdout.
- Age_Group: Age binned into five groups; 23/93 anthropometric features selected by absolute correlation **before** the split.
- CTGAN: 10 epochs; 10,000 synthetic rows for Gender/DODRace and 20,000 for Age_Group.
- ctdGAN: 150 epochs; 5,000 requested rows per class.
- Downstream models: XGBoost, Random Forest, Logistic Regression and SVM.
- Evaluation: SDMetrics QualityReport, a historical custom Wasserstein/MMD score, and TRTR/TSTR accuracy, macro-F1 and AUC.

Known V1 limitations: feature-selection leakage in Age_Group, unequal generator training settings, unscaled LR/SVM, Logistic Regression convergence warnings and single-run stochastic estimates. V1 results are therefore descriptive.

## V2 — AI-assisted methodological development

AI assistance was used for methodological audit, code inspection, refactoring, test design and CI orchestration. The original V1 experiments and the project interpretation remain the author's work and review.

V2 uses:

- split before target-dependent feature selection;
- 70/30 stratified real train/test split;
- matched headline CTGAN/ctdGAN architecture and 150-epoch budget;
- StandardScaler for Logistic Regression and SVM;
- Logistic Regression `max_iter=5000`;
- most-frequent dummy baseline;
- seeds 11, 23, 37, 53 and 71;
- untouched real holdout for TRTR/TSTR;
- SDMetrics quality, standardised Wasserstein distance and exact-duplicate rate.

The complete successful benchmark is GitHub Actions run #3 (15 target-seed jobs + aggregate).

### V2 interpretation

Across all three targets, ctdGAN has higher mean SDMetrics quality and mean TSTR macro-F1 than CTGAN. CTGAN improves markedly for Gender relative to V1, showing that the historical gap was partly design-dependent.

Age_Group remains difficult even under real-data training, so low absolute TSTR performance is not synthesis failure alone. DODRace provides the clearest example that distributional similarity and downstream predictive utility are distinct properties.

### Limitations

V1 and V2 use different designs and should not be pooled. ARTSyn ctdGAN returned slightly fewer than the requested rows for some multiclass seeds; realised counts are reported in `benchmark_v2/results/summary.csv`. Exact duplicate rate was zero in V2 but does not establish privacy. Five-seed confidence intervals are descriptive and do not establish external validity.
