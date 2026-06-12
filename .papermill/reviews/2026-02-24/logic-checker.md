# Logic Checker Report

**Date**: 2026-02-24
**Paper**: Model Selection for Reliability Estimation in Series Systems

## Theorem Verification

### Theorem 5.1 (Weibull Closure for Series Systems)

**Closure part**: Correct. The algebra is straightforward: under k_1 = ... = k_m = k, the exponent in the reliability function factors as t^k * sum(lambda_j^{-k}), giving Weibull form. No issues.

**Uniqueness part**: The proof is correct but has a scope issue.

- **What is actually proven**: If independent Weibull(k_j, lambda_j) components form a series system whose lifetime is Weibull, then all k_j must be equal.
- **What is claimed**: "no other single-parameter restriction on the full 2m-parameter model yields a Weibull system lifetime"
- **Gap**: The theorem proves that k_1 = ... = k_m is *necessary* for Weibull closure. But the claim about "single-parameter restriction" is broader -- it implicitly claims that no constraint of the form g(k_1, ..., k_m, lambda_1, ..., lambda_m) = 0 (reducing to 2m-1 free parameters) can yield a Weibull system lifetime unless it implies k_1 = ... = k_m. The proof only addresses the case where the constraint is on the k_j values. What about exotic constraints mixing shapes and scales?

  In fact, the proof does handle this: if the cumulative hazard sum_{j}(t/lambda_j)^{k_j} must equal (t/lambda_s)^{k_s}, the linear independence argument forces all k_j = k_s regardless of what lambda_j values are chosen. So any parameter configuration with heterogeneous shapes, regardless of how the scales are constrained, fails to produce Weibull system lifetime. The uniqueness proof is **correct** but the connection between "single-parameter restriction" and the actual argument could be stated more explicitly.

**Severity**: Minor. The proof is sound but the framing of "single-parameter restriction" is slightly imprecise. A careful reader might wonder what happens with constraints that jointly involve shapes and scales.

### LRT Asymptotic Distribution

**Claim** (line 424-428): Under H0, Lambda ~ chi^2_{m-1}.

**Assessment**: This invokes the standard Wilks' theorem result for nested models. The regularity conditions for Wilks' theorem require:
1. The null hypothesis is in the interior of the parameter space -- **satisfied** (common shape k is interior)
2. Standard regularity conditions (smoothness, identifiability, etc.) -- **assumed but not verified**
3. The null model is correctly specified -- **satisfied by construction in simulations**

The simulation results (Table 4) confirm the chi-squared approximation is accurate, which provides empirical validation. **No logical issues.**

### Likelihood Function (Equations 8-12)

**Assessment**: The likelihood correctly accounts for:
- Censored observations contribute only the survival function
- Failed observations with candidate set C_i marginalize over possible failure causes
- The conditional probability Pr{K_i = j | t_i, theta} = h_j(t_i) / h(t_i) is correct under the independent competing risks assumption

**Potential issue**: Equation 10 shows the likelihood contribution for a failed system as:
L_i = sum_{j in C_i} Pr{K_i = j | t_i, theta} * f(t_i; theta)

This simplifies to:
L_i = sum_{j in C_i} h_j(t_i) / h(t_i) * f(t_i; theta) = f(t_i; theta) * sum_{j in C_i} h_j(t_i) / h(t_i)

Since f(t) = h(t) * R(t), this gives:
L_i = R(t_i) * sum_{j in C_i} h_j(t_i)

This is correct and matches the code in sim_utils.R (loglik_vec function, Term 1 + Term 2 decomposition).

**Code-paper consistency**: Verified. The vectorized log-likelihood in sim_utils.R correctly implements the mathematical formulation.

## Logical Chain Assessment

### Central Argument Structure

1. Well-designed systems have similar shape parameters (premise, informal)
2. Common-shape model is uniquely justified (Theorem 1)
3. LRT can test common-shape hypothesis (standard methodology)
4. Simulation shows LRT has low power for CV < 5% (empirical finding)
5. Therefore, reduced model is appropriate for well-designed systems (conclusion)

**Assessment**: The logical chain is valid but has a notable weakness at step 1: "well-designed" is circularly defined. The paper essentially says "if shapes are similar, the common-shape model fits" -- which is tautological. The interesting question is *why* well-designed systems should have similar shapes, and whether the CV < 5% threshold has physical meaning.

### Interpretation Issues

**Critical**: The paper conflates "LRT cannot reject" with "the reduced model is appropriate." Low power does not mean the reduced model fits well -- it means the test cannot detect the misfit. At n=100 with CV=8%, the rejection rate is only 8.8%, but the common-shape model is genuinely wrong. The paper acknowledges this is a power issue but still recommends using the reduced model at small n when CV is moderate. This is a defensible pragmatic recommendation (bias-variance tradeoff) but the epistemological argument is muddled.

**Major**: The paper does not quantify the *consequence* of using the wrong model. What is the bias in MTTF estimation when the reduced model is used but shapes are heterogeneous? A CV of 10% means the model is wrong -- the question is whether it's wrong enough to matter for reliability prediction. This is the missing piece of the argument.

## Findings Summary

| # | Finding | Severity | Confidence |
|---|---------|----------|------------|
| L1 | Theorem 1 proof scope: "single-parameter restriction" claim slightly broader than what's proven | Minor | High |
| L2 | Circular definition: "well-designed" defined by shape similarity, then claim reduced model works for well-designed systems | Major | High |
| L3 | Conflating "cannot reject" with "model is appropriate" -- missing consequence analysis | Critical | High |
| L4 | No quantification of reliability prediction error under model misspecification | Major | High |
| L5 | LRT chi-squared approximation empirically validated but regularity conditions not formally verified | Minor | Medium |
