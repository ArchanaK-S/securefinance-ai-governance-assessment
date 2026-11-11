"""Model training and mitigation variants (all scikit-learn, fully deterministic)."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from . import config


def split(df: pd.DataFrame):
    strat = df["region_type"] + "_" + df["observed_label"].astype(str)
    train, test = train_test_split(df, test_size=config.TEST_SIZE, random_state=config.SEED, stratify=strat)
    return train.reset_index(drop=True), test.reset_index(drop=True)


def make_model() -> Pipeline:
    return Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(max_iter=2000, random_state=config.SEED))])


def fit(train: pd.DataFrame, features: list[str], sample_weight: np.ndarray | None = None) -> Pipeline:
    model = make_model()
    kwargs = {"clf__sample_weight": sample_weight} if sample_weight is not None else {}
    model.fit(train[features], train["observed_label"], **kwargs)
    return model


def reweighing_weights(train: pd.DataFrame, group_col: str = "region_type", label_col: str = "observed_label") -> np.ndarray:
    """Kamiran & Calders (2012) reweighing: w(g, y) = P(g) * P(y) / P(g, y)."""
    n = len(train)
    p_g = train[group_col].value_counts(normalize=True)
    p_y = train[label_col].value_counts(normalize=True)
    p_gy = train.groupby([group_col, label_col]).size() / n
    w = train.apply(lambda r: p_g[r[group_col]] * p_y[r[label_col]] / p_gy[(r[group_col], r[label_col])], axis=1)
    return w.values


def audit_calibrated_thresholds(train: pd.DataFrame, features: list[str], base_threshold: float,
                                reference_group: str = "urban", audit_frac: float = 0.30) -> dict:
    """Post-processing control: choose per-group thresholds on a small VERIFIED audit sample.

    A random `audit_frac` of the training population is assumed to have independently verified
    fraud outcomes (a recommended control - see docs). Each group's threshold is the lowest
    value whose audit-sample FPR is closest to the reference group's FPR at the base threshold.
    Out-of-fold probabilities are used so scores are not in-sample.
    """
    oof = cross_val_predict(make_model(), train[features], train["observed_label"], cv=5, method="predict_proba")[:, 1]
    tmp = train.assign(score=oof)
    audit = tmp.sample(frac=audit_frac, random_state=config.SEED)

    def fpr(sub: pd.DataFrame, thr: float) -> float:
        neg = sub[sub["true_fraud"] == 0]
        return float((neg["score"] >= thr).mean()) if len(neg) else float("nan")

    target = fpr(audit[audit["region_type"] == reference_group], base_threshold)
    grid = np.round(np.arange(0.05, 0.95, 0.01), 2)
    thresholds = {}
    for g, sub in audit.groupby("region_type"):
        gaps = [abs(fpr(sub, t) - target) for t in grid]
        thresholds[g] = float(grid[int(np.argmin(gaps))])  # closest match; ties -> lowest threshold
    thresholds[reference_group] = base_threshold
    return thresholds
