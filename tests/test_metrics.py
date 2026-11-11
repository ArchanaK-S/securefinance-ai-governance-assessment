import numpy as np
import pandas as pd
import pytest

from sfa_fairness import metrics


def test_confusion_rates_known_values():
    y_true = np.array([1, 1, 1, 1, 0, 0, 0, 0, 0, 0])
    y_pred = np.array([1, 1, 0, 0, 1, 0, 0, 0, 0, 0])
    r = metrics.confusion_rates(y_true, y_pred)
    assert (r["tp"], r["fn"], r["fp"], r["tn"]) == (2, 2, 1, 5)
    assert r["tpr"] == pytest.approx(0.5)
    assert r["fpr"] == pytest.approx(1 / 6)
    assert r["precision"] == pytest.approx(2 / 3)
    assert r["flag_rate"] == pytest.approx(0.3)


def test_disparity_summary_ratio_and_difference():
    df = pd.DataFrame({
        "g": ["a"] * 10 + ["b"] * 10,
        "y": [0] * 10 + [0] * 10,
        "flag": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0] + [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    })
    tbl = metrics.group_table(df, "g", y_true="y", y_pred="flag")
    d = metrics.disparity_summary(tbl, reference="a")
    assert d.loc["b", "statistical_parity_diff"] == pytest.approx(0.2)
    assert d.loc["b", "disparate_impact_ratio"] == pytest.approx(3.0)
    assert d.loc["b", "fpr_ratio"] == pytest.approx(3.0)


def test_empty_denominator_returns_nan():
    r = metrics.confusion_rates(np.array([0, 0]), np.array([0, 0]))
    assert np.isnan(r["tpr"]) and np.isnan(r["precision"])


def test_bootstrap_ci_brackets_point_estimate():
    rng = np.random.default_rng(1)
    df = pd.DataFrame({"g": ["a"] * 400, "y": rng.integers(0, 2, 400), "flag": rng.integers(0, 2, 400)})
    point = metrics.group_table(df, "g", "y", "flag").loc["a", "flag_rate"]
    ci = metrics.bootstrap_ci(df, "g", "flag_rate", n_boot=200, seed=1, y_true="y", y_pred="flag")
    assert ci.loc["a", "flag_rate_lo"] <= point <= ci.loc["a", "flag_rate_hi"]
