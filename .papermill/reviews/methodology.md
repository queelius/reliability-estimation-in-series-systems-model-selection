# Methodology Audit Report

**Date**: 2026-02-27
**Paper**: "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"
**Reviewer focus**: Experimental design, statistical rigor, reproducibility

## Summary

The simulation methodology is well-designed for its core claims. The code is professional (analytical gradients, vectorized operations, resume logic, per-condition seeds). The statistical analysis uses appropriate methods (Wilson CIs for proportions, RMSE for predictions). However, the study has several methodological weaknesses that should be either addressed or explicitly acknowledged. The two most significant are: (1) the reduced model's convergence is never checked, which could produce negative Lambda values and inflate rejection rates; and (2) the vary-m experiment confounds number of components with shape CV, undermining one of its central claims. No issue I identified invalidates the paper's main conclusions, but several require correction or discussion.

---

## Critical Issues

### C1: Reduced model convergence is never checked

- **Location**: `results/sim_utils.R` lines 237-259; all simulation scripts
- **Problem**: Every simulation script checks `sol_F$convergence != 0` and skips non-converged full model fits. But the reduced model's convergence is **never checked**. The `fit_reduced_model()` function runs L-BFGS-B followed by Nelder-Mead, returning whichever achieves the higher log-likelihood. If both fail to converge properly, the reduced model's log-likelihood could be artificially low, producing an inflated Lambda statistic biasing the LRT toward rejection.
- **Impact**: If the reduced model systematically fails to fully converge in some fraction of cases, Lambda values will be biased upward, inflating both Type I error rates and power estimates.
- **Severity**: Critical
- **Confidence**: High

### C2: No guard against negative Lambda values

- **Location**: All simulation scripts, e.g., `lrt-divergence.R` line 151
- **Problem**: By nesting, `loglik_F >= loglik_R` must hold, giving `Lambda >= 0`. However, numerical optimization does not guarantee this. The code never checks for `Lambda < 0`, which would indicate an optimization failure.
- **Severity**: Critical
- **Confidence**: Medium

---

## Major Issues

### M1: Vary-m experiment confounds component count with shape CV

- **Problem**: When varying m from 2 to 8, the shape CV changes: m=2 has CV=5.5%, m=8 has CV=3.5%. The declining CV with increasing m means the power decrease attributed to "system complexity" is partially due to the decreasing shape heterogeneity.
- **Severity**: Major
- **Confidence**: High

### M2: Non-convergence rates substantially exceed "0-3%" at extreme conditions

- **Problem**: The paper claims "0-3% at n=100, near zero at larger n," but data shows up to 10% failure at CV=50% for n=500 and n=1000. Non-convergence rates do not decrease monotonically with n at extreme CVs.
- **Severity**: Major
- **Confidence**: High

### M3: Uniformly spaced shapes limit generalizability

- **Problem**: Symmetric arithmetic sequences produce minimum maximum-deviation-from-mean for a given CV. An asymmetric configuration at the same CV would likely produce larger MTTF bias.
- **Severity**: Major
- **Confidence**: Medium

### M4: LRT vs AIC vs BIC comparison uses different Type I error rates

- **Problem**: AIC and BIC are not hypothesis tests. Comparing their "Type I error rates" to the LRT's is category confusion. A fair comparison would calibrate all three to the same Type I error rate and compare power.
- **Severity**: Major
- **Confidence**: High

### M5: 500 replications produces wide CIs for key quantities

- **Problem**: Wilson 95% CI at p=0.05 with n=500 is [0.034, 0.073]. The bias claim "below 1% through CV 15%" has uncertainty of roughly +/- 0.4%.
- **Severity**: Major
- **Confidence**: High

---

## Minor Issues

- **m1**: Full model uses parscale but reduced model does not (asymmetric optimizer configuration)
- **m2**: RNG resume logic is incorrect (calls `runif(1)` per skipped replication, not the actual number consumed)
- **m3**: CV mapping between target and actual is non-obvious (target 10% → actual 13.7%, a 37% inflation)
- **m4**: Single baseline system may not span the parameter space (all shapes 1.13-1.26, no infant mortality or strong wear-out)
- **m5**: Default censoring (17.5%) may be optimistic for practical reliability studies
- **m6**: Adaptive procedure evaluated on same data used for selection (noted as a non-issue since truth is known)

---

## Strengths

1. **Analytical gradients** with vectorized implementation (not numerical differentiation)
2. **Two-stage optimization** for reduced model (L-BFGS-B + Nelder-Mead)
3. **Wilson confidence intervals** for proportions (correct choice)
4. **Per-condition reproducible seeds** enabling independent condition reproduction
5. **Comprehensive experimental design** varying five factors with multiple levels
6. **Sound overall statistical framework** with proper Type I error validation
7. **Multiple prediction metrics** (MTTF, R(t) at three points, component probabilities)
8. **Transparency about limitations** in the paper

---

## Reproducibility Checklist

- [x] Algorithm fully specified
- [x] Data described (simulation-based, fully specified)
- [partial] Hyperparameters listed (max_iter, lower bounds in code but not all in paper)
- [x] Code available
- [x] Statistical tests appropriate
- [partial] Baselines adequate (no cross-validation or bootstrap model selection comparison)
- [partial] Random seeds documented (in code, not in paper)
- [ ] Package versions specified

## Overall Assessment

**Sound with identified weaknesses.** The critical issues (C1, C2) should be investigated. The major issues (M1-M5) should be discussed or addressed. None invalidate the main narrative; the most likely impact would be to widen the uncertainty around specific numerical thresholds.
