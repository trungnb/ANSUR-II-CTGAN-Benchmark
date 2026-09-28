# Viewing and chart rendering

GitHub can display the README, figures, CSV tables, and notebooks without installation.
The committed `pyproject.toml` and `uv.lock` describe a **portfolio tools environment**:
Matplotlib for plotting existing result tables; optional JupyterLab for viewing code.
They do not recreate the original Colab analysis environment.

```bash
uv sync --locked
uv run --locked python scripts/render_figures.py
# Optional interactive notebook viewer; do not select Run All to merely read notebooks:
uv run --locked --extra notebooks jupyter lab notebooks/
```

`requirements.txt` is the original, incomplete, unpinned dependency list retained
for historical context. Exact analysis package versions and hardware are unverified.
Notebook installation cells and Google Drive paths are preserved as originally written.
Executing the research notebooks requires their data, dependencies, and appropriate
compute resources. No segmentation, synthesis, model evaluation, or reproduction run
was performed for this release. Only existing results were extracted and plotted.
