# Experimental Results Analysis

## Overview

This document provides a detailed analysis of the simulation results for the likelihood ratio test (LRT) and bootstrap confidence interval studies in the context of model selection for reliability estimation in series systems with Weibull-distributed component lifetimes.

All experiments use a baseline 5-component series system with shape parameters near 1.1--1.3 and scale parameters around 900--1000. The null hypothesis H0 posits a reduced model where all components share a common shape parameter. The full model allows each component its own shape and scale (2m = 10 parameters), while the reduced model has m + 1 = 6 parameters. The LRT statistic Lambda = -2(loglik_R - loglik_F) is compared to a chi-squared distribution with m - 1 = 4 degrees of freedom at significance level alpha = 0.05.

---

## 1. LRT Divergence Analysis (Shape Heterogeneity)

**Experiment**: Vary the coefficient of variation (CV) of shape parameters from 0% (perfect homogeneity, H0 true) to 50% (extreme heterogeneity, H0 strongly violated), across sample sizes n = {100, 500, 1000, 5000, 10000}, with 500 replications per condition.

### 1.1 Type I Error (CV = 0)

When all shape parameters are identical (CV = 0), the LRT should reject at rate alpha = 0.05. Observed rejection rates:

| n | Rejection Rate | 95% Wilson CI | Status |
|---|---|---|---|
| 100 | 0.054 | [0.037, 0.077] | OK |
| 500 | 0.056 | [0.039, 0.080] | OK |
| 1000 | 0.046 | [0.031, 0.068] | OK |
| 5000 | 0.068 | [0.049, 0.094] | OK |
| 10000 | 0.046 | [0.031, 0.068] | OK |

**Finding**: All Type I error rates are well-calibrated. Every 95% Wilson confidence interval contains the nominal alpha = 0.05, confirming the chi-squared approximation is valid for this baseline system under homogeneity. No evidence of size distortion at any sample size.

### 1.2 Power Curves

The LRT exhibits the expected behavior: power increases monotonically with both CV (effect size) and n (sample size).

| Target CV | n=100 | n=500 | n=1000 | n=5000 | n=10000 |
|---|---|---|---|---|---|
| 0.00 | 0.054 | 0.056 | 0.046 | 0.068 | 0.046 |
| 0.02 | 0.048 | 0.062 | 0.052 | 0.186 | 0.268 |
| 0.04 | 0.075 | 0.072 | 0.130 | 0.541 | 0.887 |
| 0.06 | 0.074 | 0.126 | 0.266 | 0.936 | 0.996 |
| 0.08 | 0.088 | 0.252 | 0.494 | 0.996 | 1.000 |
| 0.10 | 0.129 | 0.385 | 0.690 | 1.000 | 1.000 |
| 0.15 | 0.200 | 0.790 | 0.968 | 1.000 | 1.000 |
| 0.20 | 0.357 | 0.994 | 1.000 | 1.000 | 1.000 |
| 0.30 | 0.775 | 1.000 | 1.000 | 1.000 | 1.000 |
| 0.50 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

### 1.3 Minimum CV for 80% Power

| Sample Size | Min CV for 80% Power |
|---|---|
| n = 100 | 68.5% |
| n = 500 | 27.4% |
| n = 1000 | 20.5% |
| n = 5000 | 8.2% |
| n = 10000 | 5.5% |

**Finding**: At n = 100, the test has very limited power -- even a CV of 50% is needed for near-certain detection, and 80% power requires a CV of ~69% (extreme shape heterogeneity). In practice, for moderate sample sizes (n = 1000), the LRT can detect shape heterogeneity of ~20% CV. At large samples (n = 5000+), even subtle heterogeneity (CV ~ 5--8%) is detectable.

### 1.4 Model Selection Criterion Comparison (LRT vs AIC vs BIC)

At CV = 0 (Type I error comparison):
- **LRT** rejection rates: 4.6--6.8% (well-calibrated at alpha = 0.05)
- **AIC** selects full model: 8.2--12.4% (approximately 2x the LRT rate, liberal)
- **BIC** selects full model: 0--0.2% (extremely conservative)

At intermediate CV (power comparison at n = 1000):
- AIC is the most sensitive (earliest to select the full model as CV increases)
- LRT occupies a middle ground
- BIC is the most conservative (latest to select the full model)

**Finding**: AIC has an inherent bias toward model complexity -- it selects the full model about twice as often as the LRT under H0. BIC is strongly parsimonious, rarely selecting the full model even when it's correct. The LRT provides the best-calibrated Type I error control while still offering good power, making it the most appropriate test for this setting.

---

## 2. Effect of Number of Components (vary_m)

