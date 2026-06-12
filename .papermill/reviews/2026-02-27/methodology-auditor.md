# Methodology Auditor Report

**Date**: 2026-02-27
**Paper**: "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"

## Simulation Design Assessment

### Strengths

1. **Reproducibility**: Seeds are set explicitly (set.seed(2024)), with per-condition reproducible seeding. Resume logic is implemented for long-running simulations. Code and data are publicly available on GitHub
2. **Appropriate replication count**: 500 replications per condition is adequate for the precision needed. At 500 reps, a proportion of 0.05 has SE = sqrt(0.05*0.95/500) = 0.0097, giving reasonable precision
3. **Non-convergence handling**: Failed fits are silently excluded via tryCatch(), with the paper reporting convergence rates ("typically <3%; up to 10% at extreme CV"). Raw data confirms this (e.g., 488-500 successful reps out of 500 attempted)
4. **Optimization strategy**: The reduced model fitting uses L-BFGS-B followed by Nelder-Mead from the L-BFGS-B solution, addressing multimodality. The full model uses L-BFGS-B with analytical gradients and parscale
5. **Vectorized implementation**: The sim_utils.R code replaces O(n) interpreted loops with matrix operations, which is both faster and reduces the risk of implementation bugs

### Issues

#### Major

##### ME1: Single Baseline System
- **Problem**: All simulations use the same 5-component system from Guo et al. (2013) with shapes around 1.13-1.26 and scales around 840-994. The generalizability to systems with fewer/more components, different shape ranges, or markedly different scale patterns is unaddressed
- **Impact**: The bias-detectability alignment might not hold for systems with extreme shape values (e.g., k < 1 decreasing hazard, or k > 3 rapid wear-out) or asymmetric heterogeneity
- **Suggestion**: At minimum, add a second baseline system (e.g., 3 components with different shape ranges) as a robustness check. Alternatively, strengthen the limitations discussion

##### ME2: Shape Heterogeneity Pattern
- **Problem**: Shapes are generated as uniformly spaced about a mean of 1.18. Real systems could have clustered or asymmetric heterogeneity (e.g., one outlier component with a very different shape)
- **Impact**: The smooth bias and power curves may not apply when heterogeneity is concentrated in one component
- **Suggestion**: The paper mentions this limitation. A small supplementary experiment with one outlier shape would be valuable

##### ME3: Fixed Masking and Censoring
- **Problem**: The consequence analysis (Section 3) uses fixed p=0.215 and q=0.825 throughout. Appendix A varies these for LRT power but not for the bias analysis
- **Impact**: The bias-detectability alignment is demonstrated only at one (p,q) combination. It might shift under different data quality conditions
- **Suggestion**: Either vary (p,q) in the consequence analysis or clearly acknowledge that the alignment is established only at these specific values

#### Minor

##### me1: MTTF Computation via Numerical Integration
- The system MTTF is computed via `integrate()` with `rel.tol = 1e-8` and upper limit 1e5. This is appropriate for the parameter ranges used
- **Potential issue**: For shapes close to 1, the system reliability function decays slowly, and the upper limit of 1e5 might matter. Verified: with k~1.18 and lambda~900, the MTTF is ~222, so t=1e5 is about 450 MTTFs -- the integral contribution beyond this point is negligible

##### me2: Reduced Model Initial Values
- The reduced model is initialized with k_hat = mean(shapes_MLE) from the full model fit. This is reasonable but means the reduced model depends on the full model's convergence
- **Impact**: Minimal, since both models must converge for a replication to count

##### me3: No Confidence Intervals on Rejection Rates
- Table 3 reports point estimates of rejection rates without confidence intervals
- At 500 reps, a rate of 0.05 has 95% CI approximately [0.03, 0.07]; a rate of 0.50 has CI approximately [0.46, 0.54]
- **Suggestion**: Add CIs to at least the Type I error rates to demonstrate that the calibration claim is statistically supported

##### me4: Non-convergent Fits "Silently Excluded"
- The paper states non-convergent fits are excluded, typically <3%. The actual percentages should be reported per condition (or at least the max)
- **Concern**: If non-convergence is correlated with extreme parameter estimates, excluding these cases could bias the results

## Statistical Rigor

### Type I Error Assessment
- Claimed: 4.6-6.8% across n=100 to 10,000
- Verified: At n=100, rate is 0.054 (95% CI: [0.034, 0.074]); at n=5000, rate is 0.068 (95% CI: [0.046, 0.090])
- The 0.068 rate at n=5000 is borderline -- the CI barely includes 0.05 -- but is not a serious concern given the sample of 500 replications

### Power Analysis
- The power curves are monotonically increasing in both CV and n, which is expected and reassuring
- The paper correctly identifies that power depends on the product of effect size (CV) and sample size (n)

### Bias Analysis
- Bias is correctly computed as relative bias: (MTTF_hat - MTTF_true) / MTTF_true
- RMSE is in time units (not relative), which is appropriate for Table 2 but creates a mixed-units issue when comparing across CVs (since MTTF_true changes with CV)
- Table 4 expresses RMSE as % of true MTTF, which is the better metric

## Reproducibility

- **Code availability**: GitHub repository is referenced, R package is publicly available
- **Data availability**: CSV data files exist in the repository
- **Random seed**: Set explicitly with per-condition seeding
- **Dependencies**: Standard R packages plus author's custom package (wei.series.md.c1.c2.c3)
- **Concern**: The custom R package version is 0.9.0 -- a pre-1.0 version. Long-term reproducibility depends on the package being maintained

## Overall: The methodology is sound and well-implemented. The primary limitation is the single baseline system and fixed (p,q) for the consequence analysis. The statistical rigor is adequate for the claims made.
