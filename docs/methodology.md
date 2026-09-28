# Methods represented in the notebooks

## Data preparation
The code reads the female and male ANSUR II public CSVs from a GitHub mirror, concatenates
them, uses `SubjectId` as an index, and drops selected demographic / administrative
fields according to the target. Saved outputs record 6,068 rows. Gender and DODRace
experiments retain anthropometric features with their target; age experiments bin Age
into five groups and retain the 23 features with the largest absolute correlations
with encoded Age_Group (23 of 93). This selection occurs before the split in the notebooks.

Each notebook uses a stratified split with `test_size=0.7` and `random_state=42`:
1,820 training records and 4,248 real holdout records. Source code and ordering remain intact.

## Generator settings

| Generator | Targets | Epochs in code | Requested synthetic rows |
|---|---|---:|---:|
| CTGAN | Gender / DODRace | 10 | 10,000 |
| CTGAN | Age_Group | 10 | 20,000 |
| ctdGAN | Gender | 150 | 5,000 per class; 10,000 total |
| ctdGAN | Age_Group | 150 | 5,000 per class; 25,000 total |

The ctdGAN implementation is imported from `artsyn.generators.ctd_gan`. Its configured
settings include generator / discriminator layers `(256, 256)`, batch size 100,
embedding dimension 128, `pac=10`, `max_clusters=10`, k-means clustering,
`scaler='mms11'`, `sampling_strategy='create-new'`, and `random_state=42`.
The CTGAN notebooks instantiate `CTGAN(epochs=10)`.

## Saved evaluation outputs
- **SDMetrics QualityReport:** column shapes and column-pair trends, summarized by the saved overall percentage.
- **Custom distribution score:** combines transformed Wasserstein and MMD quantities. It is labeled separately from SDMetrics in `fidelity.csv`. Historical text calls it a “trust score”; no privacy or clinical validity is inferred from that label.
- **Downstream utility:** XGBoost, Random Forest, Logistic Regression and SVM. Each is trained on real data (TRTR) and synthetic data (TSTR), with real holdout evaluation. Saved metrics include accuracy, macro-F1 and AUC.

## Presentation and scope
Tables were parsed from saved reports, respecting each report's column order; ctdGAN's
age report orders columns differently from the other reports. Full aggregate output
excerpts, including warnings, are retained under `results/saved-output-excerpts/`.
The README macro-F1 ranges are minima / maxima across four classifiers, not uncertainty intervals.
The SDMetrics bar chart and macro-F1 heatmap share the same experiment row order.

These are descriptive runs with differing generator configurations. No training or
evaluation was repeated for this release. Privacy evaluation, clinical deployment,
external validation, and controlled benchmark comparisons are outside this prototype.
