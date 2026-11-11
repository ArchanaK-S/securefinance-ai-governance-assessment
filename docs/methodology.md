# Fairness and explainability methodology (Task 4)

## 1. Question
Does the proposed fraud/identity screening model flag genuine customers from some groups materially more
often than others, why, and what controls reduce the gap at an acceptable cost to fraud detection?

## 2. Harm model
A **flag** triggers an account hold or enhanced verification. For a genuine customer this is the adverse outcome,
so the **false-positive rate (FPR)** is the primary harm metric. The **true-positive rate (TPR)** shows whether
fraud protection is equally effective across groups.

## 3. Data
Synthetic, 20,000 records, seeded and reproducible. See `data/DATA_DICTIONARY.md` for variables and the biases
deliberately injected. Split: 70% train / 30% test, stratified by region and observed label.
Protected attributes (`gender`, `region_type`) are **not** model inputs ("fairness through unawareness") but are
used to audit outcomes, which is the realistic situation when sensitive attributes are not collected or are
excluded from scoring.

## 4. Model
Standardised logistic regression trained on `observed_label` (what a real firm would have), operating threshold
0.30 (documented, chosen to give an overall flag rate near 5%). Evaluation uses the synthetic `true_fraud`
ground truth, and, for contrast, the biased `observed_label`.

## 5. Fairness measures and why
| Measure | Definition | Why relevant |
|---|---|---|
| Statistical parity difference | flag rate(g) - flag rate(ref) | Visible gap in how often groups are intervened on |
| Disparate-impact ratio | flag rate(g) / flag rate(ref) | Screening heuristic; 0.80-1.25 band used as an *internal tolerance*, not a legal test in Nigeria |
| Predictive equality (FPR gap/ratio) | FPR(g) vs FPR(ref) | Direct measure of wrongful intervention on genuine customers - **primary** |
| Equal opportunity (TPR gap) | TPR(g) - TPR(ref) | Equal protection from fraud |
| Equalised-odds gap | max(abs TPR gap, abs FPR gap) | Single summary |

Reference groups: `urban` (region), `male` (gender). 95% percentile bootstrap intervals (1,000 resamples) are
reported because rural counts are small.

## 6. Explainability and decision review
1. **Global:** standardised coefficients and permutation importance (AUC drop, 20 repeats).
2. **Proxy test:** can `region_type = rural` be predicted from model inputs? (5-fold CV AUC; 0.5 = no signal.)
3. **Local review:** exact per-feature contributions to the log-odds for rural false positives vs average urban
   genuine customers (coefficient x standardised value).
4. **Counterfactual review:** would the flag disappear if a feature took typical urban-genuine values?

## 7. Mitigations compared
1. Baseline. 2. Reweighing (Kamiran and Calders 2012) on region x label. 3. Dropping suspected proxies
(`device_tier`, `geo_mismatch_flag`). 4. Per-group thresholds calibrated on a **verified audit sample** (30% of
training data assumed independently verified) so FPR matches the urban reference.

Option 4 uses group-specific thresholds. That is a legal and policy decision (equal treatment vs equal outcomes)
and is presented as an option for governance review, not a default recommendation.

## 8. Limitations
See `docs/limitations.md`.

## 9. Reproduce
```bash
python -m pip install -e ".[dev]"
python scripts/run_all.py && pytest -q
```
