# ADR-0002 — Add a separate reproducible benchmark v2

Status: ACCEPTED

## Context

The historical notebooks are valuable provenance but contain design limitations that should not
be silently edited away: Age-group feature selection used the full dataset before splitting;
CTGAN and ctdGAN were run under materially different settings; some downstream Logistic
Regression fits did not converge; and generator results came from single runs.

On 2026-09-28 the owner explicitly approved proceeding with a corrected research-grade v2.

## Decision

Preserve all historical notebooks and saved outputs unchanged. Add a separate `benchmark_v2/`
pipeline that performs leakage-safe preprocessing, matched generator settings, fixed downstream
pipelines, dummy baselines and multi-seed evaluation. V2 outputs must live separately from
historical outputs and must not be described as a reproduction until they have actually run.

## Consequences

- Historical provenance remains intact.
- New results can be interpreted under a controlled design.
- The repository temporarily contains two scopes: historical portfolio evidence and a new
  reproducible benchmark pipeline.
- Repository renaming is deferred until the v2 pull request is merged to avoid breaking links
  during implementation.

## Supersedes / Superseded by

Extends ADR-0001; does not supersede it.
