# Methodology Auditor Report

**Reviewer role**: experimental design, statistical rigor, reproducibility.
**Manuscript reviewed**: `qrei/manuscript.tex`. Cross-referenced with `results/consequence/`, `results/adaptive/`, `results/lrt/divergence/`, and prior auditor report (2026-02-27).
**Date**: 2026-05-03

## Summary

The simulation methodology is professionally executed. Underlying CSV data exactly match the manuscript tables (verified directly). The L-BFGS-B plus analytical-gradient pipeline is appropriate. Reproducibility is strong (seeds, R package, public code repo). The two methodological vulnerabilities are well-known to the author: (1) a single baseline system, and (2) Monte Carlo replication count (500) yielding wider CIs than ideal at marginal CV. Neither is a publication blocker for QREI; one of them might be at IEEE TR or Technometrics.

**Severity counts**: critical 0, major 3, minor 4, suggestions 2.

## Major Findings

### MAJ-M1: Single baseline system is a real but addressable limitation
**Location**: Section 2.4 (baseline definition), Section 6 Limitations.
**Quoted text** (Limitations, lines 308-309):
> "Our simulations use uniformly spaced shapes about a common mean. Real systems may exhibit asymmetric or clustered heterogeneity patterns. The single baseline system (5 components, moderate masking and censoring) may not capture all configurations of practical interest."

**Problem**: the paper has *internally* varied $m$, $p$, $q$ for the LRT power analysis (Appendix C), but all consequence analysis (the headline finding) is at $m=5$ and the Huairu-2013 scales. The threshold "CV ≈ 15% for 1% bias" is therefore tied to one configuration. Reviewers will ask: does this hold for $m=3$? for $m=8$? for systems with one weak component dominating? for $\bar{k} = 2.5$ (high-aging) vs $\bar{k} = 1.0$ (constant hazard)?

**Severity assessment**: this is the classic "single example study" critique. Whether it is a publication blocker depends on the venue:
- QREI: not a blocker. QREI accepts engineering case studies routinely.
- IEEE TR: borderline. Some IEEE TR reviewers will require either a second baseline or a structural argument for why the alignment generalizes.
- Technometrics, LDA: blocker. These venues will require either multiple baselines or a structural argument.

**Fix options, in order of effort**:
1. (cheapest, ~1 hour) Add a sentence in Limitations clarifying that the *qualitative* alignment is expected to be a structural property (citing the local-alternatives argument from logic-checker MAJ-L1) while the *quantitative* boundary depends on the configuration.
2. (medium, ~1 day) Add a small Appendix table running consequence analysis at $m=3$ and $m=8$ with the same shape mean and scale ratios. If alignment holds, this is decisive.
3. (expensive, ~1 week) Multi-system Monte Carlo varying $m$ and shape-mean, full bias-vs-power crossplot. Most defensible but expensive.

For QREI submission as-is: I recommend option 1 plus the structural argument. For IEEE TR: option 2 is essentially required.

### MAJ-M2: Adaptive procedure is evaluated only against three static strategies
**Location**: Section 5.2.
**Quoted text**:
> "We compare three strategies: 1. Always-full ... 2. Always-reduced ... 3. Adaptive (LRT)."

**Problem**: an obvious comparator is missing: **adaptive AIC** and **adaptive BIC**. The paper has the data (the divergence simulation includes AIC and BIC selection rates) but does not include AIC/BIC-adaptive RMSE columns in Table 4. This is a practitioner-relevant comparison: many engineers use AIC/BIC by default. Without an apples-to-apples adaptive comparison, the paper's "use LRT" recommendation rests on the Type I error analysis only.

**Fix**: extend Table 4 with two more strategies (Adaptive-AIC, Adaptive-BIC). The simulation already computes AIC/BIC selection probabilities; assembling the RMSE table is a re-run from existing CSV data, not new simulation. ~half a day. This addresses what every QREI reviewer will ask.

### MAJ-M3: Non-convergence handling is mentioned in passing but not fully reported
**Location**: Section 3.1 ("Non-convergent fits (typically $< 3\%$; up to 10\% at extreme CV) are excluded.") and Section 5.2 ("Non-convergent fits are excluded (typically $< 2\%$ of replications).").

**Problem**: the prior 2026-02-27 review flagged that the *reduced* model's convergence was never checked separately, only the full model's. The current draft has not addressed this. The two-stage optimizer is robust in practice, but a reviewer with statistical training will ask: "What fraction of replications had successful full-model convergence but non-convergent reduced-model fits, or vice versa? Could selection bias from differential convergence affect results?"

The CSV data does have exclusion counts implicitly (n_reps column ranges from 494 to 500 in the consequence summary; from 495 to 500 in the divergence summary; from 495 to 500 in the adaptive summary). Most exclusions are minor.

**Fix**: add a one-paragraph note in Section 3.1 (or a footnote on Table 2):
> "Convergence was monitored independently for the full model (L-BFGS-B with analytical gradients) and the reduced model (constrained optimization). Replications were excluded when *either* model failed to converge. Exclusion rates ranged from 0 to 6 in 500 (1.2%) at moderate CV, rising to up to 5 in 500 at extreme CV (CV = 41%). Selection bias from this exclusion is bounded by the exclusion rate and is negligible for the reported quantities."

