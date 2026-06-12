---
title: "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"
stage: draft
format: latex
authors:
  - name: "Alexander Towell"
    email: "lex@metafunctor.com"
    orcid: "0000-0001-6443-9897"

thesis:
  claim: "Misspecification consequence and statistical detectability are structurally decoupled in sample size and coupled in heterogeneity for common-shape Weibull series models fit to masked, censored data. (i) The reduced model's relative MTTF bias is a sample-size-independent population quantity scaling as c_B*CV^2 at leading order (delta method; empirically c_B ~ 0.30-0.35, so bias < 1% through CV ~ 18%; verified n-stable across a 50x range of n). (ii) LRT detectability is governed by a noncentral chi-square with ncp ~ c_D*n*CV^2 (Le Cam local asymptotics; empirically c_D = 0.50 +/- 0.03 across n in [1000, 10000] and CV in [2.7%, 27%] at baseline masking p=0.215, censoring q=0.825), so the detectable-CV threshold falls as CV50 ~ 3.5/sqrt(n); log-log slope -0.468 vs theoretical -0.5. Corollary (two-regime safety): for n >~ 1000 the LRT rejects with >= 80% power before bias crosses 1%; for n <~ 500 the test under-detects but sampling error (4-10% RMSE) dominates the <= 3% specification bias, so model choice is second-order; over-rejection at very large n is harmless because switching to the full model costs nothing first-order. (iii) Zero-first-order-gain proposition: at any common-shape point (any scales), the common-shape constraint yields exactly zero first-order variance reduction for any functional of the system lifetime distribution (MTTF, R(t), quantiles); proved for complete data via the (k, eta=lambda^-k) parameterization, conjectured + empirically verified under masking/censoring (notes/zero-first-order-gain.md). Hence second-order effects decide the finite-n MSE ordering, and they favor the FULL model: at CV=0 the reduced model has strictly higher MTTF MSE (paired t=-3.65 at n=100, replicated in an independent dataset; ~7% RMSE penalty at n=100, ~1% at n=500-1000, vanishing at n=5000 as first-order theory requires). The case for the common-shape model is Weibull closure and engineering-adequate predictions, never statistical efficiency."
  novelty: "First consequence analysis (engineering significance vs statistical detectability) for common-shape simplification of Weibull series systems under masked, censored data. Prior masked-data work (Usher, Lin-Guess, Sarhan, Tan, Guo; Craiu-Lee for masked competing risks) develops estimators and selection procedures but never quantifies when simplification is safe. Three contributions: (1) decoupling result with empirically calibrated constants (bias ~ 0.3*CV^2, ncp ~ 0.5*n*CV^2, CV50 ~ 3.5/sqrt(n)) and a 1-2 page derivation (delta method + Le Cam) that converts the single-baseline simulation into formulas evaluable at any design point; (2) zero-first-order-gain proposition: the common-shape constraint provides exactly zero asymptotic variance reduction for system-level functionals, explaining why the finite-n MSE ordering favors the full model and refuting parsimony-reduces-variance for system-level prediction (upgrade over the previous 'counterexample' framing: now a theorem with the simulation as confirmation); (3) honest empirical evaluation of LRT-pretest model selection in this setting, exhibiting the classic pretest-estimator risk hump at n=100 (worst case +17% RMSE at CV=27%) and its disappearance by n=500. Threats to novelty to verify in prior-art: focused information criterion (Claeskens-Hjort) selects on a focus functional like MTTF; pretest-estimation literature (Bancroft onward) owns the risk-hump phenomenon; equivalence-testing framings of practical significance. Differentiator: none of these address masked series-system data or the Weibull-closure-motivated common-shape reduction."
  refined: "2026-06-10"

