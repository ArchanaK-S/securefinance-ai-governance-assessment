# SecureFinance Africa - AI Ethics, Governance and Legal Compliance Assessment

[![CI](https://github.com/ArchanaK-S/securefinance-ai-governance-assessment/actions/workflows/ci.yml/badge.svg)](https://github.com/ArchanaK-S/securefinance-ai-governance-assessment/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Data](https://img.shields.io/badge/data-100%25%20synthetic-orange)

Evidence repository for **ICDFA AICS-201, Assessment 01** (AI Ethics, Governance and Legal Frameworks).
It supports the written report with a reproducible fairness evaluation, an AI risk register and governance documentation
for the **fictional** SecureFinance Africa platform (identity verification, fraud detection and automated risk assessment, planned for Nigeria).

> **Data safety:** every record is synthetic. No real customer data, credentials or financial identifiers are included.

## Headline finding
In the synthetic evaluation the baseline model wrongly flags **4.2% of genuine rural customers versus 0.7% of urban customers (5.9x)**,
despite identical true fraud prevalence. The gap is traced mainly to measurement bias in the ID-match signal rather than to the
obvious proxy features, and a control comparison shows the accuracy cost of each remedy. Gender, used as a control, shows no material gap.
Details: [`results/README.md`](results/README.md).

## Repository map

| Path | Purpose | Assessment task |
|---|---|---|
| [`risk-register/`](risk-register/) | 12-risk register (CSV source, scored CSV, Markdown view) with likelihood, impact, owner, controls, residual risk | Task 2 |
| [`docs/nist-ai-rmf-mapping.md`](docs/nist-ai-rmf-mapping.md) | Govern/Map/Measure/Manage mapping, oversight and incident escalation | Task 2 |
| [`docs/legal-assumptions.md`](docs/legal-assumptions.md) | Binding vs non-binding instruments, jurisdiction assumptions and triggers | Task 3 |
| [`data/`](data/) | Synthetic dataset and data dictionary | Task 4 |
| [`src/sfa_fairness/`](src/sfa_fairness/) | Data generator, metrics, model, explainability, mitigation, plots | Task 4 |
| [`results/`](results/) | Tables, figures, JSON summary (committed evidence) | Task 4 |
| [`docs/methodology.md`](docs/methodology.md), [`docs/limitations.md`](docs/limitations.md) | Method, assumptions, caveats | Tasks 4-5 |
| [`docs/ai-use-declaration.md`](docs/ai-use-declaration.md) | AI-assisted tools declaration | Integrity |
| [`report/`](report/) | Final PDF report | Task 5 |
| [`tests/`](tests/), [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | Unit tests and CI that re-runs the whole analysis | Quality |

## Quick start
```bash
git clone https://github.com/ArchanaK-S/securefinance-ai-governance-assessment.git
cd securefinance-ai-governance-assessment
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
python scripts/run_all.py      # regenerate data, run fairness evaluation, rebuild risk register + figures
pytest -q                      # 9 tests
```
Everything is seeded (`SEED = 20260611` in [`config.py`](src/sfa_fairness/config.py)); re-running reproduces the committed outputs.
`make all` does the same where `make` is available.

## Method in one paragraph
A standardised logistic regression flags suspected fraud using eight behavioural, device and identity features; gender and region are **not**
inputs but are audited. Fairness is measured with statistical parity difference, disparate-impact ratio, FPR (primary harm) and TPR gaps,
with bootstrap confidence intervals. Explainability uses exact per-feature contributions, permutation importance, a proxy-detection test and
counterfactual decision review. Four controls are compared. See [`docs/methodology.md`](docs/methodology.md).

## Limitations
Synthetic data demonstrate the method, not real-world prevalence; subgroup counts are small; legal analysis is educational, not legal advice.
See [`docs/limitations.md`](docs/limitations.md).

## Key references
NIST AI RMF 1.0 (NIST AI 100-1, 2023) - Nigeria Data Protection Act 2023 and NDPC GAID 2025 - Regulation (EU) 2024/1689 (EU AI Act) -
UNESCO Recommendation on the Ethics of AI (2021) - OECD AI Principles (2019, rev. 2024). Full list in the report.

## Licence and author
MIT - see [`LICENSE`](LICENSE). Author: [Student Name], ICDFA AICS-201. Cite via [`CITATION.cff`](CITATION.cff).
