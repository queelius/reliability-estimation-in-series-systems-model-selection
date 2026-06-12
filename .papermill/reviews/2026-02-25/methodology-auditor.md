# Methodology Auditor Report

**Date**: 2026-02-25
**Paper**: "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"

## Summary

The simulation methodology is competent and well-implemented. The R code is clear, uses analytical gradients, and follows good practices (seed management, resume logic, error handling). However, there are several methodological concerns regarding generalizability, shape generation, and statistical reporting.

## Findings

### MAJOR: Shape generation method creates artificial regularity

- **Location**: All simulation scripts (e.g., `results/consequence/consequence-analysis.R` line 62)
- **Code**: `shapes <- seq(mean_k - half_range, mean_k + half_range, length.out = m)`
- **Problem**: Shapes are generated as evenly spaced (arithmetic sequence) around the mean, with the spread calibrated to achieve the target CV. This produces a very specific, regular pattern of heterogeneity. Real systems would have arbitrary shape configurations. The uniform spacing means the "worst" and "best" components are always symmetric around the mean, which may systematically underestimate the bias that could occur with asymmetric configurations (e.g., one component with a very different shape).
- **Severity**: Major (affects generalizability)
- **Suggestion**: Include additional shape generation methods: (1) random draws from a distribution with the target CV, (2) asymmetric configurations where one component deviates while others are homogeneous. Report sensitivity to the shape generation method.

### MAJOR: Only 500 replications per condition -- binomial CIs are wide

- **Location**: All simulation scripts
- **Problem**: With 500 replications, the standard error of a rejection rate is $\sqrt{p(1-p)/500}$. At p=0.05 (Type I error), SE = 0.0097, giving a 95% CI of [0.031, 0.069]. This is adequate for the Type I error validation (Table 4 shows ranges consistent with this). However, for power comparisons at moderate rejection rates (e.g., 13% vs 15%), the uncertainty is substantial (SE ~ 0.015). The paper does not report confidence intervals for the power values in Table 5, nor for the MTTF bias values in Table 3.
- **Severity**: Major
- **Suggestion**: Report 95% binomial CIs for all rejection rates. For bias and RMSE, report bootstrap CIs or standard errors. Consider increasing to 1000+ replications for key conditions.

### MAJOR: Non-convergent fits silently dropped

- **Location**: All simulation scripts (e.g., `consequence-analysis.R` line 178: `if (sol_F$convergence != 0) next`)
- **Problem**: When the full model fails to converge, that replication is silently skipped. The paper does not report the convergence failure rate. If convergence failures are correlated with certain parameter configurations (e.g., extreme shapes, small samples), the results may be biased by survivorship. The `conv_F` column exists in the CSV but is always 0 for saved rows (by construction).
- **Severity**: Major
- **Suggestion**: Report the convergence failure rate for each condition. Discuss whether failures are random or systematic. Consider whether failed convergence cases should be handled differently (e.g., multiple restarts).

### MINOR: Reduced model fitted with mean of full model shapes as starting point

- **Location**: `sim_utils.R` line 184; consequence-analysis.R line 184
- **Code**: `k_hat <- mean(shapes_F); sol_R <- fit_reduced_model(par0 = c(k_hat, scales_F), ...)`
- **Problem**: The reduced model is initialized from the full model's MLE. This is efficient but could bias the comparison: the reduced model starts at a good point in parameter space because it uses the full model's solution. A more principled approach would use moment-based or independent starting values. The two-stage optimization (L-BFGS-B then Nelder-Mead) in `fit_reduced_model` mitigates this somewhat.
- **Severity**: Minor
- **Suggestion**: Acknowledge this design choice. Consider testing sensitivity to starting values.

### MINOR: CV metric conflates target and actual values

- **Location**: Shape generation across all scripts
- **Problem**: The paper specifies target CVs (0, 0.02, 0.04, ...) but the actual CVs differ substantially due to the uniform spacing formula: target_cv=0.10 produces actual_cv=0.137 (37% higher). The tables correctly use actual CV but the prose sometimes uses target CV (see Logic Checker report). This is a systematic mapping issue, not a random discrepancy.
- **Severity**: Minor (presentation issue, not methodology)
- **Suggestion**: Either redesign the shape generation to hit exact target CVs, or clearly document the mapping between target and actual CVs.

### MINOR: Single baseline system configuration

- **Location**: All simulations
- **Problem**: All results are based on a single 5-component baseline system from Guo et al. (2013) with shapes near 1.13-1.26 and scales near 840-994. This is a well-designed system with slight wear-out (k > 1). Results may differ for systems with k < 1 (infant mortality), k >> 1 (strong wear-out), or highly asymmetric scale parameters.
- **Severity**: Minor (affects generalizability, partially addressed by vary-m analysis)
- **Suggestion**: Add a brief discussion of generalizability limitations. The vary-m analysis is helpful but only changes the number of components, not the parameter ranges.

### SUGGESTION: Report actual number of successful replications

- **Problem**: The paper says "500 replications per condition" but some conditions may have fewer due to convergence failures. The CSV files should be checked for the actual counts.
- **Suggestion**: Report a table of actual replication counts by condition, or at minimum state the overall convergence rate.

### SUGGESTION: Consider parametric bootstrap for LRT calibration

- **Problem**: The LRT uses the chi-squared approximation. While the Type I error validation (Table 4) confirms this is adequate at the tested sample sizes, a parametric bootstrap calibration would provide exact finite-sample rejection rates and could improve power at small n.
- **Suggestion**: Mention this as a potential refinement.

## Reproducibility Assessment

- **Code availability**: R scripts and data are included in the repository
- **Seeds**: Fixed seeds with per-condition variation (good practice)
- **Resume logic**: Scripts can resume from partial runs (good for long simulations)
- **Dependencies**: Custom R packages (wei.series.md.c1.c2.c3, md.tools) are required -- these should be version-pinned
- **Overall**: Reproducible given access to the custom R packages

## Confidence: HIGH