prior_art:
  last_survey: "2026-06-10"
  survey_report: ".papermill/reviews/2026-06-10/prior-art.md (18 ready BibTeX entries)"
  key_references:
    - key: claeskens2003fic
      role: "TOP NOVELTY THREAT: focused information criterion selects on focus-parameter MSE under local misspecification; Section 4.5 must engage and differentiate (fixed vs local misspecification)"
    - key: bancroft1944
      role: "Pretest estimation origin; Section 5's adaptive procedure is a pretest estimator, the n=100 risk hump is Bancroft's phenomenon (with judge1978, danilov2004, leeb2005)"
    - key: mccool1975
      role: "Closest prior art on testing equal Weibull shapes (multi-sample, no masking, no consequence analysis)"
    - key: hart2024
      role: "IEEE TR 2024/2025: estimation under common-shape Weibull competing risks assuming the model true; benign venue competitor, corroborates IEEE TR fit"
    - key: aitchison1958
      role: "Constrained-MLE asymptotics; foundation for the zero-first-order-gain proposition"
    - key: pascual2005
      role: "Cross-family Weibull misspecification MLE bias precedent (no series system, no masking)"
    - key: towell2025masked
      role: "Foundation paper: C1-C2-C3 likelihood framework (replaces stale towell2023reliability citation)"
    - key: towell2025weibull-fim
      role: "Sibling paper: closed-form FIM and masking invariance for homogeneous Weibull series; supplies the asymptotic-variance theory underlying the decoupling"
    - key: barlow1975
      role: "Weibull closure property (Property 1 in our paper)"
    - key: Huairu-2013
      role: "Baseline 5-component system configuration"
    - key: wilks1938
      role: "LRT asymptotic theory"
    - key: vandervaart2000
      role: "Le Cam contiguous alternatives, used in Section 4.5 detection-threshold derivation"
    - key: casella2002
      role: "Delta method, used in Section 4.5 bias-scaling derivation"
    - key: White-1982
      role: "MLE under model misspecification, cited for the MSE counterexample mechanism"
    - key: Craiu-2005
      role: "Closest comparator: model selection for masked competing-risks (non-series-system setting)"
    - key: burnham2002
      role: "Information-theoretic model selection (AIC/BIC)"
  gaps: "Sarhan-2001/2004, Tan-2005/2007, Usher-1996, Lin-1996 remain in refs.bib but uncited (still open per 2026-06-10 review). Genuinely novel after the 2026-06-10 survey: consequence-vs-detectability decoupling under fixed misspecification in the masked series setting; zero-first-order-gain proposition (no prior derivation found); calibrated safe-zone constants under masking/censoring. Referee question to pre-answer in the paper: why not apply FIC to MTTF directly."

