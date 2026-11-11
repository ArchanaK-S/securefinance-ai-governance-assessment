import pandas as pd

from sfa_fairness import config, generate_data, modeling


def test_generation_is_deterministic():
    a = generate_data.generate(n=500, seed=7)
    b = generate_data.generate(n=500, seed=7)
    pd.testing.assert_frame_equal(a, b)


def test_dataset_is_synthetic_and_has_no_real_identifiers():
    df = generate_data.generate(n=300, seed=3)
    assert df["applicant_id"].str.startswith("SYN-").all()
    forbidden = {"name", "email", "phone", "bvn", "nin", "account_number", "address"}
    assert forbidden.isdisjoint(c.lower() for c in df.columns)


def test_protected_attributes_are_not_model_inputs():
    assert set(config.PROTECTED).isdisjoint(config.MODEL_FEATURES)


def test_true_fraud_rate_is_similar_across_groups_by_design():
    df = generate_data.generate(n=20_000, seed=11)
    rates = df.groupby("region_type")["true_fraud"].mean()
    assert rates.max() - rates.min() < 0.02


def test_reweighing_balances_label_rate_across_groups():
    df = generate_data.generate(n=20_000, seed=5)
    w = modeling.reweighing_weights(df)
    weighted = (df["observed_label"] * w).groupby(df["region_type"]).sum() / pd.Series(w, index=df.index).groupby(df["region_type"]).sum()
    assert weighted.max() - weighted.min() < 0.005
