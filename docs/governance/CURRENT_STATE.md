# Current state

Updated: 2026-09-28.

The repository has two intentionally separate layers.

1. **V1 — original exploratory experiments:** the author's historical notebooks, saved
   aggregate results, figures and provenance remain unchanged. These are the original
   exploratory experiments and are not retrospectively rewritten as AI-generated work.
2. **V2 — AI-assisted methodological development:** a leakage-safe, multi-seed benchmark
   lives under `benchmark_v2/`. AI assistance was used for audit, code inspection,
   refactoring, CI orchestration and reproducibility checks; methodological decisions and
   interpretation remain under author review.

Benchmark v2 has now been fully executed. GitHub Actions run #3 completed with 15/15 matrix
jobs and the aggregate job successful. Reviewed headline summaries and workflow provenance
are committed under `benchmark_v2/results/`.

V2 confirms higher mean quality and TSTR utility for ctdGAN than CTGAN across the three
targets, while substantially reducing the apparent Gender gap seen in V1. Historical V1 and
V2 results remain separate because they come from different experimental designs.

Known V2 limitation: realised ARTSyn ctdGAN synthetic row counts were slightly below the
requested count in some multiclass seeds, so V2 is a methodological development benchmark
rather than a claim of perfectly matched output size.