**Experiment**: Vary the number of components m = {2, 3, 4, 5, 6, 7, 8} while keeping the same shape parameters (first m components of the baseline), across n = {100, 500, 1000, 5000}, with 500 replications per condition.

### 2.1 Key Results

| m | df (m-1) | Shape CV | n=100 | n=500 | n=1000 | n=5000 |
|---|---|---|---|---|---|---|
| 2 | 1 | 5.5% | 0.074 | 0.126 | 0.216 | 0.774 |
| 3 | 2 | 5.6% | 0.068 | 0.128 | 0.186 | 0.720 |
| 4 | 3 | 4.5% | 0.048 | 0.088 | 0.122 | 0.404 |
| 5 | 4 | 4.0% | 0.078 | 0.066 | 0.096 | 0.307 |
| 6 | 5 | 3.9% | 0.103 | 0.076 | 0.084 | 0.264 |
| 7 | 6 | 3.7% | 0.083 | 0.090 | 0.080 | 0.208 |
| 8 | 7 | 3.5% | 0.088 | 0.078 | 0.060 | 0.160 |

### 2.2 Analysis

There are two competing effects as m increases:

1. **Dilution of shape heterogeneity**: As more components are added (all having similar shape parameters), the CV of the full shape vector *decreases* (from ~5.5% at m=2 to ~3.5% at m=8). The newly added components dilute the variation that exists among the original components.

2. **Increased degrees of freedom**: The LRT has df = m-1, so the critical value of the chi-squared distribution increases. This makes it harder to reject H0 for any given test statistic value.

Both effects conspire to reduce rejection rates as m increases. At n = 5000:
- m = 2: rejection rate = 77.4% (strong power)
- m = 5: rejection rate = 30.7% (moderate power)
- m = 8: rejection rate = 16.0% (weak power)

**Finding**: The LRT is most powerful for smaller systems. For large systems (m >= 6), the combination of diluted heterogeneity and higher chi-squared critical values makes it difficult to detect mild shape differences unless sample sizes are very large. The mean test statistic tracks the expected value (df) well at small n but grows substantially faster than df at n = 5000, consistent with the test having power (the true model violates H0 for all m > 1 due to the non-identical shapes in the baseline).

---

## 3. Effect of Masking Probability (vary_p)

**Experiment**: Vary the masking probability p = {0.05, 0.10, 0.15, 0.215, 0.30, 0.40, 0.50, 0.60, 0.70} (fraction of failures where the exact cause is masked), across n = {100, 500, 1000, 5000}, with 500 replications per condition. The baseline shape CV is ~4%, so the LRT is operating near the null.

### 3.1 Key Results

| p | n=100 | n=500 | n=1000 | n=5000 |
|---|---|---|---|---|
| 0.050 | 0.060 | 0.102 | 0.120 | 0.482 |
| 0.100 | 0.052 | 0.102 | 0.098 | 0.442 |
| 0.150 | 0.085 | 0.060 | 0.096 | 0.351 |
| 0.215 | 0.067 | 0.066 | 0.096 | 0.307 |
| 0.300 | 0.081 | 0.062 | 0.074 | 0.262 |
| 0.400 | 0.054 | 0.062 | 0.066 | 0.184 |
| 0.500 | 0.054 | 0.044 | 0.056 | 0.144 |
| 0.600 | 0.044 | 0.048 | 0.068 | 0.100 |
| 0.700 | 0.026 | 0.042 | 0.032 | 0.076 |

### 3.2 Analysis

The masking probability has a dramatic effect on the LRT's behavior:

**Low masking (p <= 0.15)**: Rejection rates are noticeably *inflated* above 0.05, especially at large n. At p = 0.05, n = 5000, the rejection rate is 0.482 -- nearly 10x the nominal level. This is because low masking provides more information about failure causes, which actually exposes the small shape differences in the baseline system (CV ~ 4%). The LRT correctly detects these real (albeit small) deviations from homogeneity.

**High masking (p >= 0.50)**: Rejection rates *drop below* 0.05 (e.g., 0.026 at p = 0.70, n = 100). Heavy masking obscures failure cause information so severely that the test loses power to detect even the baseline's shape heterogeneity. At p = 0.70, even n = 5000 yields a near-nominal 0.076 rejection rate.

**Default setting (p = 0.215)**: At the project's default masking probability, rejection rates are close to nominal (0.067--0.096) for moderate n, with some inflation at n = 5000 (0.307).

**Finding**: Masking acts as a "blurring" mechanism on the LRT. Low masking exposes true parameter differences (even small ones), while high masking hides them. This is a nuisance parameter effect: the masking probability changes the effective information content of each observation. For practical guidance, researchers should be aware that LRT results are most reliable at moderate masking levels, and that low masking combined with large n may produce rejections from practically insignificant shape differences.

