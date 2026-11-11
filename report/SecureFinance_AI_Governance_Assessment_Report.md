# SecureFinance Africa: AI Ethics, Governance and Legal Compliance Assessment

**Course:** AICS-201 – AI Ethics, Governance and Legal Frameworks 
**Prepared by:** Archana K S | **Student ID:** 2026/AICDF/16738
**Evidence repository:** https://github.com/ArchanaK-S/securefinance-ai-governance-assessment.git

## 1. Executive Summary

SecureFinance Africa, a fictional Nigerian fintech, plans to deploy an AI platform for identity verification, fraud detection and financial-risk assessment. The platform could improve security and efficiency, but it also raises concerns about privacy, fairness, transparency and legal compliance.

This report evaluates the platform against ethical principles, the NIST AI Risk Management Framework (AI RMF 1.0) and the relevant Nigerian and international legal frameworks. It includes a fairness test on a synthetic dataset of 20,000 records (6,000 test records).

**Key results**

- Genuine rural customers were wrongly flagged at a false-positive rate (FPR) of 4.2%, against 0.7% for urban customers: about 5.9 times higher (calculated from unrounded rates). Peri-urban customers had an FPR of 1.9%. Gender differences were minimal (1.5% female, 1.4% male).
- Identity-match quality was the main driver. Replacing the rural identity-match score with a typical urban value removed 96.6% of rural false-positive flags. Removing device and geolocation features helped only slightly.
- The Nigeria Data Protection Act 2023 (NDPA) applies and is binding. It requires a Data Protection Impact Assessment (DPIA), extra care for biometric data and safeguards for automated decisions. The EU AI Act is not triggered at launch but could be on EU expansion or credit-related use. UNESCO and OECD principles are non-binding guidance.
- Twelve risks were registered. Eight were initially High or Critical. If the proposed controls are implemented and verified, none is expected to exceed Medium.

**Recommendation:** conditional approval for a controlled pilot, with no approval for fully automated adverse decisions. Before launch, the company must complete its DPIA, pass fairness testing on verified audit data, introduce human review and appeals, provide reason codes and establish an AI governance committee.

## 2. System Description, Scope and Assumptions

### 2.1 The platform

1. **Identity verification:** identity documents and facial matching.
2. **Fraud detection:** analysis of transaction patterns, device information and location signals.
3. **Financial-risk assessment:** risk scores that recommend account holds, declines or extra verification.

### 2.2 Stakeholders

Customers (especially rural and first-time users), fraud analysts, compliance and risk teams, executives, identity and cloud vendors, the Nigeria Data Protection Commission (NDPC) and financial regulators.

### 2.3 Assumptions

- SecureFinance Africa operates in Nigeria and is the data controller. Vendors are processors.
- Facial-matching data is treated as sensitive biometric data.
- At launch there are no EU customers or operations. Expansion, or use of risk scores in credit decisions, may follow later.
- Only fictional and synthetic data were used. No live system or third-party service was tested. This is an academic exercise and not legal advice.

## 3. Key Findings

1. **Accuracy is not enough.** The model detects roughly 62% of fraud at 74% precision, but errors fall unevenly on rural customers.
2. **Removing sensitive fields does not guarantee fairness.** Region and gender were excluded from the model, yet rural status could still be predicted from other inputs (AUC 0.81).
3. **The root cause is data quality, not geolocation.** Poor identity capture drives most rural false positives.
4. **Automated adverse decisions create the greatest legal and customer-harm exposure** under NDPA section 37.
5. **Governance gaps are the largest residual risk.** Appeals, human review and clear ownership must exist before launch.

## 4. Task 1: Ethical Risk Identification

| Risk | Cause | Affected stakeholders | Likely consequence | Proportionate control |
| --- | --- | --- | --- | --- |
| **E1. Algorithmic bias** | Under-represented rural data, weak identity capture, biased historical labels | Rural and thin-file customers | More false flags, unequal treatment | Regular fairness testing, label review, better identity capture |
| **E2. Privacy intrusion** | Excess biometric, device and location collection | Customers, DPO, NDPC | Unlawful processing, loss of trust, penalties | Data minimisation, documented lawful basis, DPIA |
| **E3. Unfair financial exclusion** | Incorrect flags with slow appeals | Genuine customers | Frozen accounts, declined transactions, hardship | Appeals targeting resolution within two business days; harm monitoring |
| **E4. Lack of transparency** | Opaque scores and no explanations | Customers, reviewers, regulators | Decisions that cannot be understood or challenged | Reason codes, customer notices, reviewer explanations |
| **E5. Weak human oversight** | Workload and time pressure cause automation bias | Customers, fraud analysts | Errors accepted without scrutiny | Meaningful review, override authority, reviewer training |
| **E6. Unclear accountability** | Responsibility split across departments | Executives, regulators, customers | Delayed fixes, no clear owner | Governance committee and RACI matrix |

