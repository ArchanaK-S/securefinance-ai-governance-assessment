"""Generate the FULLY SYNTHETIC applicant dataset used in the fairness evaluation.

No real person, customer, account, ID document or transaction is represented.
All values are drawn from the pseudo-random generators below.

Design (documented assumptions, see docs/methodology.md):
  * True fraud prevalence is identical (6%) across every group by construction.
    Any outcome gap therefore cannot be explained by genuine behavioural differences.
  * Rural applicants are under-represented (12%) -> representation bias.
  * Three features are distorted for rural applicants by *measurement* effects
    (lower camera / ID-capture quality, weaker device tier, less accurate
    network geolocation) -> proxy and measurement bias.
  * Historical investigator labels contain extra false "fraud" labels for
    peri-urban and rural applicants -> label bias in the training signal.
  * Gender is deliberately given NO injected effect. It serves as a control
    attribute: a sound method should NOT report a material gender disparity.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import config

REGION_P = {"urban": 0.62, "peri_urban": 0.26, "rural": 0.12}
GENDER_P = {"female": 0.48, "male": 0.52}
FRAUD_PREVALENCE = 0.06
# Probability that a genuine (non-fraud) customer received a historical "fraud" label.
EXTRA_FALSE_LABEL = {"urban": 0.012, "peri_urban": 0.030, "rural": 0.070}
FRAUD_LABEL_RECALL = 0.85  # share of real fraud that investigators historically labelled


def generate(n: int = config.N_RECORDS, seed: int = config.SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    gender = rng.choice(list(GENDER_P), size=n, p=list(GENDER_P.values()))
    region = rng.choice(list(REGION_P), size=n, p=list(REGION_P.values()))
    age = np.clip(rng.normal(34, 10, n), 18, 75).round().astype(int)
    fraud = rng.random(n) < FRAUD_PREVALENCE  # independent of gender and region

    is_rural = region == "rural"
    is_peri = region == "peri_urban"

    # --- behavioural features (depend on true fraud only) -------------------
    txn_velocity = np.where(
        fraud, rng.gamma(3.0, 1.4, n), rng.gamma(2.0, 1.1, n)
    )  # transactions per 24h
    avg_amount_log = np.where(
        fraud, rng.normal(10.7, 1.0, n), rng.normal(10.2, 0.9, n)
    )  # log of NGN amount
    night_ratio = np.clip(
        np.where(fraud, rng.beta(3, 6, n), rng.beta(2, 6, n)), 0, 1
    )
    new_device = (rng.random(n) < np.where(fraud, 0.35, 0.15)).astype(int)
    account_age = np.where(
        fraud, rng.gamma(2.0, 110, n), rng.gamma(3.0, 200, n)
    ).round().astype(int)

    # --- identity verification score: measurement bias for rural users ------
    id_match = np.where(fraud, rng.normal(0.74, 0.12, n), rng.normal(0.88, 0.07, n))
    id_match = id_match - np.where(is_rural, 0.07, np.where(is_peri, 0.025, 0.0))
    id_match = np.clip(id_match + rng.normal(0, 0.02, n), 0, 1)

    # --- device tier proxy (1 = entry level ... 3 = premium) ----------------
    tier_p_urban = [0.20, 0.45, 0.35]
    tier_p_peri = [0.38, 0.45, 0.17]
    tier_p_rural = [0.62, 0.33, 0.05]
    device_tier = np.empty(n, dtype=int)
    for mask, p in ((~is_rural & ~is_peri, tier_p_urban), (is_peri, tier_p_peri), (is_rural, tier_p_rural)):
        device_tier[mask] = rng.choice([1, 2, 3], size=mask.sum(), p=p)

    # --- geolocation mismatch: noisier network geolocation outside cities ---
    geo_base = np.where(fraud, 0.30, 0.07)
    geo_extra = np.where(is_rural, 0.12, np.where(is_peri, 0.04, 0.0))
    geo_mismatch = (rng.random(n) < geo_base + geo_extra).astype(int)

    # --- historical (observed) investigator label, with label bias ----------
    extra_fp = np.array([EXTRA_FALSE_LABEL[r] for r in region])
    detected = rng.random(n) < FRAUD_LABEL_RECALL
    spurious = rng.random(n) < extra_fp
    observed_label = np.where(fraud, detected, spurious).astype(int)

    df = pd.DataFrame(
        {
            "applicant_id": [f"SYN-{i:06d}" for i in range(1, n + 1)],
            "gender": gender,
            "region_type": region,
            "age": age,
            "txn_velocity_24h": txn_velocity.round(3),
            "avg_txn_amount_log": avg_amount_log.round(3),
            "night_txn_ratio": night_ratio.round(3),
            "new_device_flag": new_device,
            "account_age_days": account_age,
            "id_match_score": id_match.round(3),
            "device_tier": device_tier,
            "geo_mismatch_flag": geo_mismatch,
            "true_fraud": fraud.astype(int),
            "observed_label": observed_label,
        }
    )
    return df


def main() -> None:
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = generate()
    df.to_csv(config.DATA_FILE, index=False)
    print(f"Wrote {len(df):,} synthetic records to {config.DATA_FILE}")


if __name__ == "__main__":
    main()