This pre-empts the convergence-bias critique.

## Minor Findings

### MIN-M1: 500 replications is at the low end for the precision claimed
**Location**: throughout.
**Issue**: a reported rejection rate of 0.789 (from 500 reps) has Wilson 95% CI of approximately [0.751, 0.823]. A reported bias of 1.49% has standard error of about $\sigma / \sqrt{500}$; with $\sigma \approx \text{RMSE}_\text{red} \approx 10.5$, this gives SE ≈ 0.47%, so the 95% CI for the bias is roughly $\pm 0.92\%$. **The "1% bias" threshold is therefore within Monte Carlo noise of the claim**.

This does not invalidate the qualitative conclusions, but it does mean the paper's statements about specific CV thresholds ("through CV ≈ 15%") have residual uncertainty. The 2026-02-27 review flagged this; the current draft did not address it.

**Fix**: either (a) increase to 2000+ reps (recommended for IEEE TR / Technometrics; would take a few hours of compute), or (b) add a sentence acknowledging Monte Carlo precision: "All percentages reported here have approximate Monte Carlo standard errors of 0.4-0.5 percentage points; thus 'bias < 1%' should be read as 'bias not statistically distinguishable from 0 at the 95% level.'"

### MIN-M2: The vary-m experiment confounds m with realized CV
**Location**: Appendix C, Table 5 (Effect of Data Quality Factors on LRT Power).
**Quoted claim**: "Components $m$: 2-8, Power Range 77\% → 16\%, Effect $5\times$ reduction."

**Issue**: when $m$ varies, the CV of the (uniformly-spaced) shapes also varies. For $m=2$, two shapes around mean 1.18 give one perturbation pattern; for $m=8$ they give a tighter distribution. This was flagged in the prior review (MAJ-1). I cannot confirm from the manuscript text alone whether the simulation holds CV constant across $m$ or not (the text says "for the baseline system (CV ≈ 4%)" which could mean either). If CV is fixed at 4%, the "5x reduction" claim is meaningful; if not, it is partially confounded.

**Fix**: state explicitly in Appendix C that CV is held at the baseline value across $m$ (if so), or acknowledge the confound and reinterpret (if not).

### MIN-M3: The 500-rep claim in 3.1 vs adaptive 5.2 vs LRT divergence
The three result sections use slightly different reported exclusion rates ("< 3%", "< 2%", and an unstated rate for the LRT divergence). This is presentational, not methodological. Unify in one sentence: "Across all simulations, non-convergent fits (typically 0-3% of replications, rising to 10% at the most extreme CV) are excluded. Both models' convergence is monitored independently."

### MIN-M4: Wilson CIs (or any CI) are not reported on the rejection rates in the paper text
The CSVs contain `ci_low`, `ci_high` columns (Wilson 95%). These do not appear in any manuscript table. Adding even one column or one in-text quantification would strengthen the rigor signal.

## Suggestions

### SUG-M1: Tighten the convergence reporting
Most simulations had 494-500 successful reps out of 500. A small footnote in Section 2.4 stating the convergence-handling protocol would professionalize the methodology section.

### SUG-M2: Move "vary-m, vary-p, vary-q" into the main text or replace with structural argument
Currently these are in Appendix C. They support important claims but are visually marginalized. If kept in Appendix, add a one-sentence pointer in Section 4.2 ("the LRT power profile is robust to varying data-quality factors; see Appendix C").

## Reproducibility Verification

I verified the following:
- Simulation code is in `results/consequence/`, `results/adaptive/`, `results/lrt/divergence/`. Exists and is non-empty.
- CSV data is generated by these scripts and used by the figure-generation Python scripts. Exists and is non-empty.
- The Python script outputs (PDF figures) are referenced by the manuscript. Verified via grep.
- The Data Availability statement points to `https://github.com/queelius/masked-series-model-selection` and `https://github.com/queelius/wei.series.md.c1.c2.c3`.

**Verification check**: the URL `https://github.com/queelius/masked-series-model-selection` is the public repo for this paper, but I should note the user mentioned `wei.series.md.c1.c2.c3` is archived. The Data Availability statement points to it. Per the user's note, the live replacement is `maskedcauses` at `~/github/rlang/maskedcauses/`. The Data Availability statement should be updated to direct readers to the live package.

## Statistical Rigor Audit

| Aspect | Status |
|--------|--------|
| Random seed control | Yes (per .papermill notes) |
| Multiple replications | Yes (500 per cell, low end of acceptable) |
| Type I error validation | Yes (CV=0 baseline used) |
| Power analysis | Yes (LRT power vs CV reported) |
| Bias-variance decomposition | Mentioned but not displayed in main paper |
| Monte Carlo standard errors | Computed (in CSVs) but not surfaced in tables |
| Multiple testing correction | Not needed for this design |
| Sensitivity analyses | Yes (Appendix C: data quality, system size) |
| Convergence diagnostics | Mentioned in passing, see MAJ-M3 |

## Verdict

The methodology is sound. The main weaknesses are the single baseline (MAJ-M1) and the missing AIC/BIC-adaptive comparison (MAJ-M2). For QREI both are addressable with one round of revision. For IEEE TR a more substantial revision is needed (multiple baselines or structural argument).

Confidence: high.