experiments:
  - name: "Consequence analysis"
    description: "MTTF bias, R(t) bias, relative efficiency across CV={0-30%}, n={100,500,1000,5000}, 500 reps"
    status: complete
    location: "results/consequence/"
  - name: "Adaptive model selection"
    description: "Always-full vs always-reduced vs adaptive-LRT vs adaptive-CV across CV={0-20%}, n={100,500,1000}, 500 reps"
    status: complete
    location: "results/adaptive/"
  - name: "LRT divergence analysis"
    description: "Type I error and power curves vs shape CV across n={100,500,1000,5000,10000}, 500 reps"
    status: complete
    location: "results/lrt/divergence/"
  - name: "Vary m (system complexity)"
    description: "LRT behavior across m={2,3,4,5,6,7,8} components"
    status: complete
    location: "results/lrt/vary_m/"
  - name: "Vary p (masking probability)"
    description: "LRT across p={0.05,0.10,...,0.70}"
    status: complete
    location: "results/lrt/vary_p/"
  - name: "Vary q (censoring level)"
    description: "LRT across q={0.50,0.60,...,1.00}"
    status: complete
    location: "results/lrt/vary_q/"
  - name: "Scale sensitivity (bootstrap CIs)"
    description: "MLE behavior and coverage under varying component 3's scale"
    status: complete
    location: "results/5_system_scale3/"
  - name: "Shape sensitivity (bootstrap CIs)"
    description: "MLE behavior and coverage under varying component 3's shape"
    status: complete
    location: "results/5_system_shape3/"
  - name: "Ideal case baseline"
    description: "No masking/censoring (p=0, q=1) for 2-component system"
    status: complete
    location: "results/lrt/nomasking/"
  - name: "AIC/BIC comparison"
    description: "LRT vs AIC vs BIC model selection across all experiments"
    status: complete
  - name: "Individual component reduction tests"
    description: "Single-component LRT reductions (reduced1, reduced2, reduced3)"
    status: complete
    location: "results/lrt/reduced1/, results/lrt/reduced2/, results/lrt/reduced3/"
  - name: "Theoretical scaling verification"
    description: "Verify O(CV^2) bias scaling (delta method) and 1/sqrt(n) detection threshold (Le Cam) against existing simulation data; basis for new Section 4.5"
    status: "verified 2026-06-10 (ncp = 0.50 +/- 0.03 * n * CV^2; CV50 ~ 3.5/sqrt(n); bias ~ 0.30-0.35 * CV^2); Section 4.5 prose not yet written"
    location: "notes/verify-thesis-claims.py, results/lrt/divergence/, results/consequence/"
  - name: "Zero-first-order-gain proposition"
    description: "Constraint yields zero first-order variance reduction for system functionals at any common-shape point; complete-data derivation sketch + FIM-projection numerics; masked-case proof pending (papermill:proof)"
    status: "verified numerically 2026-06-10; complete-data sketch done; masked-case proof and population KL-projection bias curve still to do"
    location: "notes/zero-first-order-gain.md, notes/verify-zero-gain.py"

venue:
  target: "IEEE Transactions on Reliability"
  switched_from: "Quality and Reliability Engineering International (2026-05-04, after thesis refinement added structural derivation)"
  candidates:
    - name: "IEEE Transactions on Reliability"
      fit: "EXCELLENT"
      if: 6.68
      quartile: Q1
      notes: "Upgraded from GOOD after thesis refinement. Audience matches both engineering framing and structural rigor (delta method + Le Cam). Format conversion to 4-column IEEEtran is mechanical; 11pp draft compresses to ~8pp."
    - name: "Quality and Reliability Engineering International"
      fit: "GOOD"
      if: 2.8
      quartile: Q2
      notes: "Strong fallback. Excellent topical fit; structural derivation may be over-target for typical QREI reviewer pool but acceptable. Existing cover letter and submission package can be reused."
    - name: "Lifetime Data Analysis"
      fit: "GOOD"
      if: 1.0
      quartile: Q2
      notes: "Statistician audience values delta-method/Le Cam derivation. Engineering framing is a slight mismatch. Companion FIM paper also targeting LDA, so same-issue submission carries duplication risk."
    - name: "Technometrics"
      fit: "MODERATE"
      if: 3.42
      quartile: Q1
      notes: "Would need the structural derivation to be more than the planned 1-2 page sketch; stretches scope beyond current rework plan."
  notes: "Strategy: complete the ~3-day rework (add Section 4.5 deriving O(CV^2) bias and 1/sqrt(n) detection scaling, restructure §3 to elevate MSE counterexample, reframe §5 as empirical evaluation, citation hygiene), then mint Zenodo DOI in parallel with IEEE TR submission. Fallback: QREI (no further format conversion needed) then LDA."

