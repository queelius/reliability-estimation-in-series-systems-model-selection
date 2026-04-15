# Methodology Auditor Report

**Date**: 2026-02-24
**Paper**: Model Selection for Reliability Estimation in Series Systems

## Simulation Design Assessment

### Overall Design: Competent but Limited

The simulation infrastructure is well-engineered (vectorized log-likelihood, analytical gradients, resume logic, Wilson confidence intervals for binomial proportions). The code quality is high. However, the experimental design has significant gaps.

### Issue M1: Synthetic Shape Generation (Critical)

**Location**: results/lrt/divergence/lrt-divergence.R, lines 14-38

The `generate_shapes_with_cv` function creates shape vectors by evenly spacing values around a mean to achieve a target CV. This produces a very specific pattern of heterogeneity (uniform, symmetric around the mean). Real-world systems have arbitrary, potentially asymmetric shape heterogeneity.

**Problem**: The CV threshold findings (e.g., "CV < 5% is safe") depend on HOW the CV is achieved, not just its value. A system with one outlier component (k_3 = 0.5, others ~1.2) has very different power characteristics than one with smoothly varying shapes (1.0, 1.1, 1.2, 1.3, 1.4) even at the same CV.

The main paper also has a second approach (Section 5.4): varying k_3 only while keeping others fixed. This produces asymmetric heterogeneity driven by a single component. The two approaches (symmetric spread vs. single-component outlier) are not reconciled or compared.

**Recommendation**: Test at least 2-3 different patterns of heterogeneity at each CV level. Show that the CV threshold is robust to the pattern, or acknowledge it is not.

### Issue M2: Fixed Baseline Configuration (Major)

All experiments use a single baseline system (Table 1) or minor variants. The shapes range from 1.13 to 1.26 (all slightly increasing hazard) and scales from 840 to 994. Results may not generalize to:
- Systems with higher shape values (k > 2, strong wear-out)
- Systems with mixed failure modes (some k < 1, some k > 1)
- Systems with widely differing scales
- Systems with more than 8 components

The paper should at minimum test 2-3 qualitatively different baseline configurations.

### Issue M3: Replication Count (Minor)

500 replications per condition is adequate for estimating rejection rates around 5-10% but produces wide confidence intervals. At 500 reps, the standard error for a rejection rate of 5% is sqrt(0.05*0.95/500) = 0.0097, giving a 95% CI of approximately [0.031, 0.069]. This makes it hard to distinguish a true 5% from a true 3% or 7%.

For the Type I error validation specifically, 500 reps is marginal. The Wilson CIs in Table 4 confirm this -- they are quite wide. Standard practice for Type I error validation is 5000-10000 replications.

### Issue M4: Non-Convergent Fits Silently Dropped (Major)

**Location**: lrt-divergence.R, line 139: `if (sol_F$convergence != 0) next`

Non-convergent fits are skipped without reporting the fraction discarded. If convergence failures are systematic (e.g., more common at small n or extreme parameters), this introduces selection bias -- the reported rejection rates are conditional on both models converging, which may not represent what happens in practice.

The paper should report: (a) the fraction of non-convergent replications per condition, and (b) sensitivity analysis for how including/excluding borderline cases affects results.

### Issue M5: Single k_3 Perturbation Axis (Major)

The divergence analysis in Section 5.4 varies only k_3 (one component) to generate heterogeneity. This creates a specific power profile: the LRT is testing whether a single component differs. A more general test would vary multiple components simultaneously.

The results may overstate the difficulty of detection when only one component deviates (the LRT effectively has 1 functional degree of freedom even though it has m-1 nominal degrees). Conversely, when multiple components deviate, the power structure changes.

### Issue M6: No Real Data (Major)

The paper is entirely simulation-based with no application to real data. While simulation studies are valuable, a single real-data example would:
- Demonstrate the method's practical applicability
- Show whether the CV < 5% threshold is relevant in practice
- Ground the "well-designed system" concept in reality

### Issue M7: Reduced Model Fitting Strategy (Minor)

**Location**: sim_utils.R, lines 237-259

The reduced model is fit with L-BFGS-B followed by Nelder-Mead, taking the better result. The full model is fit only with L-BFGS-B. This asymmetry could introduce bias: the reduced model gets a second chance to find a better optimum, potentially making Lambda smaller (less likely to reject H0). In practice, the effect is likely small, but it would be better to apply the same two-stage strategy to both models.

### Issue M8: Masking Mechanism (Minor)

The candidate set generation mechanism (each component independently included with probability p) is specific and may not represent real masking patterns. In practice, masking often arises from physical proximity or shared symptoms, creating correlated candidate sets. The paper's results are valid for this specific masking model but may not generalize.

## Statistical Rigor

### Confidence Intervals for Rejection Rates

The use of Wilson score intervals for binomial proportions is good practice (preferred over Wald intervals at extreme proportions). This is properly implemented in the Python analysis scripts.

### Multiple Testing

The paper reports rejection rates for many (CV, n) combinations without adjusting for multiple comparisons. This is acceptable for a power analysis (each combination is a separate question) but should be noted.

### Bootstrap CI Methodology

The BCa bootstrap intervals in Section 4 use 2000 bootstrap samples per replication across 1000 replications. This is computationally intensive and methodologically sound.

## Reproducibility

### Strengths
- Code is available and well-organized
- Seeds are set for reproducibility
- Resume logic allows interrupted simulations to continue
- R package dependencies are specified

### Weaknesses
- No Makefile or script to reproduce the full pipeline end-to-end
- R package versions not pinned (wei.series.md.c1.c2.c3 v0.9.0 is specified but not how to install it)
- Python dependencies (matplotlib, seaborn, pandas, numpy) not version-pinned

## Findings Summary

| # | Finding | Severity | Confidence |
|---|---------|----------|------------|
| M1 | Shape generation method creates specific symmetric pattern; CV threshold may not generalize | Critical | High |
| M2 | Single baseline configuration limits generalizability | Major | High |
| M3 | 500 replications marginal for Type I error validation | Minor | Medium |
| M4 | Non-convergent fits silently dropped; fraction not reported | Major | High |
| M5 | Only single-component perturbation tested in main analysis | Major | High |
| M6 | No real data application | Major | High |
| M7 | Asymmetric optimization strategy for full vs reduced model | Minor | Medium |
| M8 | Specific masking mechanism may not represent practice | Minor | Medium |
