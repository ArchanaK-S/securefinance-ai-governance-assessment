# NIST AI RMF 1.0 mapping - proposed governance approach (Task 2 support)

| Function | Organisational action at SecureFinance Africa | Evidence in this repository |
|---|---|---|
| **GOVERN** | AI Governance Committee (CEO sponsor; CRO chair; DPO, CISO, Compliance, Data Science, Fraud Ops); AI policy; RACI; go/no-go gate; board reporting; vendor governance | `risk-register/` owners and review frequency |
| **MAP** | System card: purpose, users, affected groups, context (Nigeria), data sources, assumptions; impact assessment (DPIA + algorithmic impact assessment) | `data/DATA_DICTIONARY.md`, `docs/legal-assumptions.md` |
| **MEASURE** | Fairness gate (FPR ratio, disparate impact, TPR gap), accuracy, drift, explainability tests, red-teaming (authorised only); independent verified audit sample | `src/sfa_fairness/`, `results/` |
| **MANAGE** | Prioritised controls, treatment owners, human review of adverse decisions, appeals, rollback, incident escalation with severity matrix, post-incident learning | `risk-register/risk_register.csv`, `results/tables/mitigation_comparison.csv` |

## Human oversight design
No solely automated adverse decisions on customers. Reviewer sees reason codes and evidence, may override,
and override/reversal rates are monitored by group.

## Incident escalation (summary)
| Severity | Example | Escalate to | Target time |
|---|---|---|---|
| S1 Critical | Confirmed data breach; mass false-positive event; discriminatory outcome confirmed | AI Governance Committee + CEO; DPO assesses 72-hour NDPC notice | Immediately / within 24 hours |
| S2 High | Fairness gate breach in monitoring; vendor model change | CRO, Head of Data Science | 1 business day |
| S3 Medium | Drift alert, reviewer override spike | Model owner | 5 business days |
