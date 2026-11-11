"""Group-fairness metrics for a binary 'flag' decision (1 = flagged as suspected fraud).

The adverse outcome for a genuine customer is being flagged (account hold, extra
verification, declined onboarding). Therefore the false-positive rate (FPR) is the
primary harm metric; the true-positive rate (TPR) captures whether protection is
equally effective across groups.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def _safe_div(a: float, b: float) -> float:
    return float(a) / float(b) if b else float("nan")


def confusion_rates(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    y_true = np.asarray(y_true).astype(int)
    y_pred = np.asarray(y_pred).astype(int)
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    return {
        "n": len(y_true),
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "base_rate": _safe_div(tp + fn, len(y_true)),
        "flag_rate": _safe_div(tp + fp, len(y_true)),
        "tpr": _safe_div(tp, tp + fn),
        "fpr": _safe_div(fp, fp + tn),
        "precision": _safe_div(tp, tp + fp),
    }


def group_table(df: pd.DataFrame, group_col: str, y_true: str = "true_fraud", y_pred: str = "flag") -> pd.DataFrame:
    rows = []
    for g, sub in df.groupby(group_col, sort=True):
        r = confusion_rates(sub[y_true].values, sub[y_pred].values)
        r[group_col] = g
        rows.append(r)
    out = pd.DataFrame(rows).set_index(group_col)
    return out


def disparity_summary(table: pd.DataFrame, reference: str) -> pd.DataFrame:
    """Compare every group with a reference group.

    statistical_parity_diff : flag_rate(g) - flag_rate(ref)
    disparate_impact_ratio  : flag_rate(g) / flag_rate(ref)   (selection-rate ratio)
    fpr_ratio / fpr_diff    : predictive-equality gap (harm to genuine customers)
    tpr_diff                : equal-opportunity gap (protection effectiveness)
    equalized_odds_gap      : max(|TPR diff|, |FPR diff|)
    """
    ref = table.loc[reference]
    rows = []
    for g, r in table.iterrows():
        rows.append(
            {
                "group": g,
                "reference": reference,
                "statistical_parity_diff": r["flag_rate"] - ref["flag_rate"],
                "disparate_impact_ratio": _safe_div(r["flag_rate"], ref["flag_rate"]),
                "fpr_diff": r["fpr"] - ref["fpr"],
                "fpr_ratio": _safe_div(r["fpr"], ref["fpr"]),
                "tpr_diff": r["tpr"] - ref["tpr"],
                "equalized_odds_gap": max(abs(r["tpr"] - ref["tpr"]), abs(r["fpr"] - ref["fpr"])),
            }
        )
    return pd.DataFrame(rows).set_index("group")


def bootstrap_ci(df: pd.DataFrame, group_col: str, stat: str, n_boot: int, seed: int,
                 y_true: str = "true_fraud", y_pred: str = "flag", alpha: float = 0.05) -> pd.DataFrame:
    """Percentile bootstrap CI (resampling rows) for a per-group statistic."""
    rng = np.random.default_rng(seed)
    groups = sorted(df[group_col].unique())
    store = {g: [] for g in groups}
    arrays = {g: (sub[y_true].values, sub[y_pred].values) for g, sub in df.groupby(group_col)}
    for g, (yt, yp) in arrays.items():
        n = len(yt)
        for _ in range(n_boot):
            idx = rng.integers(0, n, n)
            store[g].append(confusion_rates(yt[idx], yp[idx])[stat])
    rows = []
    for g in groups:
        vals = np.array(store[g], dtype=float)
        vals = vals[~np.isnan(vals)]
        rows.append({group_col: g, f"{stat}_lo": np.percentile(vals, 100 * alpha / 2),
                     f"{stat}_hi": np.percentile(vals, 100 * (1 - alpha / 2))})
    return pd.DataFrame(rows).set_index(group_col)
