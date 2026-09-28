# Benchmark v2 results

These files summarise the first complete successful **benchmark v2** run:

- GitHub Actions run: [benchmark-v2-full #3](https://github.com/trungnb/Medical-CTGAN-Synthesis/actions/runs/36395443027)
- 15/15 target-seed matrix jobs succeeded.
- Aggregate job succeeded.
- Five pre-specified seeds: 11, 23, 37, 53, 71.

## Published summaries

- [headline_results.csv](headline_results.csv): SDMetrics quality, TSTR macro-F1 summaries, realised synthetic row counts and exact-duplicate rate.
- [trtr_baseline.csv](trtr_baseline.csv): real-data TRTR macro-F1 reference.
- [run_manifest.json](run_manifest.json): workflow provenance.

The complete per-seed and per-metric CSVs remain available as the `benchmark-v2-combined`
artifact in run #3.

## Interpretation

Across the five-seed v2 benchmark, ctdGAN had higher mean SDMetrics quality and higher
mean TSTR macro-F1 than CTGAN for all three targets. The gap was smaller than in the
historical V1 experiments, especially for Gender, where CTGAN improved substantially
under the revised training design.

High statistical fidelity did not guarantee high downstream utility. DODRace is the
clearest example and is retained only as a dataset-inherited technical stress test.

## Important limitation

The intended synthetic sampling policy was aligned across generators, but ARTSyn ctdGAN
returned slightly fewer than the requested rows for some multiclass seeds. Realised
synthetic counts are therefore reported explicitly in `headline_results.csv`.
V2 should be read as an AI-assisted methodological development benchmark, not a claim of
perfectly matched generator output size.