review_history:
  - date: "2026-06-10"
    agent: "papermill (inline lead-session review + surveyor agent; multi-agent orchestrator killed twice by account spend limit)"
    verdict: "MAJOR REVISION toward thesis v4 (rework confirmed as the right move)"
    notes: "Data-verification-first review. New findings: 1 critical (C2 assumption missing from Section 2.2 while Eq. 3 requires it), 7 major (White-1982 miscitation on the MSE mechanism, unqualified abstract alignment claim, wrong AIC mechanism in Appendix B, specification-vs-estimation bias conflation, MSE counterexample missing its n=5000 confirmation and error bars, unproved uniqueness claim, dropped R(t) results), 9 minor, 4 suggestions. All 2026-05-03 findings re-verified still open (draft unchanged since 2026-02-28). Every numeric claim in the draft re-verified against CSVs (ledger in review). Prior-art survey: FIC is top positioning threat; pretest literature owns the risk hump; McCool 1975 and Hart 2024/2025 must-cites; zero-first-order-gain proposition appears genuinely novel; 18 BibTeX entries ready. Reports at .papermill/reviews/2026-06-10/."
  - date: "2026-02-24"
    agent: "papermill:reviewer"
    verdict: "MAJOR REVISION"
    notes: "Theorem 1 is textbook, no consequence analysis, reads as simulation report. Led to full restructure."
  - date: "2026-02-25"
    agent: "papermill:reviewer"
    verdict: "MINOR REVISION"
    notes: "1 critical (30k claim unsupported), 5 major (CV labeling, MSE claim, units, convergence, shape generation). All fixed."
  - date: "2026-05-03"
    agent: "papermill:area-chair (multi-specialist)"
    verdict: "MINOR REVISION"
    notes: "6 specialists + literature context. Verdict: submit to QREI as planned. 1 critical (stale ecosystem citations: towell2023reliability should be towell2025masked, missing FIM sibling paper, archived R package), 8 major (single-baseline limitation, alignment observed but not derived, MSE surprise undersold, adaptive procedure framing, related work thin, AIC/BIC adaptive comparators missing, qrei artifacts not gitignored, neutral title), 11 minor, 9 suggestions. Numerical claims verified against simulation CSVs (all match). Reports at .papermill/reviews/2026-05-03/."
---

## Format

- **Source:** `paper/paper.tex` and `qrei/manuscript.tex` (11pp each; differ by ~131 diff lines: citation style, ORCID block, Data Availability statement, bibliography style). Rework target: `paper/paper.tex` will be reformatted to IEEEtran 4-column for IEEE TR; `qrei/` retired post-switch.
- **Bibliography:** `paper/refs.bib` (24 entries, IEEEtranN style via natbib)
- **Build:** `cd paper && make` (latexmk via Makefile)
- **PDF:** `paper/paper.pdf` (11 pages, built 2026-02-26; to be regenerated post-rework)
- **Figures:** 12 included figures from `paper/image/`

## Structure (post-rework target)

| # | Section | Content |
|---|---------|---------|
| 1 | Introduction | Turbine motivation, related work (expanded with Sarhan/Tan/Usher/Lin), 2 contributions: decoupling theorem, MSE counterexample |
| 2 | Model Framework | Weibull series, masked/censored data, common-shape model (Property 1), model hierarchy, baseline system |
| 3 | Consequence Analysis | Prediction metrics, MTTF/R(t) bias results, **MSE counterexample at CV=0 elevated to co-headline finding**, bias-variance decomposition |
| 4 | Likelihood Ratio Testing | LRT formulation, Type I error, power analysis; bridge to Appendices C-D |
| **4.5** | **Theoretical Justification (NEW)** | **Delta-method derivation that bias = O(CV^2) and is sample-size-independent. Le Cam contiguous-alternatives derivation that detectable CV threshold = 1/sqrt(n). Decoupling theorem statement and proof. Verification against simulation CSVs from §3-4.** |
| 5 | Empirical Evaluation of LRT-Based Selection | Reframed from "Adaptive Model Selection" per 2026-05-03 review. Honestly positioned as empirical evaluation of textbook LRT-for-nested-models in this masked-data setting (not a new procedure). 4-strategy comparison; AIC/BIC-adaptive comparators added. |
| 6 | Conclusion | Decoupling result, MSE counterexample, LRT calibration, limitations (single-baseline objection now structurally addressed), future |
| A | MLE Sensitivity | Scale and shape perturbation effects on MLE |
| B | Ideal Case | No masking/censoring baseline |
| C | Data Quality Effects | Masking, censoring, system complexity effects on LRT power |
| D | Information Criteria | AIC/BIC comparison with LRT |

