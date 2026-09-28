# Architecture

`notebooks/` preserves historical analysis cell sources and order. Publication removes
session metadata and row-level previews; selected aggregate reports remain.
`results/` contains explicitly selected saved tables and figures derived from them.
`scripts/render_figures.py` reads these tables only. `docs/` records methods and provenance.
`data/README.md` explains input access; raw inputs remain outside version control.
`.local-originals/` is an ignored local backup. The publication allowlist is `.gitignore`.
The Python lockfile covers presentation tools, not the historical analysis runtime.
