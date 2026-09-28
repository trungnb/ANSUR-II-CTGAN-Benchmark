# This recipe only plots saved CSV values; it does not run the research notebooks.
figures:
    uv run --locked python scripts/render_figures.py

notebooks:
    uv run --locked --extra notebooks jupyter lab notebooks/
