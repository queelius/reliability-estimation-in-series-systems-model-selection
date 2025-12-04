---
layout: default
title: Model Selection for Reliability Estimation in Series Systems
---

# Model Selection for Reliability Estimation in Series Systems

**Author:** Alex Towell ([lex@metafunctor.com](mailto:lex@metafunctor.com))

## Abstract

When can reliability engineers safely use a simpler model for series system analysis? This paper provides a definitive answer: for well-designed systems with similar component failure characteristics, a reduced homogeneous-shape Weibull model is statistically indistinguishable from the full heterogeneous model even with 30,000 observations. This striking finding means practitioners can confidently use the simpler model—which halves the parameter count from 2m to m+1 and renders the system itself Weibull-distributed—without sacrificing accuracy.

## Key Results

### The Central Question

In reliability engineering, we often face a choice between:
- **Full model**: Each of m components has its own shape and scale parameter (2m parameters)
- **Reduced model**: All components share a common shape parameter (m+1 parameters)

The reduced model is simpler and more interpretable, but is it accurate enough?

### Main Findings

1. **For well-designed systems**: The reduced model cannot be rejected even with n = 30,000 observations
2. **Sharp sensitivity boundaries**: We quantify exactly how much heterogeneity triggers rejection
3. **Practical thresholds**:
   - CV < 10%: Use reduced model confidently
   - CV 10-20%: Depends on sample size
   - CV > 25%: Use full model

### Power Analysis

| CV (%) | n=100 | n=500 | n=1000 | n=5000 | n=10000 |
|--------|-------|-------|--------|--------|---------|
| 0.0    | 0.07  | 0.06  | 0.05   | 0.05   | 0.05    |
| 2.7    | 0.06  | 0.05  | 0.06   | 0.17   | 0.34    |
| 5.5    | 0.07  | 0.09  | 0.13   | 0.53   | 0.85    |
| 8.2    | 0.07  | 0.12  | 0.26   | 0.91   | 1.00    |

*Rejection rates at α = 0.05 for the likelihood ratio test*

## Practical Implications

For reliability practitioners:

1. **Well-designed systems** (similar component characteristics): Use the reduced model. Benefits include lower variance estimates, simpler interpretation, and analytical tractability.

2. **Systems with a weak component**: Use the full model. Even one component with substantially different shape will be detected with moderate sample sizes.

3. **Unknown system design**: Estimate the coefficient of variation of shape parameters from initial data to guide model selection.

## Citation

```bibtex
@article{towell2024modelselection,
  title={Model Selection for Reliability Estimation in Series Systems},
  author={Towell, Alex},
  year={2024},
  note={Preprint}
}
```

## Resources

- [GitHub Repository](https://github.com/queelius/reliability-estimation-in-series-systems-model-selection)
- [Download Paper (PDF)](paper.pdf)
- [Simulation Code](https://github.com/queelius/reliability-estimation-in-series-systems-model-selection/tree/master/results)

## Related Work

This paper builds on:
- Towell (2023). *Reliability Estimation in Series Systems with Masked Data*. [GitHub](https://github.com/queelius/reliability-estimation-in-series-systems)
- Guo, Niu, & Szidarovszky (2013). *Estimating component reliabilities from incomplete system failure data*