## 5. Task 2: AI Governance and Risk Management (NIST AI RMF)

### 5.1 Govern

An **AI Governance Committee**, chaired by the Chief Risk Officer (CRO) with the CEO as executive sponsor, should include Data Protection, Information Security, Compliance, Data Science, Fraud Operations and Legal. It approves AI policies, reviews risk assessments, authorises deployment and reports to the board.

- Head of Data Science: model performance and fairness.
- Data Protection Officer (DPO): privacy and data protection.
- Chief Information Security Officer (CISO): security.
- Head of Fraud Operations: human review of AI decisions.

Vendor contracts must include audit rights and incident-notification duties.

### 5.2 Map

Before deployment, document the system's purpose, users, affected groups, data sources and limitations. Complete a DPIA and an algorithmic impact assessment, and repeat them when the purpose changes (for example, credit use or a new market).

### 5.3 Measure

Track accuracy, recall, FPR, true-positive rate (TPR) and disparate-impact ratios by group. Add explainability checks, drift monitoring and authorised red-team testing. Because true fraud outcomes are not immediately known in live use, fairness testing should rely on a verified random audit sample.

### 5.4 Manage and human oversight

Controls follow the risk register below. Drift and override rates are reviewed monthly and fairness quarterly. No adverse customer decision may rest solely on an automated recommendation. Reviewers must understand the reasons, be able to override and be trained against automation bias.

### 5.5 Incident escalation

| Severity | Example | Escalation |
| --- | --- | --- |
| S1 | Confirmed breach, widespread false positives or discriminatory outcomes | Notify committee and CEO immediately; DPO assesses the 72-hour NDPC notification duty |
| S2 | Fairness-gate failure or unexpected vendor model change | Escalate to CRO within one business day |
| S3 | Model drift or unusual override-rate rise | Notify model owner within five days |

Every incident is documented and reviewed for root cause.

### 5.6 AI risk register

Risk score = Likelihood (L) × Impact (I), each rated 1–5. Bands: 1–5 Low; 6–11 Medium; 12–19 High; 20–25 Critical.

| ID | Risk | L | I | Initial | Owner | Control | Residual (L×I) |
| --- | --- | --: | --: | --- | --- | --- | --- |
| R01 | Higher false-positive rates for rural customers | 4 | 4 | 16 High | Head of Data Science | Fairness testing, better identity capture | 3×3 = 9 Medium |
| R02 | Unlawful or excessive personal-data processing | 3 | 5 | 15 High | DPO | Lawful-basis review, minimisation, DPIA | 2×4 = 8 Medium |
| R03 | Customers cannot understand or challenge decisions | 4 | 4 | 16 High | Compliance Officer | Reason codes, customer notices | 2×3 = 6 Medium |
| R04 | Automated holds or declines without meaningful review | 4 | 5 | 20 Critical | Head of Fraud Operations | Mandatory human review, override authority | 2×4 = 8 Medium |
| R05 | Rural and thin-file customers under-represented in training data | 3 | 4 | 12 High | Head of Data Science | Stratified sampling, verified audit data | 3×3 = 9 Medium |
| R06 | Exposure of biometric, identity or transaction data | 3 | 5 | 15 High | CISO | Encryption, least privilege, breach procedures | 2×4 = 8 Medium |
| R07 | Model drift reduces accuracy and fairness | 3 | 3 | 9 Medium | Head of Data Science | Drift monitoring, rollback | 2×2 = 4 Low |
| R08 | Vendors introduce biased or poorly governed models | 3 | 3 | 9 Medium | Head of Vendor Risk | Vendor assessment, independent testing | 2×2 = 4 Low |
| R09 | Failure to meet Nigerian or applicable EU requirements | 3 | 5 | 15 High | General Counsel | Compliance register, jurisdiction reviews | 2×4 = 8 Medium |
| R10 | Genuine customers suffer financial exclusion | 4 | 4 | 16 High | CRO | Faster appeals, harm monitoring | 3×3 = 9 Medium |
| R11 | AI incidents not identified or escalated promptly | 3 | 3 | 9 Medium | CRO | Incident classification, 24×7 escalation | 2×2 = 4 Low |
| R12 | Unclear responsibilities across departments | 3 | 3 | 9 Medium | CEO | Committee, RACI, internal audit | 2×2 = 4 Low |