---

## 4. Effect of Censoring Level (vary_q)

**Experiment**: Vary the censoring quantile q = {0.50, 0.60, 0.70, 0.825, 0.90, 0.95, 1.00} (q = 1.0 means no censoring; q = 0.5 means approximately 50% of observations are right-censored), across n = {100, 500, 1000, 5000}, with 500 replications per condition.

### 4.1 Key Results

| q | Pct Censored | n=100 | n=500 | n=1000 | n=5000 |
|---|---|---|---|---|---|
| 0.500 | ~50% | 0.082 | 0.068 | 0.096 | 0.170 |
| 0.600 | ~40% | 0.088 | 0.080 | 0.082 | 0.216 |
| 0.700 | ~30% | 0.095 | 0.060 | 0.100 | 0.240 |
| 0.825 | ~17.5% | 0.067 | 0.066 | 0.096 | 0.307 |
| 0.900 | ~10% | 0.080 | 0.076 | 0.090 | 0.341 |
| 0.950 | ~5% | 0.072 | 0.086 | 0.100 | 0.398 |
| 1.000 | 0% | 0.078 | 0.084 | 0.112 | 0.430 |

### 4.2 Analysis

Censoring has a *monotonic but moderate* effect on rejection rates:

- At **n = 5000**, rejection rates increase from 0.170 (50% censored) to 0.430 (no censoring) -- a 2.5x factor.
- At **n = 100--1000**, the effect is much smaller and largely within sampling variability. Most rates fall in the range 0.06--0.10 regardless of censoring level.

The censoring effect is notably weaker than the masking effect. At n = 5000:
- Varying q from 0.5 to 1.0 changes rejection rate by ~0.26 (from 0.17 to 0.43)
- Varying p from 0.05 to 0.70 changes rejection rate by ~0.41 (from 0.48 to 0.08)

**Finding**: Censoring reduces the effective sample size but does not fundamentally change the information structure of each observation (unlike masking). The LRT remains approximately well-calibrated across all censoring levels for moderate n. The inflated rates at n = 5000 are again attributable to the test detecting the baseline's real (small) shape heterogeneity, not to size distortion -- the same pattern seen in the masking experiment.

---

## 5. Bootstrap Confidence Interval Analysis (Scale3 System)

**Experiment**: Vary the scale parameter of component 3 (lambda_3) from 250 to 1750 while keeping all other parameters fixed. This systematically changes the failure probability of component 3 (Pr{K_i = 3}). For each setting, 200 bootstrap replications produce BCa 95% confidence intervals for all 10 parameters (5 shapes + 5 scales). The x-axis represents either the MTTF of the system or Pr{K_i = 3}.

### 5.1 Coverage Probability Results

Coverage probabilities for shape and scale parameters across varying scale_3:

**Scale parameters**: Coverage rates for scales lambda_1, lambda_2, lambda_4, lambda_5 (the non-varying components) are generally stable around 0.91--0.95. Scale lambda_3 (the varying component) also maintains reasonable coverage, though it degrades slightly at extreme values (both very low and very high lambda_3).

**Shape parameters**: Coverage for shapes consistently runs below the nominal 95% level, typically in the range 0.87--0.93. Shape k_1 shows the most degradation, dropping to ~0.87 at high Pr{K_3} values. This undercoverage of shape parameters is a known issue with BCa intervals for Weibull MLE in masked data settings.

**Overall pattern**: As Pr{K_3} increases (lambda_3 becomes more extreme relative to other scales), coverage tends to decrease for shape parameters while remaining more stable for scale parameters. This suggests that the MLE's are more sensitive to model perturbations in the shape dimension.

### 5.2 MLE Bias and Precision

The boxplot series (10 plots per system) show the distribution of MLE estimates across bootstrap replications as a function of the varying parameter. Key observations:

- **Scale MLE bias**: Scale estimates for non-varying components remain well-centered around true values across all conditions. Scale_3 estimates track the true value but show increasing variance at extreme settings.
- **Shape MLE bias**: Shape estimates show mild positive bias that increases slightly as the system departs from the well-designed baseline.
- **Precision**: Confidence interval widths (upper - lower bounds) increase substantially for extreme parameter settings, reflecting increased estimation uncertainty when the system is poorly designed.

---

## 6. Bootstrap Confidence Interval Analysis (Shape3 System)

**Experiment**: Vary the shape parameter of component 3 (k_3) from 0.1 to 1.9 while keeping all other parameters fixed. This changes both the failure probability of component 3 and the hazard rate structure of the system.

### 6.1 Coverage Probability Results

**Scale parameters**: Coverage for all scale parameters remains in the range 0.91--0.97, with most values near 0.94--0.95. Scale parameters are notably robust to shape perturbations. At extreme k_3 values (0.1 or 1.9), some degradation occurs but coverage remains above 0.90 for most components.

