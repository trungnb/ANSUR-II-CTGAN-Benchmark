# Portfolio packaging checks

2026-09-28.

Local Markdown targets were checked against the files selected for Git. Notebook analysis cell sources and order were compared with local originals; hashes are recorded in the provenance manifest. Raw image formats, row-level input data, unrelated notebooks and local backups are excluded from Git. Selected public text was checked for common credential patterns.

No listed direct-identifier pattern was found in selected public text and tables. Pattern scans do not establish de-identification or rule out indirect identifiers. Public notebooks were scanned as JSON as well as structurally inspected.

Figures were rendered from saved tables and visually inspected. The chart scripts passed Ruff checks. No research notebook, segmentation, training, scientific validation or reproducibility audit was run. These checks concern the publication package only.