Eight risks (R01–R06, R09, R10) start as High or Critical. After controls, none exceeds Medium. R01, R05 and R10 carry the highest residual score (9), so fairness testing and customer protection must remain mandatory deployment conditions.

## 6. Task 3: Legal and Regulatory Compliance

### 6.1 Binding and non-binding instruments

| Instrument | Status | When it affects SecureFinance Africa |
| --- | --- | --- |
| Nigeria Data Protection Act 2023 (NDPA) and NDPC GAID 2025 | Binding | Whenever it processes personal data of individuals in Nigeria |
| EU AI Act, Regulation (EU) 2024/1689 | Binding where applicable | Only with a qualifying EU connection (see 6.3) |
| UNESCO Recommendation on the Ethics of AI (2021) | Non-binding | Guidance only |
| OECD AI Principles (2019, updated 2024) | Non-binding | Guidance only |

### 6.2 Nigeria Data Protection Act 2023

- **Principles and lawful basis (ss. 24–25):** processing must be lawful, fair, transparent, purpose-limited, minimised, accurate and secure. A lawful basis must be documented for onboarding, fraud detection and risk assessment; consent is not automatically the right basis for all of them.
- **Sensitive personal data (s. 30):** biometric data used to identify a person needs additional protection, so the facial-matching function needs particular attention.
- **DPIA (s. 28):** biometrics, profiling and automated decisions create high risk, so a DPIA is needed before deployment.
- **Automated decision-making (s. 37):** individuals have rights regarding decisions based solely on automated processing that have legal or similarly significant effects, subject to the Act's exceptions and safeguards. Account holds and declines qualify, so meaningful human review is essential.
- **Security and breaches (ss. 39–40):** technical and organisational safeguards are required. The NDPC must be notified within 72 hours of awareness of a breach likely to risk individuals' rights, and affected individuals must be told promptly where the risk is high.
- **Cross-border transfers (Part VIII):** transfers to foreign vendors or cloud regions need an adequacy decision or another permitted safeguard.
- **Controller of major importance:** depending on scale, the company may face additional registration and DPO duties.

Other Nigerian obligations include KYC rules, anti-money-laundering law and cybercrime legislation.

### 6.3 EU Artificial Intelligence Act

The Act can reach non-EU organisations whose systems are placed on the EU market, deployed in the EU or whose outputs are used in the EU. Under this report's assumptions, it **does not apply at launch**. Future changes could alter this:

- **Fraud detection:** expressly excluded from the Annex III point 5(b) creditworthiness category.
- **Credit-related risk scoring of people in the EU:** generally high-risk. Relevant requirements include risk management (Art. 9), data governance (Art. 10), transparency (Art. 13), human oversight (Art. 14), deployer duties (Art. 26) and a fundamental-rights impact assessment (Art. 27).
- **Identity verification:** one-to-one biometric verification is excluded from the remote biometric identification high-risk category, although data protection law still applies.

**Timing:** Regulation (EU) 2026/1744 (the Digital Omnibus on AI) was published in the Official Journal on 24 July 2026 and entered into force on 27 July 2026. It moved the application date for stand-alone Annex III high-risk obligations from 2 August 2026 to 2 December 2027. This is confirmed by several law-firm reports; the dates should still be checked against EUR-Lex before any compliance reliance.

### 6.4 UNESCO and OECD principles

UNESCO stresses fairness, privacy, transparency, human oversight, proportionality and avoiding harm. The OECD principles cover inclusive growth and well-being, human rights and democratic values (including fairness and privacy), transparency and explainability, robustness and safety, and accountability. They support the proposed controls but do not replace NDPA compliance. The legal review should be repeated on EU entry, credit use or new international transfers.

## 7. Task 4: Algorithmic Fairness and Explainability

### 7.1 Dataset and method

