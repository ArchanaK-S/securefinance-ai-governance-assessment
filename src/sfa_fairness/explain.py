"""Explainability and decision-review techniques for the (linear) screening model.

Because the model is a standardised logistic regression, per-feature contributions to the
log-odds are EXACT: contribution_j = coef_j * (x_j - mean_j) / std_j. No approximation
library is needed, which keeps the analysis transparent and reproducible.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from . import config


def coefficient_table(model: Pipeline, features: list[str]) -> pd.DataFrame:
    coefs = model.named_steps["clf"].coef_[0]
    return (pd.DataFrame({"feature": features, "std_coef": coefs, "odds_ratio_per_sd": np.exp(coefs)})
            .sort_values("std_coef", key=np.abs, ascending=False).reset_index(drop=True))


def permutation_table(model: Pipeline, test: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    res = permutation_importance(model, test[features], test["observed_label"], scoring="roc_auc",
                                 n_repeats=20, random_state=config.SEED)
    return (pd.DataFrame({"feature": features, "auc_drop_mean": res.importances_mean, "auc_drop_sd": res.importances_std})
            .sort_values("auc_drop_mean", ascending=False).reset_index(drop=True))


def proxy_test(df: pd.DataFrame, features: list[str], suspects: list[str]) -> pd.DataFrame:
    """Can the 'protected' attribute be inferred from model inputs? (5-fold CV AUC; 0.5 = no signal)."""
    y = (df["region_type"] == "rural").astype(int)
    rows = []
    sets = {"ALL model features": features, **{f"only {s}": [s] for s in suspects},
            "all features except suspects": [f for f in features if f not in suspects]}
    for name, cols in sets.items():
        pipe = Pipeline([("s", StandardScaler()), ("c", LogisticRegression(max_iter=2000))])
        p = cross_val_predict(pipe, df[cols], y, cv=5, method="predict_proba")[:, 1]
        rows.append({"feature_set": name, "auc_predicting_rural": roc_auc_score(y, p)})
    return pd.DataFrame(rows)


def contributions(model: Pipeline, X: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    scaler, clf = model.named_steps["scale"], model.named_steps["clf"]
    z = (X[features].values - scaler.mean_) / scaler.scale_
    return pd.DataFrame(z * clf.coef_[0], columns=features, index=X.index)


def counterfactual_flip_rate(model: Pipeline, cases: pd.DataFrame, reference_genuine: pd.DataFrame,
                             features: list[str], swap: list[str], threshold: float) -> dict:
    """Decision review: if the `swap` features took typical urban-genuine values, would the flag disappear?"""
    cf = cases[features].copy()
    for f in swap:
        cf[f] = reference_genuine[f].median()
    new_p = model.predict_proba(cf)[:, 1]
    return {"n_cases": int(len(cases)), "swapped_features": swap,
            "share_no_longer_flagged": float((new_p < threshold).mean())}
