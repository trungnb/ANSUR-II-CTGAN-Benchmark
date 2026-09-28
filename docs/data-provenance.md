# Provenance of this portfolio release

Packaged on 2026-09-28 from the author's existing project notebooks and result files.
No segmentation, synthesis, model training, evaluation, or reproduction run was performed.

## Notebooks
[notebook-provenance.json](notebook-provenance.json) records SHA-256 fingerprints of
the original and published notebook files. Original analysis cell sources and their
order are unchanged. No heading cell was inserted, so zero-based source references
still match. Publication clears session metadata, widget state and output previews.
Only aggregate CTGAN reporting cells retain their stream outputs. Original notebooks
remain in an ignored `.local-originals/` directory on the author's machine.

## Result tables
The CTGAN tables and report excerpts were extracted from existing notebook outputs.
Each row records its source notebook; detailed tables record zero-based source cells.
CSV serialization does not add precision beyond the saved reports. Excerpt line endings and trailing whitespace are normalized; report text and values are preserved.

See [the result index](../results/README.md) and [table fingerprints](result-sources.json).
Original CSV / notebook files do not establish the exact historical data version,
execution date, hardware or analysis package versions; those details remain unverified.

## Figures
`scripts/render_figures.py` reads the published CSVs and renders PNG and SVG figures.
It performs chart formatting and display-unit conversion only; it does not import
segmentation or generative-model libraries. The Python lockfile covers these portfolio
tools. Figure sources are documented in the result index and figure captions.

## Publication scope
Raw CT images, segmentation masks, raw ANSUR II rows, generated synthetic rows,
unrelated notebooks, and local backups are excluded. Code links to external packages
and datasets do not transfer their licenses. See [LICENSE](../LICENSE).
