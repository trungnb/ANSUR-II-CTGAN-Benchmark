# Current state

Updated: 2026-09-28.

The repository now has two intentionally separate layers.

1. **Historical portfolio:** the original exploratory notebooks, saved aggregate results,
   figures and provenance remain unchanged. No historical result has been rerun.
2. **Benchmark v2:** a new leakage-safe, multi-seed analysis pipeline lives under
   `benchmark_v2/`. It pins the ANSUR mirror revision, standardises scale-sensitive
   downstream models, adds a dummy baseline, matches headline generator settings and keeps
   target-dependent feature selection inside the training partition.

Benchmark v2 code and unit tests are implemented, but the full GAN benchmark has not yet
been executed and no v2 scientific result is claimed. Historical and v2 outputs must remain
separate.
