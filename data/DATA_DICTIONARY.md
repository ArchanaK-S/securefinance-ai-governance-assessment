# Data dictionary - `synthetic_applicants.csv`

**All records are fully synthetic.** They are produced by `src/sfa_fairness/generate_data.py` using a seeded
pseudo-random generator (`SEED = 20260611`). No real customer, ID document, account or transaction is represented,
and no direct identifier (name, phone, email, BVN, NIN, address) exists in the file.

| Column | Type | Description | Used as model input? |
|---|---|---|---|
| `applicant_id` | string | Synthetic key `SYN-000001` ... | No |
| `gender` | category (`female`, `male`) | Protected attribute - **control attribute with no injected effect** | No (audit only) |
| `region_type` | category (`urban`, `peri_urban`, `rural`) | Protected / sensitive attribute - audit group | No (audit only) |
| `age` | int | Age in years (18-75) | No |
| `txn_velocity_24h` | float | Transactions in the last 24 hours | Yes |
| `avg_txn_amount_log` | float | Natural log of average transaction amount (NGN) | Yes |
| `night_txn_ratio` | float | Share of transactions made 00:00-05:00 | Yes |
| `new_device_flag` | 0/1 | Login from a device not previously seen | Yes |
| `account_age_days` | int | Days since account opening | Yes |
| `id_match_score` | float 0-1 | Face-to-ID match confidence (**measurement bias injected for rural/peri-urban**) | Yes |
| `device_tier` | 1-3 | Device capability tier, 1 = entry level (**proxy for region**) | Yes |
| `geo_mismatch_flag` | 0/1 | IP/network geolocation disagrees with declared address (**noisier outside cities**) | Yes |
| `true_fraud` | 0/1 | Synthetic ground truth. **Not observable in real life**; used only to evaluate error rates | No (evaluation) |
| `observed_label` | 0/1 | Historical investigator label used for training; contains injected label bias | Training target |

## Injected, documented biases (so the audit has something to detect)

1. **Equal true prevalence** - fraud prevalence is ~6% in every group by construction.
2. **Representation bias** - rural = 12%, peri-urban = 25%, urban = 62% of records.
3. **Measurement bias** - `id_match_score` (-0.07 rural, -0.025 peri-urban), `geo_mismatch_flag` (+12 / +4 percentage points), `device_tier` skewed to tier 1.
4. **Label bias** - extra false "fraud" labels for genuine customers: urban 1.2%, peri-urban 3.0%, rural 7.0%; investigators also miss 15% of true fraud.
5. **Gender control** - no injected effect; a sound method should find no material gender disparity.
