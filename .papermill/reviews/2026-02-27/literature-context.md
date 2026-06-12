# Literature Context Report

**Date**: 2026-02-27
**Paper**: "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"

## Field Overview

Model selection for series system reliability with masked and censored data is a niche but well-established subfield of reliability engineering. The foundational work on MLE from masked system data goes back to Usher & Hodgson (1988), with subsequent contributions by Lin, Usher, and Guess (1993) and the Bayesian treatment by Lin et al. (1996). The field has seen steady but modest activity, with the most recent computational advances coming from Guo et al. (2013) and Towell (2023).

The Weibull closure property under common shape is classical (Barlow & Proschan 1975), but its implications for model selection in the presence of masked data have not been systematically explored in the literature.

## Competing Approaches

### Bayesian Model Selection
- **Lin et al. (1996)** developed Bayes estimation for masked data but did not address model selection between full and reduced models
- **Craiu & Lee (2005)** addressed model selection for competing-risks models with masking using Bayes factors and BIC, but in a different (non-Weibull series) context
- No Bayesian model averaging approach for the full-vs-reduced Weibull series question has been published

### Information-Theoretic Approaches
- The paper compares LRT, AIC, and BIC (Appendix B), which is appropriate
- Burnham & Anderson (2002) is in the .bib but not cited in the QREI manuscript -- this is a minor gap since it is a standard reference for information-theoretic model selection
- No work applies cross-validation or predictive model selection to masked series data

### Robust/Semiparametric Approaches
- No published work on robust estimation approaches that sidestep the model selection question entirely for masked Weibull series data
- Potential gap: semiparametric approaches, nonparametric reliability estimation from masked data

## Masked Data Literature -- Recent Advances (2018-2025)

The bibliography is somewhat dated. The most recent masked data papers cited are from 2013 (Guo et al.) and 2005 (Craiu & Lee). Potential missing references include:

1. **Bayesian approaches to masked data**: Several papers post-2013 have applied MCMC and Gibbs sampling to masked series systems
2. **EM algorithm approaches**: Variants of EM for masked data with competing risks
3. **Dependent masking**: Work relaxing the non-informative masking assumption

However, the core frequentist MLE literature for masked Weibull series systems is adequately covered. The gap is primarily in Bayesian methods and recent methodological advances.

## Model Misspecification in Reliability

The paper's "consequence analysis" framing -- quantifying prediction error rather than just detectability -- is genuinely novel in this specific context. Related work:

- **White (1982)**: Cited, provides the theoretical foundation for MLE under misspecification
- **Meeker & Escobar (1998)**: In .bib but uncited in QREI manuscript; discusses model adequacy checking for reliability
- **Lawless (2003)**: In .bib but uncited; covers model selection and assessment for lifetime data

The decision-theoretic framing (consequence of being wrong vs. ability to detect wrongness) has analogues in other statistical fields (e.g., equivalence testing, practical significance vs. statistical significance) but has not been applied to masked series system model selection.

## Benchmark Configurations

The 5-component baseline from Guo et al. (2013) is a standard test configuration in this literature. The paper's simulation parameters (p=0.215, q=0.825) are within standard ranges. The systematic variation of shape CV as the primary independent variable is a well-chosen design.

## Gaps in Coverage

1. **Meeker & Escobar (1998)** and **Lawless (2003)**: Standard reliability textbooks that should be cited for context even if not directly used
2. **Burnham & Anderson (2002)**: Standard reference for information criteria, in .bib but uncited
3. **Recent Bayesian masked data work**: Post-2013 contributions
4. **Equivalence testing / TOST literature**: Related to the "is the difference practically significant?" framing
5. **Bootstrap methods for model selection in reliability**: Not discussed
6. **Competing risks literature beyond Craiu & Lee**: Crowder (2001), Pintilie (2006)

## Self-Citation Assessment

Two self-citations (Towell 2023a, 2023b) are both essential -- one provides the likelihood framework used throughout, and the other is the R package implementing all simulations. These are appropriate and not excessive. The self-citations are technically to a GitHub repository (Misc entry) and an R package (Manual entry), which is somewhat unconventional but acceptable for software/method papers.

## Key Takeaway

The paper addresses a genuine gap: no prior work has quantified the prediction consequences (as opposed to statistical detectability) of common-shape misspecification in Weibull series systems with masked data. The "bias-detectability alignment" observation appears to be novel. The bibliography is adequate for the core topic but could be strengthened with standard textbook references and more recent masked data work.
