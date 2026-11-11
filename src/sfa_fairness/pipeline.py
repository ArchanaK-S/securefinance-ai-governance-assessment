"""End-to-end, reproducible fairness and explainability evaluation.

Run:  python -m sfa_fairness.pipeline        (from the repo root with `pip install -e .`)
  or: python scripts/run_all.py
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from . import config, explain, generate_data, metrics, modeling, plots


def _flag(model, X, thr):
    p = model.predict_proba(X)[:, 1]
    return p, (p >= thr).astype(int)


def _variant_row(name, test, flag, extra=None):
    t = test.assign(flag=flag)
    reg = metrics.group_table(t, "region_type")
    overall = metrics.confusion_rates(t["true_fraud"].values, t["flag"].values)
    di = reg.loc["rural", "flag_rate"] / reg.loc["urban", "flag_rate"]
    row = {
        "variant": name,
        "fpr_urban": reg.loc["urban", "fpr"], "fpr_peri_urban": reg.loc["peri_urban", "fpr"], "fpr_rural": reg.loc["rural", "fpr"],
        "fpr_ratio_rural_vs_urban": reg.loc["rural", "fpr"] / reg.loc["urban", "fpr"],
        "tpr_urban": reg.loc["urban", "tpr"], "tpr_rural": reg.loc["rural", "tpr"],
        "disparate_impact_rural_vs_urban": di,
        "recall_overall": overall["tpr"], "precision_overall": overall["precision"], "flag_rate_overall": overall["flag_rate"],
    }
    if extra:
        row.update(extra)
    return row


def run() -> dict:
    for d in (config.TABLE_DIR, config.FIG_DIR):
        d.mkdir(parents=True, exist_ok=True)

    if not config.DATA_FILE.exists():
        generate_data.main()
    df = pd.read_csv(config.DATA_FILE)
    train, test = modeling.split(df)
    feats, thr = config.MODEL_FEATURES, config.DECISION_THRESHOLD

    # ---------------- baseline model ----------------
    base = modeling.fit(train, feats)
    p, flag = _flag(base, test[feats], thr)
    test = test.assign(score=p, flag=flag)
    auc_true = roc_auc_score(test["true_fraud"], p)

    region_tbl = metrics.group_table(test, "region_type")
    gender_tbl = metrics.group_table(test, "gender")
    region_disp = metrics.disparity_summary(region_tbl, "urban")
    gender_disp = metrics.disparity_summary(gender_tbl, "male")

    seed = config.SEED
    ci = {}
    for key, col in (("region", "region_type"), ("gender", "gender")):
        ci[key] = {s: metrics.bootstrap_ci(test, col, s, config.N_BOOTSTRAP, seed) for s in ("fpr", "flag_rate", "tpr")}
    region_out = region_tbl.join([ci["region"][s] for s in ci["region"]])
    gender_out = gender_tbl.join([ci["gender"][s] for s in ci["gender"]])
    region_out.to_csv(config.TABLE_DIR / "baseline_metrics_by_region.csv")
    gender_out.to_csv(config.TABLE_DIR / "baseline_metrics_by_gender.csv")
    region_disp.to_csv(config.TABLE_DIR / "baseline_disparity_region_vs_urban.csv")
    gender_disp.to_csv(config.TABLE_DIR / "baseline_disparity_gender_vs_male.csv")

    # What the organisation could "see" using only historical labels (label bias hides harm)
    seen = metrics.group_table(test, "region_type", y_true="observed_label")[["base_rate", "fpr", "tpr", "precision"]]
    seen.columns = [f"{c}_vs_observed_labels" for c in seen.columns]
    seen.to_csv(config.TABLE_DIR / "baseline_metrics_vs_observed_labels.csv")

    plots.rates_by_group(region_tbl, ci["region"]["fpr"], ci["region"]["flag_rate"],
                         gender_tbl, ci["gender"]["fpr"], ci["gender"]["flag_rate"])

    # ---------------- explainability ----------------
    coefs = explain.coefficient_table(base, feats)
    perm = explain.permutation_table(base, test, feats)
    proxy = explain.proxy_test(df, feats, config.SUSPECT_PROXIES)
    coefs.to_csv(config.TABLE_DIR / "explain_coefficients.csv", index=False)
    perm.to_csv(config.TABLE_DIR / "explain_permutation_importance.csv", index=False)
    proxy.to_csv(config.TABLE_DIR / "explain_proxy_test.csv", index=False)
    plots.importance(coefs, perm)

    feature_means = df.groupby("region_type")[feats].mean().round(3)
    feature_means.to_csv(config.TABLE_DIR / "feature_means_by_region.csv")

    rural_fp = test[(test.region_type == "rural") & (test.true_fraud == 0) & (test.flag == 1)]
    urban_gen = test[(test.region_type == "urban") & (test.true_fraud == 0)]
    contrib_fp = explain.contributions(base, rural_fp, feats)
    contrib_urban = explain.contributions(base, urban_gen, feats)
    contrib_fp.mean().rename("mean_contribution_rural_false_positives").to_frame().join(
        contrib_urban.mean().rename("mean_contribution_urban_genuine")).to_csv(
        config.TABLE_DIR / "explain_contributions_rural_fp_vs_urban.csv")
    case_idx = (rural_fp["score"] - rural_fp["score"].median()).abs().idxmin()
    plots.local_review(contrib_fp.loc[case_idx], contrib_urban.mean(), rural_fp.loc[case_idx, "applicant_id"],
                       rural_fp.loc[case_idx, "score"])
    case_table = contrib_fp.loc[[case_idx]].T.rename(columns={case_idx: "contribution_log_odds"})
    case_table["feature_value"] = rural_fp.loc[case_idx, feats]
    case_table.to_csv(config.TABLE_DIR / "explain_representative_case.csv")

    clean_urban_genuine = urban_gen[urban_gen.flag == 0]
    cf = explain.counterfactual_flip_rate(base, rural_fp, clean_urban_genuine, feats,
                                          swap=["id_match_score", "device_tier", "geo_mismatch_flag"], threshold=thr)

    cf_rows = [{"swapped": "+".join(sw), **{k: v for k, v in explain.counterfactual_flip_rate(
        base, rural_fp, clean_urban_genuine, feats, swap=sw, threshold=thr).items() if k != "swapped_features"}}
        for sw in (["id_match_score"], ["device_tier"], ["geo_mismatch_flag"], ["account_age_days"],
                   ["id_match_score", "device_tier", "geo_mismatch_flag"])]
    pd.DataFrame(cf_rows).to_csv(config.TABLE_DIR / "explain_counterfactual_flip_rates.csv", index=False)

    # ---------------- mitigation variants ----------------
    rows = [_variant_row("1 Baseline", test, flag)]

    w = modeling.reweighing_weights(train)
    m_rw = modeling.fit(train, feats, w)
    _, f_rw = _flag(m_rw, test[feats], thr)
    rows.append(_variant_row("2 Reweighing", test, f_rw))

    reduced = [f for f in feats if f not in ("device_tier", "geo_mismatch_flag")]
    m_red = modeling.fit(train, reduced)
    _, f_red = _flag(m_red, test[reduced], thr)
    rows.append(_variant_row("3 Drop device+geo", test, f_red))

    thresholds = modeling.audit_calibrated_thresholds(train, feats, thr)
    p_base = test["score"].values
    f_thr = np.array([int(s >= thresholds[r]) for s, r in zip(p_base, test["region_type"])])
    rows.append(_variant_row("4 Audit-calibrated thresholds", test, f_thr))

    variants = pd.DataFrame(rows).set_index("variant")
    variants.to_csv(config.TABLE_DIR / "mitigation_comparison.csv")
    plots.mitigation(variants)

    summary = {
        "seed": config.SEED, "n_records": int(len(df)), "n_train": int(len(train)), "n_test": int(len(test)),
        "decision_threshold": thr, "true_fraud_prevalence": float(df.true_fraud.mean()),
        "baseline_auc_vs_true_fraud": float(auc_true),
        "group_sizes_test": {k: int(v) for k, v in test.region_type.value_counts().items()},
        "baseline_region": region_out.round(4).reset_index().to_dict(orient="records"),
        "baseline_gender": gender_out.round(4).reset_index().to_dict(orient="records"),
        "disparity_region_vs_urban": region_disp.round(4).reset_index().to_dict(orient="records"),
        "disparity_gender_vs_male": gender_disp.round(4).reset_index().to_dict(orient="records"),
        "proxy_test": proxy.round(4).to_dict(orient="records"),
        "counterfactual_review_rural_false_positives": cf,
        "audit_calibrated_thresholds": thresholds,
        "mitigation": variants.round(4).reset_index().to_dict(orient="records"),
    }
    (config.RESULTS_DIR / "metrics_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    s = run()
    print("Pipeline complete. Key results:")
    for r in s["baseline_region"]:
        print(f"  {r['region_type']:<11} n={r['n']:<5} flag_rate={r['flag_rate']:.3f}  FPR={r['fpr']:.3f}  TPR={r['tpr']:.3f}")
    print("  counterfactual:", s["counterfactual_review_rural_false_positives"])


if __name__ == "__main__":
    main()
