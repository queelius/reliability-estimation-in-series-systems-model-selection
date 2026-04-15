# Paper Rewrite Design: Model Selection for Reliability Estimation in Series Systems

**Date**: 2026-02-24
**Decision**: Paths B + C with significant restructure

## Motivation

The current paper is a simulation report. The review identified three critical gaps:
1. Theorem 1 (Weibull closure) is textbook material, not novel
2. No consequence analysis — the paper shows the LRT *can't reject* but never asks whether misspecification *matters*
3. No actionable procedure — telling practitioners "if CV < 5%, use reduced" requires knowing CV, which requires the full model

## New Paper Structure

| # | Section | Status | Key Change |
|---|---------|--------|-----------|
| 1 | Introduction | Rewrite | Sharper motivation, expanded related work, reframed contributions |
| 2 | Model Framework | Merge+compress | Combine old Secs 2+3. Property 1 (not Theorem). Model hierarchy elevated. |
| 3 | Consequence Analysis | **NEW** | Bias in MTTF, R(t), failure probs when reduced model is misspecified |
| 4 | Likelihood Ratio Testing | Compress | Old Sec 5.4-5.6 compressed. Power analysis, Type I, factors, AIC/BIC |
| 5 | Adaptive Model Selection | **NEW** | Fit full → estimate CV → decide. Operating characteristics. |
| 6 | Conclusion | Rewrite | Integrated framework: consequences + LRT + adaptive procedure |
| A | Appendix | Relocate | Old Section 4 figures, power tables, convergence diagnostics |

## New Simulations

### Simulation A: Consequence Analysis (`results/consequence/`)

**Question**: When the reduced model is used but shapes are heterogeneous, how wrong are predictions?

**Design**:
- CV values: 0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20, 0.30
- Sample sizes: 100, 500, 1000, 5000
- 500 replications per condition
- Masking p = 0.215, censoring q = 0.825

**Metrics per replication**:
- System MTTF bias: (MTTF_reduced - MTTF_true) / MTTF_true
- System R(t) bias at t = MTTF_true/2, MTTF_true, 2*MTTF_true
- Component failure probability bias: |P_j_reduced - P_j_true|

**Implementation**: Reuses `sim_utils.R`. For each rep:
1. Generate data from full model (heterogeneous shapes at target CV)
2. Fit both full and reduced models
3. Compute prediction metrics under each model
4. Compare to ground truth

### Simulation B: Adaptive Procedure (`results/adaptive/`)

**Question**: Does a data-driven model selection procedure outperform always-full or always-reduced?

**Design**:
- CV values: 0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20
- Sample sizes: 100, 500, 1000
- 500 replications per condition
- CV threshold for adaptive: calibrated from Type I error

**Strategies compared**:
1. Always-full: always use full model estimates
2. Always-reduced: always use reduced model estimates
3. Adaptive: fit full → estimate CV → decide
4. Oracle: knows true CV, picks optimal model

**Metrics**: MSE of system MTTF, component MTTF bias, model selection accuracy

## References to Add

- Barlow & Proschan (1975) — Weibull closure is standard
- Meeker & Escobar (1998) — standard reliability text
- Lawless (2003) — lifetime data methods
- Wilks (1938) — LRT distribution theory
- Akaike (1974) — AIC
- Schwarz (1978) — BIC
- Burnham & Anderson (2002) — model selection framework
- Nelson (1982) — applied life data

## Key Structural Decisions

1. **Theorem 1 → Property 1**: Cite Barlow & Proschan. Retain uniqueness as a remark.
2. **Cut Section 4**: Move figures to appendix. Compress to one motivating paragraph.
3. **Split Section 5**: Model definition (→ Sec 2) + simulation study (→ Sec 4).
4. **New central contribution**: Consequence analysis (Sec 3) replaces simulation report as the heart of the paper.
5. **Adaptive procedure**: The practical deliverable. Replaces crude CV-bin framework.

## Target

- Length: ~20 pages (down from 31)
- Venue: IEEE Transactions on Reliability or RESS
- Key message: "The difference doesn't matter, and here's how to decide automatically"
