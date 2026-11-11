"""Figures for the fairness evidence pack (matplotlib only)."""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import config

PALETTE = {"urban": "#1f4e79", "peri_urban": "#c58b00", "rural": "#a23b3b",
           "female": "#5b4b8a", "male": "#2e7d6b"}
plt.rcParams.update({"figure.dpi": 150, "axes.spines.top": False, "axes.spines.right": False,
                     "font.size": 10, "axes.titleweight": "bold"})


def _save(fig, name: str) -> None:
    config.FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(config.FIG_DIR / name, bbox_inches="tight")
    plt.close(fig)


def rates_by_group(region_tbl, region_ci_fpr, region_ci_flag, gender_tbl, gender_ci_fpr, gender_ci_flag) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, stat, title, ci_r, ci_g in (
        (axes[0], "flag_rate", "Flag rate (share of customers flagged)", region_ci_flag, gender_ci_flag),
        (axes[1], "fpr", "False-positive rate (genuine customers wrongly flagged)", region_ci_fpr, gender_ci_fpr),
    ):
        labels, vals, lo, hi, cols = [], [], [], [], []
        for tbl, ci in ((region_tbl, ci_r), (gender_tbl, ci_g)):
            for g in tbl.index:
                labels.append(g.replace("_", "-")); vals.append(tbl.loc[g, stat])
                lo.append(tbl.loc[g, stat] - ci.loc[g, f"{stat}_lo"]); hi.append(ci.loc[g, f"{stat}_hi"] - tbl.loc[g, stat])
                cols.append(PALETTE[g])
        x = np.arange(len(labels))
        ax.bar(x, vals, yerr=[lo, hi], color=cols, capsize=3)
        ax.set_xticks(x); ax.set_xticklabels(labels, rotation=20); ax.set_title(title, fontsize=10)
        ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
        ax.axvline(len(region_tbl) - 0.5, color="grey", ls=":", lw=1)
    fig.suptitle("Baseline model - outcomes by group (test set, 95% bootstrap CI)", fontweight="bold")
    _save(fig, "fig1_baseline_rates_by_group.png")


def importance(coefs: pd.DataFrame, perm: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    c = coefs.sort_values("std_coef")
    axes[0].barh(c["feature"], c["std_coef"], color=np.where(c["std_coef"] > 0, "#a23b3b", "#1f4e79"))
    axes[0].set_title("Standardised coefficients (log-odds of flag)")
    p = perm.sort_values("auc_drop_mean")
    axes[1].barh(p["feature"], p["auc_drop_mean"], xerr=p["auc_drop_sd"], color="#555555")
    axes[1].set_title("Permutation importance (AUC drop)")
    _save(fig, "fig2_feature_importance.png")


def local_review(contrib_case: pd.Series, contrib_mean_urban_genuine: pd.Series, case_id: str, prob: float) -> None:
    df = pd.DataFrame({"case": contrib_case, "typical_urban_genuine": contrib_mean_urban_genuine}).sort_values("case")
    fig, ax = plt.subplots(figsize=(8, 4))
    y = np.arange(len(df))
    ax.barh(y + 0.2, df["case"], height=0.4, color="#a23b3b", label=f"{case_id} (rural, genuine, flagged; p={prob:.2f})")
    ax.barh(y - 0.2, df["typical_urban_genuine"], height=0.4, color="#1f4e79", alpha=0.7, label="Average urban genuine customer")
    ax.set_yticks(y); ax.set_yticklabels(df.index); ax.axvline(0, color="black", lw=0.8)
    ax.set_xlabel("Contribution to log-odds of being flagged (relative to training mean)")
    ax.set_title("Decision review - why was this genuine customer flagged?", fontsize=10)
    ax.legend(fontsize=8, loc="lower right")
    _save(fig, "fig3_local_decision_review.png")


def mitigation(variants: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    order = list(variants.index)
    x = np.arange(len(order)); w = 0.38
    axes[0].bar(x - w / 2, variants["fpr_urban"], w, color=PALETTE["urban"], label="urban")
    axes[0].bar(x + w / 2, variants["fpr_rural"], w, color=PALETTE["rural"], label="rural")
    axes[0].set_xticks(x); axes[0].set_xticklabels(order, rotation=20, ha="right", fontsize=8)
    axes[0].yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0)); axes[0].legend()
    axes[0].set_title("False-positive rate: urban vs rural", fontsize=10)
    axes[1].bar(x - w / 2, variants["recall_overall"], w, color="#2e7d6b", label="overall recall (TPR)")
    axes[1].bar(x + w / 2, variants["precision_overall"], w, color="#777777", label="overall precision")
    axes[1].set_xticks(x); axes[1].set_xticklabels(order, rotation=20, ha="right", fontsize=8)
    axes[1].yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0)); axes[1].legend(fontsize=8)
    axes[1].set_title("Effectiveness cost of each control", fontsize=10)
    _save(fig, "fig4_mitigation_tradeoffs.png")
