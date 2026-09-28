"""Render portfolio charts from saved CSV tables only. No notebook execution."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = RESULTS / "figures"
OUT.mkdir(exist_ok=True)
NAVY, TEAL, ORANGE = "#17324D", "#168B8A", "#D17845"
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.labelcolor": NAVY,
        "text.color": NAVY,
        "axes.titleweight": "bold",
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "svg.fonttype": "none",
    }
)


def rows(name):
    with (RESULTS / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save(fig, name, footer):
    fig.text(0.06, 0.018, footer, fontsize=8, color="#586777")
    fig.savefig(OUT / (name + ".png"), dpi=180, bbox_inches="tight")
    fig.savefig(OUT / (name + ".svg"), bbox_inches="tight")
    svg = OUT / (name + ".svg")
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
    plt.close(fig)


fidelity = rows("fidelity.csv")
metrics = rows("downstream_metrics.csv")
models = ["XGBoost", "Random Forest", "Logistic Regression", "SVM"]
labels = [
    r["generator"] + " / " + r["target"].replace("Age_Group", "Age group")
    for r in fidelity
]
matrix = [
    [
        next(
            float(m["F1_Synth"])
            for m in metrics
            if (m["generator"], m["target"], m["model"])
            == (r["generator"], r["target"], model)
        )
        for model in models
    ]
    for r in fidelity
]
fig, (a, b) = plt.subplots(
    1, 2, figsize=(13, 5.6), gridspec_kw={"width_ratios": [1, 1.6]}
)
fig.subplots_adjust(left=0.19, right=0.96, top=0.78, bottom=0.23, wspace=0.48)
fig.suptitle(
    "Synthetic tables: distribution fidelity and downstream utility",
    x=0.06,
    ha="left",
    y=0.97,
    fontsize=17,
    fontweight="bold",
)
fig.text(
    0.06,
    0.89,
    "Five exploratory runs on ANSUR II • values extracted from saved notebook reports",
    fontsize=11,
    color="#586777",
)
scores = [float(r["sdmetrics_percent"]) for r in fidelity]
a.barh(
    range(5),
    scores,
    color=[TEAL if r["generator"] == "ctdGAN" else NAVY for r in fidelity],
    height=0.56,
)
for i, v in enumerate(scores):
    a.text(v + 1, i, f"{v:.2f}", va="center", fontsize=9)
a.set(
    yticks=range(5),
    yticklabels=labels,
    xlim=(0, 113),
    xlabel="SDMetrics quality score (%)",
)
a.invert_yaxis()
a.set_title("A  Distribution fidelity", loc="left", pad=14)
a.grid(axis="x", alpha=0.12)
im = b.imshow(matrix, vmin=0, vmax=1, cmap="YlGnBu", aspect="auto")
for i, row in enumerate(matrix):
    for j, v in enumerate(row):
        b.text(
            j,
            i,
            f"{v:.3f}",
            ha="center",
            va="center",
            color="white" if v > 0.55 else NAVY,
            fontsize=11,
        )
b.set(
    xticks=range(4),
    xticklabels=["XGBoost", "Random\nForest", "Logistic\nRegression", "SVM"],
    yticks=range(5),
    yticklabels=[],
)
b.tick_params(axis="both", length=0)
b.set_title("B  Train synthetic, test real: macro-F1", loc="left", pad=14)
fig.colorbar(im, ax=b, fraction=0.045, pad=0.025, ticks=[0, 0.5, 1])
save(
    fig,
    "prototype-overview",
    "Source: fidelity.csv and downstream_metrics.csv. Different generator settings; descriptive runs, not a controlled ranking or privacy assessment.",
)

fig, axes = plt.subplots(1, 3, figsize=(13.5, 5.3), sharey=True)
fig.subplots_adjust(left=0.07, right=0.98, top=0.75, bottom=0.23, wspace=0.28)
fig.suptitle(
    "Downstream utility against the real-data baseline",
    x=0.06,
    ha="left",
    y=0.97,
    fontsize=18,
    fontweight="bold",
)
fig.text(
    0.06,
    0.88,
    "Saved macro-F1 • same four downstream model types in each target experiment",
    fontsize=11,
    color="#586777",
)
for ax, target in zip(axes, ["Gender", "Age_Group", "DODRace"]):
    ax.set_title(target.replace("Age_Group", "Age group"), loc="left")
    for generator, color, offset in [("ctdGAN", TEAL, -0.08), ("CTGAN", ORANGE, 0.08)]:
        selected = [
            r for r in metrics if r["target"] == target and r["generator"] == generator
        ]
        if not selected:
            continue
        for j, model in enumerate(models):
            row = next(r for r in selected if r["model"] == model)
            real = float(row["F1_Real"])
            synth = float(row["F1_Synth"])
            ax.plot(
                [j + offset, j + offset], [real, synth], color=color, lw=1.5, alpha=0.65
            )
            ax.scatter(j + offset, real, color=color, marker="_", s=110)
            ax.scatter(
                j + offset,
                synth,
                color=color,
                s=40,
                label=generator + " TSTR" if j == 0 else None,
            )
    ax.set(xticks=range(4), xticklabels=["XGB", "RF", "LR", "SVM"], ylim=(0, 1.05))
    ax.grid(axis="y", alpha=0.15)
axes[0].set_ylabel("Macro-F1")
from matplotlib.lines import Line2D

fig.legend(
    handles=[
        Line2D([], [], marker="o", ls="", color=TEAL, label="ctdGAN TSTR"),
        Line2D([], [], marker="o", ls="", color=ORANGE, label="CTGAN TSTR"),
        Line2D(
            [], [], marker="_", ls="", color=NAVY, markersize=12, label="TRTR baseline"
        ),
    ],
    loc="upper right",
    bbox_to_anchor=(0.98, 0.87),
    ncol=3,
    frameon=False,
)
save(
    fig,
    "downstream-baselines",
    "Circles: train synthetic / test real. Horizontal ticks: train real / test real. XGB: XGBoost; RF: Random Forest; LR: Logistic Regression.",
)
