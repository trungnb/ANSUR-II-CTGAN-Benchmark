# ADR-0001 — Notebook portfolio with saved results

Status: ACCEPTED

## Context
On 2026-09-28 the owner approved three separate repositories, concise English READMEs,
flowcharts, saved results, and GitHub publication. The owner explicitly declined
reproduction runs and then requested charts drawn from saved result files.

## Decision
Preserve notebook analysis code. Publish selected saved results with provenance and
plots. Keep raw input data and original unsanitized notebook backups outside Git.

## Rationale
The deliverable is a readable account of existing experiments using available outputs.

## Allowed
Documentation, output extraction, chart rendering, publication cleanup and Git publication.

## Not allowed
Claiming rerun or clinical validation, altering analyses, or publishing raw input images.

## Consequences
The repository is readable without executing the computational experiments.
The presentation lockfile does not establish analysis reproducibility.

## Supersedes / Superseded by
None.