A synthetic dataset of 20,000 records was generated with a fixed random seed. Fraud prevalence was about 6% in every group. Rural customers were deliberately under-represented, with lower identity-match scores, more geolocation mismatches and more incorrect historical fraud labels (7.0% of genuine rural customers, 3.0% peri-urban, 1.2% urban). Gender was a control variable with no built-in effect.

A logistic regression used eight behavioural, device and identity features, excluding gender and region. Data were split 70/30 (14,000 train, 6,000 test) with a threshold of 0.30.

**Why these measures:** FPR is the primary measure because wrongly flagging genuine customers causes account restrictions. TPR, statistical parity difference and the disparate-impact ratio (ratio of group flag rates) were also used, with an internal tolerance of 0.80–1.25 and 95% bootstrap confidence intervals.

### 7.2 Results

| Group | Test records | Flag rate | FPR (95% CI) | TPR |
| --- | --: | --: | --: | --: |
| Urban | 3,734 | 4.3% | 0.7% (0.5–1.0) | 59.5% |
| Peri-urban | 1,526 | 5.4% | 1.9% (1.2–2.6) | 62.5% |
| Rural | 740 | 9.1% | 4.2% (2.8–5.8) | 74.5% |
| Female | 2,861 | 5.4% | 1.5% (1.1–2.0) | 62.6% |
| Male | 3,139 | 5.0% | 1.4% (0.9–1.8) | 62.0% |

Rural customers had an FPR about 5.9 times the urban rate. The rural-to-urban statistical parity difference was +4.8 percentage points and the disparate-impact ratio was 2.11, well outside the tolerance range. Peri-urban customers were also affected. Gender differences were small and within tolerance.

Excluding region and gender did not prevent unfair outcomes, because other features act as proxies. Evaluating against biased historical labels would also mislead: rural TPR would appear as 38% (versus 49% urban) instead of the true 74.5% (versus 59.5%).

### 7.3 Explainability findings

- Permutation importance ranked `id_match_score` (AUC drop 0.068) and `account_age_days` (0.061) highest.
- Rural status could be predicted from the inputs with AUC 0.81; removing three suspected proxies reduced this to 0.50 (individual AUCs: `id_match_score` 0.71, `device_tier` 0.72, `geo_mismatch_flag` 0.55).
- Across 29 rural false positives, the average identity-match contribution was +1.26 log-odds, against −0.21 for urban genuine customers.
- **Counterfactual test:** replacing the identity-match score with a typical urban value removed 96.6% of rural false positives. Changing geolocation alone removed 27.6%; changing device tier alone removed none.

Identity-capture quality (camera quality, document clarity, verification conditions) is therefore the main problem.

### 7.4 Fairness controls

| Control | Rural FPR | Rural/urban FPR ratio | Disparate impact | Recall | Precision |
| --- | --: | --: | --: | --: | --: |
| Baseline | 4.2% | 5.9x | 2.11 | 62.3% | 73.8% |
| Reweighing | 3.3% | 4.7x | 1.86 | 63.7% | 76.1% |
| Remove device and geolocation features | 3.8% | 4.6x | 1.99 | 63.1% | 74.8% |
| Audit-calibrated thresholds | 0.4% | 0.6x | 0.95 | 55.5% | 86.0% |

Reweighing and feature removal gave limited gains. Audit-calibrated thresholds (0.30 urban, 0.46 peri-urban, 0.52 rural) cut rural FPR sharply but reduced overall recall by 6.8 points and rural recall from 74.5% to 52.9%. The company should therefore prioritise better identity capture, vendor testing, retraining with reweighing and human review of borderline cases. Group-specific thresholds should be a temporary measure only, after governance and legal review.

## 8. Prioritised Recommendations

| Priority | Action | Owner | Timeline |
| --- | --- | --- | --- |
| 1 | Complete DPIA, document lawful bases, set cross-border safeguards | DPO | Before live use |
| 2 | Introduce human review and customer appeals for adverse decisions | Fraud Operations | Before pilot |
| 3 | Investigate identity-capture bias and reassess vendors | Data Science, Vendor Risk | Before pilot |
| 4 | Set fairness requirements using verified audit samples | Data Science | Before pilot, then quarterly |
| 5 | Provide reason codes, customer notices and model documentation | Compliance | Before pilot |
| 6 | Establish governance committee, RACI and incident procedures | CRO and CISO | Before pilot |
| 7 | Monitor drift, override rates and customer harm | Data Science | From pilot start |
| 8 | Review EU requirements before expansion or credit use | General Counsel | Before expansion |

