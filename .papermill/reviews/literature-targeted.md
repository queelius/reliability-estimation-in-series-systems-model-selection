# Targeted Literature Comparison

**Date**: 2026-02-27

## Closest Competitors

### 1. Craiu and Lee (2005) — "Model Selection for the Competing-Risks Model With and Without Masking"
- **Threat**: HIGH. Both papers do model selection for competing risks under masked data using AIC/BIC.
- **Differentiator**: Craiu & Lee use nonparametric piecewise-constant hazards; select number of intervals, not parametric structure. No consequence analysis, no adaptive procedure.
- Technometrics 47(4), 2005.

### 2. Pareek, Kundu, Kumar (2009) — "On progressively censored competing risks data for Weibull distributions"
- **Threat**: MEDIUM. Uses identical common-shape Weibull model as the paper's reduced model.
- **Differentiator**: Tests equality of *scales* (not shapes). No masked data, no consequence analysis.
- Computational Statistics & Data Analysis 53(12):4083-4094.

### 3. Pascual (2005) — "MLE Under Misspecified Lognormal and Weibull Distributions"
- **Threat**: MEDIUM. Consequence-of-misspecification analysis for reliability.
- **Differentiator**: Studies family misspecification (Weibull vs lognormal), not within-family (common vs heterogeneous shape). No masked data.
- Communications in Statistics 34(3):503-524.

### 4. McCool (1970) / Thoman & Bain (1969) — LRT for Weibull shape equality
- **Threat**: MEDIUM. Classical precedent for the paper's LRT.
- **Differentiator**: Complete/Type II censored data from independent populations, not masked series systems.

### 5. Kundu and Pradhan (2011) — Bayesian common-shape Weibull competing risks
- **Threat**: MEDIUM. Same model, Bayesian approach.
- **Differentiator**: No model selection question; assumes common shape is correct.

### 6-10. (Xu & Tang 2005, Davila & Henna 2021, Murthy et al. 2004, Yang & Lin 2007, Guo et al. 2013) — Low threat, supportive or complementary.

## Missing Citations (should cite)

| Reference | Why |
|-----------|-----|
| Craiu and Lee (2005) | Most directly relevant prior work on masked data model selection |
| Pareek, Kundu, Kumar (2009) | Most cited paper using common-shape Weibull competing risks |
| McCool (1970) | Classical LRT for Weibull shape equality |
| Pascual (2005) | Precedent for misspecification consequence analysis |
| White (1982) | Theoretical foundation for MLE under misspecification |

## Novelty Assessment

| Claim | Status |
|-------|--------|
| Consequence analysis (MTTF bias vs CV) for masked data | **Genuinely new** — no prior work found |
| Bias-detectability alignment | **New framing** — specific quantification is original |
| Adaptive LRT procedure | **Standard methodology** — evaluation is new |
| Full model lower MSE at CV=0 | **Known possibility** for nonlinear functionals, but new demonstration |
| AIC liberal / BIC conservative | **Well-known** — confirmation in new setting |
