# Benchmark v2

AI-assisted methodological development of the original V1 workflow into a leakage-safe, multi-seed benchmark.

## Design

- ANSUR II revision pinned by commit.
- 70/30 stratified real split.
- Train-only Age_Group feature selection.
- CTGAN and ctdGAN: matched headline architecture, 150 epochs, batch size 100.
- LR/SVM scaled; LR `max_iter=5000`.
- Dummy, XGBoost, Random Forest, Logistic Regression and SVM downstream baselines.
- Five seeds: 11, 23, 37, 53, 71.
- Metrics: SDMetrics quality, standardised Wasserstein distance, exact duplicates, TRTR/TSTR accuracy, balanced accuracy, macro-F1 and macro-AUC.

## Result

GitHub Actions [run #3](https://github.com/trungnb/ANSUR-II-CTGAN-Benchmark/actions/runs/36395443027): **15/15 matrix jobs + aggregate succeeded**.

| Target | CTGAN F1 | ctdGAN F1 | CTGAN quality | ctdGAN quality |
|---|---:|---:|---:|---:|
| Gender | 0.855 | **0.942** | 79.61% | **90.42%** |
| Age group | 0.192 | **0.226** | 87.77% | **92.28%** |
| DODRace | 0.108 | **0.209** | 82.34% | **91.07%** |

Reviewed values and realised synthetic counts: [results/summary.csv](results/summary.csv).

## Run

```bash
cd benchmark_v2
python -m pip install -e '.[dev]'
pytest -q
python run_benchmark.py --config config.json --output-dir results
```

V1 and V2 are different designs. Exact duplicates are a sanity check, not a privacy guarantee. DODRace is retained only as a technical stress test.