## Key Findings

1. **Decoupling theorem (co-headline)**: misspecification bias is sample-size-independent and O(CV^2) at leading order; LRT detection threshold scales as 1/sqrt(n) at fixed CV. *Different mechanisms, not different growth rates.* Replaces the original "bias grows sub-linearly, power super-linearly" framing flagged as technically imprecise by the 2026-05-03 review.
2. **MSE counterexample (co-headline)**: full model has lower MTTF MSE than reduced **even when shapes are truly equal (CV=0)** at n ≤ 1000. Mechanism: common-shape constraint amplifies shape estimation error through the nonlinear MTTF functional. Refutes parsimony-reduces-variance for system-level predictions.
3. **Practical safe zone**: MTTF bias < 1% through actual CV ≈ 14%; 1% threshold not crossed until CV ≈ 20%. Empirical confirmation of the structural decoupling.
4. **LRT well-calibrated** (4.6-6.8% Type I error at α=0.05) where AIC is liberal (~2x) and BIC over-conservative (~0%).
5. **Empirical evaluation of textbook LRT selection**: RMSE within 2.5% of always-full at n ≥ 500 (8-18% at n = 100). Reframed from "adaptive procedure" (over-claimed novelty per 2026-05-03 review) to honest evaluation of a standard procedure that the decoupling result predicts should perform well.

## Simulation Infrastructure

- **Baseline:** 5-component Weibull series, shapes k ~ 1.13-1.26, scales lambda ~ 840-994
- **Sample sizes:** 50 to 30,000
- **Default masking:** p = 0.215
- **Default censoring:** q = 0.825
- **Replications:** 500 per condition
- **Pipeline:** R scripts -> CSV -> Python analysis -> PDF figures -> LaTeX
- **Shared utilities:** `results/sim_utils.R`

## Related Work (Ecosystem)

### Foundation Paper (`~/github/masked/masked-causes-in-series-systems/`)
- C1-C2-C3 framework. Citation key `towell2025masked` (DOI 10.5281/zenodo.18725577). Replaces stale `towell2023reliability` references throughout the manuscript per 2026-05-03 review.

### Sibling Paper: Weibull Masked FIM (`~/github/masked/weibull-masked-fim/`)
- Closed-form Fisher information matrix and masking invariance theorem for homogeneous Weibull series. Citation key `towell2025weibull-fim`. Supplies the asymptotic-variance theory backing the empirical decoupling. Cross-citation to be added per 2026-05-03 review.

### Expo-Masked-FIM (`Zenodo 10.5281/zenodo.18344335`, published; no local checkout)
- Exponential model FIM. Bottom of nesting chain.

### R Packages
- `maskedcauses`: high-level masked-causes likelihood with closed-form Exp/Weibull (replaces archived `wei.series.md.c1.c2.c3` per 2026-05-03 review).
- `algebraic.mle`: Numerical MLE optimization, post-estimation inference.
- Legacy: `wei.series.md.c1.c2.c3` (archived; existing simulation CSVs were generated against this version and remain valid).

## Log