**Shape parameters**: Shape coverage shows a clear downward trend as Pr{K_3} increases (k_3 moves away from the baseline). At low Pr{K_3} (k_3 near the baseline), shape coverage is approximately 0.90--0.93. At high Pr{K_3} (k_3 extreme), shape k_1 drops to ~0.81 and shape k_3 drops even lower.

**Component 3 shape**: The coverage probability for k_3 itself follows an interesting trajectory. At extreme k_3 values (very low or very high), the coverage intervals for k_3 widen dramatically, and the coverage either improves (intervals become conservative) or degrades depending on the direction.

### 6.2 Comparison with Scale3 System

Shape perturbations produce more severe coverage degradation than scale perturbations:
- **Scale3**: Mean shape coverage drops from ~0.92 to ~0.88 as Pr{K_3} goes from 0.12 to 0.55
- **Shape3**: Mean shape coverage drops from ~0.91 to ~0.83 over a similar Pr{K_3} range

This asymmetry makes physical sense: shape parameters control the *form* of the hazard function (increasing, decreasing, constant), while scale parameters only shift the time axis. Perturbing the shape fundamentally changes the failure dynamics, making the MLE landscape more complex and bootstrap approximations less accurate.

---

## 7. Cross-Cutting Themes and Conclusions

### 7.1 The LRT is Well-Calibrated Under the Null

Across all experimental conditions at CV = 0 (or near-zero shape heterogeneity), the LRT maintains good Type I error control. The chi-squared approximation with m-1 degrees of freedom is accurate for this Weibull series system.

### 7.2 Power Depends on Sample Size, Information Content, and System Complexity

Three factors govern LRT power:
1. **Sample size (n)**: Most dominant factor. Going from n = 100 to n = 10000 transforms a near-powerless test into one that detects CV = 5.5% with 80% power.
2. **Masking probability (p)**: More masking = less information per observation = lower power. This is effectively an information-theoretic constraint.
3. **System complexity (m)**: More components = more parameters to estimate = less power for any fixed n.

Censoring has a comparatively modest effect.

### 7.3 AIC is Liberal, BIC is Conservative, LRT is Well-Calibrated

The three model selection criteria have distinct operating characteristics:
- **AIC**: ~2x the false positive rate of the LRT; early detection of true differences but poor specificity
- **BIC**: Nearly zero false positives; strong parsimony but may miss real differences at moderate n
- **LRT at alpha = 0.05**: Balanced Type I error with good power; recommended for formal hypothesis testing

### 7.4 Bootstrap CIs Show Systematic Shape Undercoverage

Both the scale3 and shape3 experiments reveal that BCa bootstrap confidence intervals for shape parameters tend to undercover (typically 88--93% instead of the nominal 95%). Scale parameter coverage is better (91--96%). This systematic pattern suggests that:
- The bootstrap distribution for shape parameters has heavier tails or asymmetry not fully captured by the BCa correction
- Shape parameters are intrinsically harder to estimate in masked data settings due to confounding between shape and cause-of-failure information

### 7.5 Well-Designed Systems Enable Reliable Inference

The baseline system was designed so that all components contribute roughly equally to system failure. The experiments show that as the system departs from this well-designed baseline (by perturbing one component's shape or scale):
- MLE variance increases
- Coverage probabilities decrease
- The reduced model becomes increasingly inappropriate

This supports the paper's core thesis: the homogeneous-shape reduced model is a reasonable approximation for well-designed series systems, but its validity degrades as component heterogeneity increases. The LRT provides a principled way to test this assumption.

---

## Summary Table of Key Findings

| Experiment | Key Finding | Practical Implication |
|---|---|---|
| Divergence (CV) | Type I error = 0.046--0.068, power → 1.0 as CV increases | LRT correctly calibrated; detects heterogeneity |
| Vary m | Rejection rate decreases from 0.77 (m=2) to 0.16 (m=8) at n=5000 | Larger systems need larger samples for same power |
| Vary p | Rejection rate spans 0.026--0.482 depending on masking | Low masking inflates rejection (detects real differences) |
| Vary q | Rejection rate spans 0.170--0.430 at n=5000 | Censoring has moderate, monotonic effect |
| Bootstrap (Scale3) | Scale CP ~0.91--0.95; Shape CP ~0.87--0.93 | Shape parameters systematically undercover |
| Bootstrap (Shape3) | Shape CP drops to ~0.83 at extreme perturbations | Shape perturbations more damaging than scale |
| AIC vs BIC vs LRT | AIC 2x false positives; BIC near-zero; LRT calibrated | LRT recommended for formal testing |
