# Citation Verifier Report

**Date**: 2026-02-27
**Paper**: "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"

## Bibliography Integrity

### Citations Used vs Bibliography
- **Citations in manuscript**: 13 unique cite commands referencing 13 distinct keys
- **Bibliography entries (.bbl)**: 13 entries
- **Entries in refs.bib**: 22 entries (9 uncited: Amma-2001, Usher-1996, Lin-1996, Zhibi-2007, Zhibi-2005, Amma-2004, meeker1998, lawless2003, burnham2002)
- **Status**: All cited keys resolve correctly. No undefined references, no multiply-defined labels

### Uncited Bibliography Entries

The .bib file contains 9 entries not cited in the QREI manuscript:

1. **Amma-2001** (Sarhan): Reliability estimations from masked data -- relevant but not directly used
2. **Usher-1996**: Weibull component reliability with masked data -- directly relevant, should arguably be cited
3. **Lin-1996**: Bayes estimation from masked data -- relevant as the Bayesian counterpart
4. **Zhibi-2007** (Tan): Exponential component reliability from uncertain data -- peripheral
5. **Zhibi-2005** (Tan): Component failure probability from masked binomial data -- peripheral
6. **Amma-2004** (Sarhan): Parameter estimation in linear failure rate model -- peripheral
7. **meeker1998** (Meeker & Escobar): Standard reliability textbook -- **should be cited**
8. **lawless2003** (Lawless): Standard lifetime data methods textbook -- **should be cited**
9. **burnham2002** (Burnham & Anderson): Standard model selection reference -- **should be cited** given AIC/BIC are discussed

### Citation Accuracy Spot-Checks

#### Barlow & Proschan 1975 [1]
- **Cited for**: Weibull closure property
- **Assessment**: Correct. The closure property for minimum of Weibull random variables with common shape is established in this book

#### Wilks 1938 [8]
- **Cited for**: LRT asymptotic chi-squared distribution
- **Assessment**: Correct reference

#### White 1982 [13]
- **Cited for**: MLE under misspecified models, supporting the bias-variance discussion
- **Assessment**: Correct. White's paper establishes that quasi-MLE converges to the KL-minimizing parameter value under misspecification. However, the paper's invocation is somewhat tangential -- White's results are about pseudo-true values, while the paper is discussing variance propagation through a nonlinear functional
- **Suggestion**: The citation to White is acceptable but a more direct reference would be to the delta method / functional delta method literature for variance propagation

#### Guo et al. 2013 [6]
- **Cited for**: Baseline system configuration
- **Assessment**: Correct. The entry lists this as "Annual Reliability and Maintainability Symposium (RAMS)" which is a conference proceedings, not a journal article. The BibTeX entry type is @article which is technically incorrect for a conference paper -- should be @inproceedings

#### Towell 2023a [2]
- **Cited for**: Foundation likelihood model
- **Assessment**: This is a GitHub repository (@Misc entry). Not peer-reviewed. Acceptable for software/methodology citations but a reviewer might question relying on unpublished work for the core likelihood derivation
- **Note**: The entry says "accessed 2026-02-18" but the publication year is 2023 -- the long gap between publication and access suggests this is an evolving document

#### Towell 2023b [12]
- **Cited for**: R package used for simulations
- **Assessment**: Appropriate citation for software. The .bbl renders with a duplicated "Available:" which is a minor formatting issue from the BibTeX entry

### Missing Citations That Reviewers Would Expect

1. **Meeker & Escobar (1998)**: Standard reliability data textbook. Should be cited when discussing Weibull distributions and MLE methods
2. **Lawless (2003)**: Standard lifetime data methods reference. Should be cited for model selection context
3. **Burnham & Anderson (2002)**: Standard information criteria reference. Should be cited alongside Akaike and Schwarz since AIC/BIC are discussed in Appendix B
4. **Nelson (2003)** or equivalent for Weibull distribution properties
5. **Self & Liang (1987)**: Asymptotic properties of MLEs for parameters on the boundary -- relevant since the null hypothesis k_1 = ... = k_m is a boundary of the parameter space (though the standard chi-squared approximation is used)

### Bibliography Format Issues

1. **Inconsistent entry types**: Guo et al. 2013 is @article but should be @inproceedings
2. **towell2023weibull .bbl**: Contains double "Available:" text
3. **Citation style**: IEEEtranN with natbib numbers -- appropriate for general use but QREI uses its own Wiley style. The paper may need reformatting for submission

## Summary

- All 13 citations resolve correctly
- 3-4 standard references should be added (Meeker/Escobar, Lawless, Burnham/Anderson)
- Minor formatting issues in bibliography entries
- The core technical citations are accurate and appropriate