- **2026-06-11**: Comprehensive review session completed (thesis -> prior-art -> review -> synthesis). Prior-art surveyor report and unified review at .papermill/reviews/2026-06-10/ (review.md, prior-art.md). Verdict: MAJOR REVISION toward v4; rework checklist in review.md maps each item to its v4 thesis element. Multi-agent reviewer orchestrator was killed twice by the account monthly spend limit; review completed inline by the lead session instead (specialist coverage preserved: logic, methodology, prose, citations, novelty, format; all numeric claims re-verified against CSVs). Paper builds clean at 11pp. Notable: working tree still uncommitted since 2026-02-28 (recommend committing before rework); qrei artifacts still not gitignored.
- **2026-06-10**: Thesis refinement v4 via papermill:thesis (data-verification mode). All three v3 claims checked against simulation CSVs with paired MC tests (notes/verify-thesis-claims.py). (a) Detection scaling confirmed sharply: ncp = (0.50 +/- 0.03)*n*CV^2, CV50 ~ 3.5/sqrt(n), log-log slope -0.468 vs -0.5 theoretical. (b) Bias scaling: exponent ~ 2.15 at n=5000 over CV 5-41%, coefficient ~ 0.30-0.35; n=100 column contaminated by additive finite-sample estimation bias (visible at CV=0: +0.36%), which the draft never separates from specification bias. (c) MSE counterexample: real and replicated (consequence t=-3.65 at n=100; adaptive dataset t=-4.82, -3.07, -2.32) but vanishes at n=5000 (t=+0.24) consistent with first-order theory; mechanism is variance (VarR=417 > VarF=348 at n=100), not bias. NEW RESULT: zero-first-order-gain proposition derived (exact for complete data, any scales, via (k, eta) parameterization; numerically gap ~ 1e-5 even at scales 1500..300) and recorded in notes/zero-first-order-gain.md; upgrades the MSE 'surprise' from counterexample to theorem-corollary. v3's 'safe zone for any practical n' corrected to a two-regime safety statement (detection-led for n >~ 1000, noise-dominance for n <~ 500, with the honest pretest hump at n=100). Pretest-estimator and FIC literatures flagged as novelty threats for prior-art. IMPORTANT REPO STATE: working-tree paper.tex/qrei manuscript (mtime 2026-02-28, uncommitted) is the condensed 11pp draft the 2026-05-03 review evaluated; git HEAD still holds the longer Feb-26 draft; the planned v3 rework (Section 4.5 etc.) was never executed, so the draft still argues the v2 'alignment' thesis.
- **2026-02-17**: Initialized papermill from existing draft.
- **2026-02-18**: Thesis refinement: tightened CV boundary from <10% to <5% for strong robustness claim.
- **2026-02-24**: Major rewrite after review. New title and structure: consequence analysis (Sec 3) + adaptive selection (Sec 5) as new contributions. Property 1 replaces Theorem 1. Old Sec 4 moved to Appendix A. Added 8 references.
- **2026-02-24**: Simulations complete. Filled in Sections 3.3-3.4 and 5.3-5.4 with results. Paper builds cleanly at 19 pages.
- **2026-02-25**: Second review (MINOR REVISION). Fixed: 30k claim, CV labeling, MSE "all conditions" overstatement, Table 3 units, convergence rates, limitations paragraph.
- **2026-02-26**: Thesis refinement. Restructured around bias-detectability alignment as central insight. Strengthened CV boundary from <10% to ~15%. Fixed n=100 adaptive overhead (8-18%, not 8-10%). 20 pages.
- **2026-05-03**: papermill:area-chair multi-specialist review (verdict MINOR REVISION). 1 critical (citation hygiene), 8 major, 11 minor. Reports at `.papermill/reviews/2026-05-03/`. Bonus finding: page-count metadata wrong (claimed 20pp/10pp; both PDFs are actually 11pp).
- **2026-05-04**: Thesis refinement v3 via papermill:thesis (Socratic). Decoupling theorem promoted to co-headline with MSE counterexample; "rate asymmetry" framing replaced by structural decoupling (bias is sample-size-independent specification effect; detection scales as 1/sqrt(n) under Le Cam contiguity). Adaptive procedure demoted from "contribution" to "empirical evaluation of textbook LRT-for-nested-models" per honesty principle. Venue switched from QREI primary to IEEE Transactions on Reliability primary (IF 6.68, Q1) on the strength of the new structural derivation. Plans: add Section 4.5 "Theoretical Justification" (delta method + Le Cam, ~1-2 pages); restructure §3 to elevate MSE counterexample; reframe §5; citation hygiene; mint Zenodo DOI in parallel with submission. Estimated rework: ~3 days. Title revision deferred to manuscript rework (current "When Does Model Simplification Matter?" candidate replacements: "Detection Outpaces Bias: Common-Shape Weibull Series Models with Masked Data" or similar).
