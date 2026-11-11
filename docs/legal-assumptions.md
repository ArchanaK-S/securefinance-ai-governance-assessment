# Legal and regulatory assumptions (Task 3 support)

*Educational assessment, not legal advice. Verify section numbers against official texts before reliance.*

## Scenario assumptions
1. SecureFinance Africa is incorporated and operating in **Nigeria** and processes personal data of individuals in Nigeria.
2. It acts as **data controller** for customer data; ID-verification and cloud vendors act as **processors**.
3. Processing includes **biometric/face-match data** (sensitive personal data), transaction profiling and automated flags.
4. **No EU establishment, EU customers or EU-based use of system output exists at launch.** International expansion is "possible later".
5. The platform's *risk assessment* output may feed credit-related decisions in future releases (to be confirmed).

## Binding versus non-binding

| Instrument | Status | Applies to SecureFinance when... | Key consequences |
|---|---|---|---|
| Nigeria Data Protection Act 2023 (NDPA) and NDPC GAID 2025 | **Binding** (Nigerian statute and regulator directive) | Always, for processing in or about individuals in Nigeria | Principles and lawful basis (ss.24-25); sensitive data conditions; DPIA for high-risk processing (s.28); rights incl. limits on solely automated decisions (s.37); security (s.39); breach notification to NDPC within 72 hours (s.40); cross-border transfer conditions (Part VIII); possible registration/DPO duties if "of major importance" |
| EU AI Act, Regulation (EU) 2024/1689 (as amended by the Digital Omnibus on AI) | **Binding in the EU; extraterritorial only with an EU nexus (Art. 2)** | SecureFinance places the system on the EU market, deploys it in the EU, or its output is used in the EU | Annex III 5(b) lists AI for creditworthiness/credit scoring of natural persons as high-risk, with an exclusion for fraud detection; 1:1 biometric verification is excluded from the remote biometric identification category. High-risk duties (risk management, data governance, human oversight, logging, transparency, conformity assessment) apply from **2 Dec 2027** for Annex III after the Omnibus |
| UNESCO Recommendation on the Ethics of AI (2021) | **Non-binding** soft law adopted by member states | Never directly; used as an ethical benchmark and a likely regulator/investor expectation | Proportionality, fairness and non-discrimination, privacy, human oversight, transparency, accountability, ethical impact assessment |
| OECD AI Principles (2019, updated 2024) | **Non-binding** intergovernmental standard | Never directly; Nigeria is not an OECD member | Inclusive growth, human rights and fairness, transparency, robustness and safety, accountability |

## Other Nigerian obligations (outside the four named instruments, noted for completeness)
Financial-sector KYC/AML rules and CBN guidance, the Money Laundering (Prevention and Prohibition) Act 2022,
and cybercrime legislation will shape retention, reporting and security design.

## Triggers that change the analysis
* Any EU customer, EU subsidiary, or EU-based deployer -> run an EU AI Act classification and GDPR review.
* Use of the risk score as the sole or main basis for credit decisions -> treat as high-risk-equivalent in all markets.
* Any new cross-border data flow or vendor -> NDPA Part VIII transfer assessment and DPIA update.
