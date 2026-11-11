# Limitations and honest caveats

* **Synthetic data prove the method, not the real system.** Injected biases make the pattern known in advance;
  the exercise demonstrates that the methodology *detects* it and that controls *reduce* it. Real data will be
  messier, and real prevalence by group is unknown.
* **Ground truth exists only because the data are synthetic.** In production, `true_fraud` is unobservable;
  the report recommends a verified random audit sample to approximate it.
* **Small subgroup counts.** Rural test n = 740, of which only 51 are true fraud cases and
  29 are false positives. Intervals are wide; point estimates should not be over-read.
* **Single model family, single operating point, single seed.** Sensitivity to threshold and seed was not
  exhaustively explored.
* **Group definitions are simplified.** Real fairness analysis would add intersections (e.g. rural x female),
  age bands and language, subject to lawful collection of sensitive attributes.
* **Disparate-impact 0.80-1.25 band** is an internal tolerance borrowed from US practice; it is not a Nigerian
  legal threshold.
* **Legal analysis** is an educational assessment, not legal advice. Statutory section numbers should be
  re-checked against the official text before reliance. EU AI Act dates reflect the Digital Omnibus on AI as of
  November 2026 and may change.