## 9. Deployment Recommendation

**Decision: conditional approval for a controlled pilot; no approval for fully automated adverse decisions.**

The baseline shows real fraud-detection value (about 62% recall, 74% precision), but the rural false-positive gap, biometric processing and automated-decision risk must be addressed first. Five conditions apply before launch:

1. DPIA completed and lawful bases approved.
2. Fairness testing passed on verified audit data.
3. Human review and customer appeals operating.
4. Reason codes and customer notices in place.
5. Governance committee and incident escalation established.

During the pilot, operations should be paused or reviewed if an S1 incident occurs, a fairness-gate failure stays unresolved for 30 days, or override rates show systematic errors. Any EU expansion needs a separate legal assessment.

## 10. Limitations and Declarations

Synthetic data demonstrate the method, not real fraud rates or customer impact. The rural test group has only 740 records (51 fraud cases). One model family, threshold and random seed were tested, and intersectional groups (for example, rural women) were not analysed. The 0.80–1.25 range is an internal benchmark, not a Nigerian legal standard. Likelihood and impact ratings are analyst judgements. Legal provisions and EU dates should be verified against official sources before compliance use.

**AI-assistance declaration:** Claude (Anthropic) assisted with drafting text, preparing code and researching legal developments. Archana reviewed, executed and verified the work. All data are synthetic.

## References

Barocas, S., Hardt, M. and Narayanan, A. (2023) *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org

Chouldechova, A. (2017) 'Fair prediction with disparate impact', *Big Data*, 5(2), pp. 153–163.

European Union (2024) *Regulation (EU) 2024/1689 – Artificial Intelligence Act*. https://ai-act-service-desk.ec.europa.eu/en/ai-act-explorer

European Union (2026) *Regulation (EU) 2026/1744 amending Regulation (EU) 2024/1689 (Digital Omnibus on AI)*, Official Journal of the European Union, 24 July 2026. https://eur-lex.europa.eu

Federal Republic of Nigeria (2023) *Nigeria Data Protection Act 2023*. https://www.dataguidance.com/sites/default/files/data\_protection\_act\_2023.pdf

Hardt, M., Price, E. and Srebro, N. (2016) 'Equality of opportunity in supervised learning', *Advances in Neural Information Processing Systems*, 29.

Kamiran, F. and Calders, T. (2012) 'Data preprocessing techniques for classification without discrimination', *Knowledge and Information Systems*, 33(1), pp. 1–33.

Mehrabi, N. et al. (2021) 'A survey on bias and fairness in machine learning', *ACM Computing Surveys*, 54(6), Article 115.

NIST (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf

Nigeria Data Protection Commission (2025) *NDPA General Application and Implementation Directive (GAID) 2025*. https://ndpc.gov.ng/wp-content/uploads/2025/07/NDP-ACT-GAID-2025-MARCH-20TH.pdf

Nigeria Data Protection Commission (n.d.) *Official resources*. https://ndpc.gov.ng/

OECD (2019, amended 2024) *OECD AI Principles*. https://www.oecd.org/en/topics/ai-principles.html

UNESCO (2021) *Recommendation on the Ethics of Artificial Intelligence*. https://www.unesco.org/en/legal-affairs/recommendation-ethics-artificial-intelligence

White & Case (2026) *EU AI Omnibus enters into force, amending the AI Act*. https://www.whitecase.com/insight-alert/eu-ai-omnibus-enters-force-amending-ai-act

## Appendix A: Evidence Repository

| Evidence | Location |
| --- | --- |
| Synthetic dataset and data dictionary | `data/synthetic_applicants.csv`, `data/DATA_DICTIONARY.md` |
| Model and fairness code | `src/sfa_fairness/`, `scripts/run_all.py` |
| Results and metrics | `results/tables/`, `results/metrics_summary.json` |
| Figures and risk heat-map | `results/figures/` |
| Risk register | `risk-register/` |
| Methodology and legal documentation | `docs/` |
| Tests and CI | `tests/`, `.github/workflows/ci.yml` |

## Appendix B: Reproduction Instructions

Requires Python 3.10 or later.

```bash
python -m pip install -e ".[dev]"
python scripts/run_all.py
pytest -q
```

**Configuration:** random seed 20260611; 20,000 records (14,000 training, 6,000 testing); threshold 0.30; 1,000 bootstrap resamples.
