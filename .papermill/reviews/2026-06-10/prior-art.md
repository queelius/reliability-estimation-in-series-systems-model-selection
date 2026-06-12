---
title: "Prior-Art Survey: Weibull Series Consequence Analysis"
date: 2026-06-10
agent: papermill:literature-survey
paper: weibull-series-consequence
---

# Prior-Art Survey

**Paper:** "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"
**Survey date:** 2026-06-10
**Agent:** papermill:literature-survey (Claude Sonnet 4.6)

---

## Summary Statistics

- Foundational references verified: 12
- Competing / novelty-threat references identified: 8
- Complementary references identified: 10
- Tangential references noted: 5
- Unverified entries: 0
- New references recommended for refs.bib: 18 (listed in BibTeX block below)

---

## Executive Summary: Top 5 Novelty Threats

### Threat 1 (HIGHEST): Claeskens-Hjort FIC Framework (2003/2006/2008)

The focused information criterion (FIC) of Claeskens and Hjort (JASA 2003) and the companion paper by Hjort and Claeskens ("Frequentist model average estimators," JASA 2003, pp. 879-899) constitute the single largest positioning risk. The FIC framework selects models to minimize estimated asymptotic MSE of a specific "focus parameter" (such as MTTF) under a local O(1/sqrt(n)) misspecification assumption. This is conceptually close to the paper's zero-first-order-gain proposition and the pretest risk hump analysis. The key differentiators are: (a) FIC operates under local (n-shrinking) misspecification exclusively, and the paper treats fixed misspecification whose bias is n-independent; (b) FIC has been applied to Cox models (Claeskens-Hjort 2006, JASA) but never to Weibull series systems or masked cause-of-failure data; (c) the paper's zero-first-order-gain proposition is a stronger claim than FIC makes: it shows the constraint provides exactly zero variance reduction at any common-shape point, which is a structural zero, not a small-number result. Positioning: the paper should cite both 2003 JASA papers and state explicitly that FIC theory under local alternatives is the motivation for the Le Cam derivation in Section 4.5, while emphasizing that the practical relevance of the fixed-misspecification bias (n-independent) is the paper's primary contribution beyond FIC.

### Threat 2: Pretest Estimation Literature (Bancroft 1944 onward)

The "adaptive LRT-based procedure" described in Section 5 is a textbook pretest estimator. Bancroft (1944) originated the pretest idea; Judge and Bock (1978) gave the canonical treatment of risk properties; Giles and Giles (1993, Journal of Economic Surveys) is the standard review; Danilov and Magnus (2004, Journal of Econometrics 122:27-46) showed the harm of ignoring pretesting and quantified bias, variance, and MSE of the pretest estimator. The n=100 risk hump the paper observes is the classical pretest risk hump, well-known in this literature. Leeb and Potscher (2003, 2005) further showed that post-model-selection inference is non-uniform. The paper's 2026-05-03 review already flagged this (reframing from "new procedure" to "empirical evaluation of textbook LRT"), so the positioning adjustment is partly done. Key additional step: cite Bancroft and Judge-Bock explicitly in the introduction to Section 5 and frame the risk hump result as a confirmation of general pretest theory in the masked Weibull setting, not a new phenomenon. No pretest literature applies to reliability functionals or masked data, which is the genuine novelty.

### Threat 3: McCool (1975, 1979) on Equal Shape in Weibull Multi-sample Problems

McCool (1975) in IEEE Transactions on Reliability developed tests for the equality of shape parameters across multiple Weibull populations with Type II censored data. McCool (1979) in Journal of Statistical Planning and Inference gave the general single-classification analysis. This is the closest prior work on the statistical question of testing common shape in Weibull systems. The key difference from the current paper: (a) McCool uses independent samples from separate Weibull populations, not system-level masked competing-risk data; (b) McCool's work provides inference procedures assuming the common-shape model but does not quantify the consequence (bias, MSE) of imposing it when it is wrong; (c) no consequence analysis or detectability-bias decoupling appears. Positioning: cite as the starting point for inference about common Weibull shape, and sharply distinguish the masked-data competing-risk setting and the consequence-analysis framing.

### Threat 4: Hart (2024/2025) in IEEE Transactions on Reliability

Hart, E.J. (2024, online; 2025 print) "Independent competing risks in common shape-parameter Weibull systems, with application to rolling bearing service life," IEEE Transactions on Reliability, Vol. 74(3), pp. 3137-3151, DOI 10.1109/TR.2024.3458173. This paper formalizes statistical estimation under the common-shape Weibull competing-risks model. It is published in the same target venue (IEEE TR). However, it does NOT study misspecification consequences, does NOT use masked cause-of-failure data, and does NOT perform model selection or consequence analysis. It proves unbiasedness of a specific estimator under the assumption that common shape holds. Positioning: this paper corroborates the engineering relevance of the common-shape model but occupies a fully orthogonal niche (validity of estimation when the model is correct vs. consequences when it is wrong). The two papers are complementary; cite Hart as motivation for studying the common-shape assumption.

### Threat 5: Pascual (2005) / Misspecification of Weibull vs. Lognormal Models

Pascual (2005, Communications in Statistics, Vol. 34) derived asymptotic distributions of MLE under misspecified Weibull or lognormal distributions. This is the closest precedent for quantifying MLE bias when the fitted distribution family is wrong. However, Pascual's misspecification is between two full parametric families (Weibull vs. lognormal), not within the Weibull family under a shape constraint. No series system structure, no masking, no competing risks. Also see: the 2017 Physica A paper on the effect of misspecification on mean for Weibull vs. lognormal models. Neither addresses the within-family constraint question. Positioning: cite as establishing the general misspecification-bias framework and contrast with the specific Weibull common-shape constraint case.

---

## Reference Table

| Key | Full Citation | Classification | Relevance |
|-----|---------------|----------------|-----------|
| claeskens2003fic | Claeskens G. and Hjort N.L. (2003). "The focused information criterion." JASA 98(464):900-916. | THREAT / MUST-CITE | Selects models by estimated MSE of a focus parameter under local misspecification; the paper's zero-first-order-gain proposition and pretest Section 5 directly engage this framework |
| hjort2003fma | Hjort N.L. and Claeskens G. (2003). "Frequentist model average estimators." JASA 98(464):879-899. | THREAT / MUST-CITE | Local misspecification framework; derives asymptotic risk of post-model-selection estimators; MTTF is exactly the kind of "focus parameter" they study |
| claeskens2008book | Claeskens G. and Hjort N.L. (2008). Model Selection and Model Averaging. Cambridge University Press. | MUST-CITE | Textbook unification of FIC, AIC, BIC, model averaging; Section 5 and Section 4.5 derivations should reference this |
| claeskens2006cox | Claeskens G. and Hjort N.L. (2006). "Focused information criteria and model averaging for the Cox hazard regression model." JASA 101(476):1449-1464. | SHOULD-CITE | Only FIC application to survival/hazard models found; shows FIC has been extended to lifetime data contexts but not to Weibull series with masking |
| bancroft1944 | Bancroft T.A. (1944). "On biases in estimation due to the use of preliminary tests of significance." Annals of Mathematical Statistics 15(2):190-204. | MUST-CITE | Origin of pretest estimators; the adaptive LRT procedure in Section 5 is a pretest estimator; the risk hump is Bancroft's phenomenon |
| judge1978 | Judge G.G. and Bock M.E. (1978). The Statistical Implications of Pre-Test and Stein-Rule Estimators in Econometrics. North-Holland, Amsterdam. | MUST-CITE | Canonical treatment of pretest estimator risk, MSE, and the risk hump; Section 5 should explicitly situate the n=100 risk hump within this framework |
| giles1993 | Giles J.A. and Giles D.E.A. (1993). "Pre-test estimation and testing in econometrics: Recent developments." Journal of Economic Surveys 7(2):145-197. | SHOULD-CITE | Standard review of pretest estimation theory; demonstrates generality of the risk hump phenomenon |
| danilov2004 | Danilov D. and Magnus J.R. (2004). "On the harm that ignoring pretesting can cause." Journal of Econometrics 122(1):27-46. | SHOULD-CITE | Derives exact bias, variance, MSE of pretest estimator and WALS alternative; confirms the quantitative risk hump |
| leeb2003 | Leeb H. and Potscher B.M. (2003). "The finite-sample distribution of post-model-selection estimators and uniform versus non-uniform approximations." Econometric Theory 19:100-142. | SHOULD-CITE | Shows that post-selection inference is non-uniform; supports honest framing of Section 5 as evaluation not recommendation |
| leeb2005 | Leeb H. and Potscher B.M. (2005). "Model selection and inference: Facts and fiction." Econometric Theory 21(1):21-59. | SHOULD-CITE | Debunks myth that consistent model selection has no asymptotic cost; relevant to the risk hump and n-100 findings |
| mccool1975 | McCool J.I. (1975). "Multiple comparison for Weibull parameters." IEEE Transactions on Reliability 24(3):186-192. | MUST-CITE | Develops tests for equality of Weibull shape parameters across populations; closest prior art on the statistical question; the current paper extends to masked competing-risk series-system data |
| mccool1979 | McCool J.I. (1979). "Analysis of single classification experiments based on censored samples from the two-parameter Weibull distribution." Journal of Statistical Planning and Inference 3:39-68. | SHOULD-CITE | Full ANOVA-style treatment assuming common shape; no consequence analysis or masking |
| hart2024 | Hart E.J. (2024, online). "Independent competing risks in common shape-parameter Weibull systems, with application to rolling bearing service life." IEEE Transactions on Reliability, Vol. 74(3), pp. 3137-3151. DOI 10.1109/TR.2024.3458173. | THREAT (benign) / MUST-CITE | Published in target venue; assumes common shape holds and formalizes estimation; does not study misspecification, masking, or model selection; complementary framing |
| pascual2005 | Pascual F.G. (2005). "Maximum likelihood estimation under misspecified lognormal and Weibull distributions." Communications in Statistics: Simulation and Computation 34(3):503-524. | SHOULD-CITE | Closest prior work on asymptotic MLE bias under parametric misspecification for Weibull-type models; different setting (cross-family misspecification, no series system, no masking) |
| aitchison1958 | Aitchison J. and Silvey S.D. (1958). "Maximum-likelihood estimation of parameters subject to restraints." Annals of Mathematical Statistics 29(3):813-828. | MUST-CITE | Foundation for constrained MLE asymptotics; directly supports the zero-first-order-gain proposition |
| silvey1959 | Silvey S.D. (1959). "The Lagrangian multiplier test." Annals of Mathematical Statistics 30(2):389-407. | SUPPORTING | Score test / LM test framework; triple equivalence (Wald, LR, LM) under H0; supports LRT formulation |
| vandervaart2000 | van der Vaart A.W. (1998). Asymptotic Statistics. Cambridge University Press. | MUST-CITE (already cited) | Le Cam contiguous alternatives, local asymptotic normality, and noncentral chi-square local power derivations |
| casella2002 | Casella G. and Berger R.L. (2002). Statistical Inference, 2nd ed. Duxbury. | MUST-CITE (already cited) | Delta method (Ch. 10); bias-scaling derivation in Section 4.5 |
| white1982 | White H. (1982). "Maximum likelihood estimation of misspecified models." Econometrica 50(1):1-25. | MUST-CITE (already cited) | Pseudo-true parameters and KL-minimization under misspecification; supports framing of reduced-model MTTF bias |
| reiser1995 | Reiser B., Guttman I., Lin D.K.J., Guess F.M., and Usher J.S. (1995). "Bayesian inference for masked system lifetime data." Applied Statistics 44(1):79-90. | SHOULD-CITE | Bayesian treatment of masked series system; earliest comprehensive Bayesian masked-data paper; context for C1-C2-C3 assumptions |
| flehinger1996 | Flehinger B.J., Reiser B., and Yashchin E. (1996). "Inference about defects in the presence of masking." Technometrics 38(3):247-255. | SHOULD-CITE | Foundational paper on parametric masked competing risks from the IBM / Lifetime Data Analysis group |
| flehinger1998 | Flehinger B.J., Reiser B., and Yashchin E. (1998). "Survival with competing risks and masked causes of failures." Biometrika 85(1):151-164. | SHOULD-CITE | Extended parametric framework for masked competing risks; closely related to C1-C2-C3 assumptions |
| flehinger2002 | Flehinger B.J., Reiser B., and Yashchin E. (2002). "Parametric modeling for survival with competing risks and masked failure causes." Lifetime Data Analysis 8(2):177-203. | SHOULD-CITE | Weibull parametric model for masked competing risks; series system context |
| sen2001 | Sen A., Basu S., and Banerjee M. (2001). "Analysis of masked failure data under competing risks." Handbook of Statistics, Vol. 20, pp. 523-540. | SHOULD-CITE | Standard review chapter on masked competing risks; provides context for C1-C2-C3 |
| kuo2000 | Kuo L. and Yang T. (2000). "Bayesian reliability modeling for masked system lifetime data." Statistics and Probability Letters 47(3):229-241. | SHOULD-CITE | Bayesian model selection by predictive approach for masked systems; covers model choice between candidate distributions |
| wellek2010 | Wellek S. (2010). Testing Statistical Hypotheses of Equivalence and Noninferiority, 2nd ed. CRC Press. | TANGENTIAL | Equivalence testing framework; the paper's "safe zone" framing is analogous to equivalence testing but the connection is loose |
| wald1943 | Wald A. (1943). "Tests of statistical hypotheses concerning several parameters when the number of observations is large." Transactions of the American Mathematical Society 54(3):426-482. | SUPPORTING | Asymptotic theory of the Wald test; provides the Wald-LR-LM equivalence supporting Section 4 |

---

## Gap Analysis: What Remains Genuinely Novel

After this survey, the following claims in the paper appear defensible as novel:

### 1. Consequence analysis for common-shape Weibull series with masked, censored data
No prior work quantifies the MTTF (or R(t)) prediction error introduced by imposing common shape on Weibull series system data with masked candidate sets and right censoring. McCool (1975, 1979) tests equality of shapes but never quantifies prediction consequences. Hart (2024) assumes the model is correct. Pascual (2005) quantifies cross-family misspecification but not within-family shape constraints in series systems. The delta-method derivation that bias scales as c_B * CV^2 with n-independent constant is new in this context.

### 2. Zero-first-order-gain proposition for system-level functionals
The claim that the common-shape constraint provides exactly zero asymptotic variance reduction for any system-level functional (MTTF, R(t), quantiles) at any common-shape point is new. FIC theory treats a generic focus parameter and derives its limiting risk, but does not derive a structural zero for constrained estimation of system-lifetime functionals. Aitchison and Silvey (1958) give the asymptotic distribution of the constrained MLE, but the specific consequence for system functionals under the Weibull closure constraint has not been worked out. This proposition, proved via the (k, eta) parameterization, is the strongest claim in the paper and appears to be genuinely novel.

### 3. Decoupling of bias (n-independent) from detectability (sqrt(n)-rate) in masked competing risks
The specific decoupling result: bias is a population quantity independent of n while detection power scales as n * CV^2 (Le Cam ncp) has not been stated for masked competing-risks data. The Hjort-Claeskens local misspecification framework uses O(1/sqrt(n)) neighborhoods, which conflates the two rates. The current paper's contribution is distinguishing fixed misspecification from local misspecification and showing that for the common-shape reduction, practical safety is structural (not asymptotic). This framing appears new.

### 4. Empirical calibration of pretest risk hump in masked reliability setting
While the risk hump is classical (Bancroft 1944, Judge-Bock 1978), no prior work demonstrates it for Weibull series system estimation with masked data. The quantitative characterization (+17% RMSE at n=100, vanishing by n=500) is an empirical contribution specific to this engineering context. The paper should frame this as "confirming classical pretest theory in the masked Weibull series setting" rather than claiming the hump itself is new.

### 5. Empirically calibrated constants
The constants c_B approximately 0.30-0.35 and c_D approximately 0.50 and the CV50 approximately 3.5/sqrt(n) threshold are engineering deliverables not derivable from general theory. These constants are specific to the Weibull series system structure and are not found anywhere in the general model selection or pretest literature.

### What the paper CANNOT claim as novel
- The existence of a pretest risk hump (Bancroft 1944, Judge-Bock 1978).
- LRT as a model selection tool for nested models (Wilks 1938, textbook).
- The Weibull closure property (Barlow-Proschan 1975).
- General consequences of model misspecification (White 1982).
- FIC as a framework for focus-parameter-targeted model selection (Claeskens-Hjort 2003).

---

## BibTeX Block

```bibtex
@article{claeskens2003fic,
  author  = {Claeskens, Gerda and Hjort, Nils Lid},
  title   = {The Focused Information Criterion},
  journal = {Journal of the American Statistical Association},
  volume  = {98},
  number  = {464},
  pages   = {900--916},
  year    = {2003},
  doi     = {10.1198/016214503000000819}
}

@article{hjort2003fma,
  author  = {Hjort, Nils Lid and Claeskens, Gerda},
  title   = {Frequentist Model Average Estimators},
  journal = {Journal of the American Statistical Association},
  volume  = {98},
  number  = {464},
  pages   = {879--899},
  year    = {2003},
  doi     = {10.1198/016214503000000828}
}

@book{claeskens2008book,
  author    = {Claeskens, Gerda and Hjort, Nils Lid},
  title     = {Model Selection and Model Averaging},
  publisher = {Cambridge University Press},
  address   = {Cambridge},
  year      = {2008},
  series    = {Cambridge Series in Statistical and Probabilistic Mathematics},
  isbn      = {9780521852258}
}

@article{claeskens2006cox,
  author  = {Claeskens, Gerda and Hjort, Nils Lid},
  title   = {Focused Information Criteria and Model Averaging for the {Cox} Hazard Regression Model},
  journal = {Journal of the American Statistical Association},
  volume  = {101},
  number  = {476},
  pages   = {1449--1464},
  year    = {2006},
  doi     = {10.1198/016214506000000069}
}

@article{bancroft1944,
  author  = {Bancroft, Theodore A.},
  title   = {On Biases in Estimation Due to the Use of Preliminary Tests of Significance},
  journal = {Annals of Mathematical Statistics},
  volume  = {15},
  number  = {2},
  pages   = {190--204},
  year    = {1944},
  doi     = {10.1214/aoms/1177731284}
}

@book{judge1978,
  author    = {Judge, George G. and Bock, M. E.},
  title     = {The Statistical Implications of Pre-Test and {Stein}-Rule Estimators in Econometrics},
  publisher = {North-Holland},
  address   = {Amsterdam},
  year      = {1978}
}

@article{giles1993,
  author  = {Giles, Judith A. and Giles, David E. A.},
  title   = {Pre-Test Estimation and Testing in Econometrics: Recent Developments},
  journal = {Journal of Economic Surveys},
  volume  = {7},
  number  = {2},
  pages   = {145--197},
  year    = {1993},
  doi     = {10.1111/j.1467-6419.1993.tb00163.x}
}

@article{danilov2004,
  author  = {Danilov, D. and Magnus, J. R.},
  title   = {On the Harm That Ignoring Pretesting Can Cause},
  journal = {Journal of Econometrics},
  volume  = {122},
  number  = {1},
  pages   = {27--46},
  year    = {2004},
  doi     = {10.1016/S0304-4076(03)00268-9}
}

@article{leeb2003,
  author  = {Leeb, Hannes and P\"{o}tscher, Benedikt M.},
  title   = {The Finite-Sample Distribution of Post-Model-Selection Estimators and Uniform versus Non-Uniform Approximations},
  journal = {Econometric Theory},
  volume  = {19},
  pages   = {100--142},
  year    = {2003},
  doi     = {10.1017/S0266466603191062}
}

@article{leeb2005,
  author  = {Leeb, Hannes and P\"{o}tscher, Benedikt M.},
  title   = {Model Selection and Inference: Facts and Fiction},
  journal = {Econometric Theory},
  volume  = {21},
  number  = {1},
  pages   = {21--59},
  year    = {2005},
  doi     = {10.1017/S0266466605050036}
}

@article{mccool1975,
  author  = {McCool, John I.},
  title   = {Multiple Comparison for {Weibull} Parameters},
  journal = {IEEE Transactions on Reliability},
  volume  = {24},
  number  = {3},
  pages   = {186--192},
  year    = {1975},
  doi     = {10.1109/TR.1975.5215145}
}

@article{mccool1979,
  author  = {McCool, John I.},
  title   = {Analysis of Single Classification Experiments Based on Censored Samples from the Two-Parameter {Weibull} Distribution},
  journal = {Journal of Statistical Planning and Inference},
  volume  = {3},
  number  = {1},
  pages   = {39--68},
  year    = {1979},
  doi     = {10.1016/0378-3758(79)90017-X}
}

@article{hart2024,
  author  = {Hart, Edward J.},
  title   = {Independent Competing Risks in Common Shape-Parameter {Weibull} Systems, with Application to Rolling Bearing Service Life},
  journal = {IEEE Transactions on Reliability},
  volume  = {74},
  number  = {3},
  pages   = {3137--3151},
  year    = {2025},
  note    = {Published online 2024-10-04},
  doi     = {10.1109/TR.2024.3458173}
}

@article{pascual2005,
  author  = {Pascual, Francis G.},
  title   = {Maximum Likelihood Estimation Under Misspecified Lognormal and {Weibull} Distributions},
  journal = {Communications in Statistics: Simulation and Computation},
  volume  = {34},
  number  = {3},
  pages   = {503--524},
  year    = {2005},
  doi     = {10.1081/SAC-200068380}
}

@article{aitchison1958,
  author  = {Aitchison, J. and Silvey, S. D.},
  title   = {Maximum-Likelihood Estimation of Parameters Subject to Restraints},
  journal = {Annals of Mathematical Statistics},
  volume  = {29},
  number  = {3},
  pages   = {813--828},
  year    = {1958},
  doi     = {10.1214/aoms/1177706538}
}

@article{silvey1959,
  author  = {Silvey, Samuel D.},
  title   = {The {Lagrangian} Multiplier Test},
  journal = {Annals of Mathematical Statistics},
  volume  = {30},
  number  = {2},
  pages   = {389--407},
  year    = {1959},
  doi     = {10.1214/aoms/1177706259}
}

@article{reiser1995,
  author  = {Reiser, Benjamin and Guttman, Irwin and Lin, D. K. J. and Guess, Frank M. and Usher, John S.},
  title   = {Bayesian Inference for Masked System Lifetime Data},
  journal = {Applied Statistics},
  volume  = {44},
  number  = {1},
  pages   = {79--90},
  year    = {1995},
  doi     = {10.2307/2986189}
}

@article{flehinger1996,
  author  = {Flehinger, Betty J. and Reiser, Benjamin and Yashchin, Emanuel},
  title   = {Inference About Defects in the Presence of Masking},
  journal = {Technometrics},
  volume  = {38},
  number  = {3},
  pages   = {247--255},
  year    = {1996},
  doi     = {10.1080/00401706.1996.10484502}
}

@article{flehinger1998,
  author  = {Flehinger, Betty J. and Reiser, Benjamin and Yashchin, Emanuel},
  title   = {Survival with Competing Risks and Masked Causes of Failures},
  journal = {Biometrika},
  volume  = {85},
  number  = {1},
  pages   = {151--164},
  year    = {1998},
  doi     = {10.1093/biomet/85.1.151}
}

@article{flehinger2002,
  author  = {Flehinger, Betty J. and Reiser, Benjamin and Yashchin, Emanuel},
  title   = {Parametric Modeling for Survival with Competing Risks and Masked Failure Causes},
  journal = {Lifetime Data Analysis},
  volume  = {8},
  number  = {2},
  pages   = {177--203},
  year    = {2002},
  doi     = {10.1023/A:1014891707936}
}

@incollection{sen2001,
  author    = {Sen, Ananda and Basu, Sanjib and Banerjee, Mousumi},
  title     = {Analysis of Masked Failure Data Under Competing Risks},
  booktitle = {Handbook of Statistics},
  volume    = {20},
  pages     = {523--540},
  year      = {2001},
  publisher = {Elsevier},
  address   = {Amsterdam}
}

@article{kuo2000,
  author  = {Kuo, Lynn and Yang, Tipu},
  title   = {Bayesian Reliability Modeling for Masked System Lifetime Data},
  journal = {Statistics and Probability Letters},
  volume  = {47},
  number  = {3},
  pages   = {229--241},
  year    = {2000},
  doi     = {10.1016/S0167-7152(99)00160-1}
}

@article{wald1943,
  author  = {Wald, Abraham},
  title   = {Tests of Statistical Hypotheses Concerning Several Parameters When the Number of Observations Is Large},
  journal = {Transactions of the American Mathematical Society},
  volume  = {54},
  number  = {3},
  pages   = {426--482},
  year    = {1943},
  doi     = {10.1090/S0002-9947-1943-0012401-3}
}
```

---

## Classified Reference List

### Foundational

- **[Barlow and Proschan, 1975]** "Statistical Theory of Reliability and Life Testing: Probability Models." Holt, Rinehart and Winston. Relation: Weibull closure property (Property 1), the unique theoretical motivation for the common-shape reduction.
- **[Usher and Hodgson, 1988]** "Maximum likelihood analysis of component reliability using masked system life-test data." IEEE TR 37(5):550-555. Relation: First MLE treatment of masked series system data.
- **[Lin et al., 1993]** "Exact maximum likelihood estimation using masked system data." IEEE TR 42(4):631-635. Relation: Exact MLE under C1-C2-C3 conditions.
- **[Wilks, 1938]** "The large-sample distribution of the likelihood ratio for testing composite hypotheses." Annals Math. Stat. 9:60-62. Relation: LRT asymptotic distribution.
- **[van der Vaart, 1998]** "Asymptotic Statistics." Cambridge University Press. Relation: Contiguous alternatives, LAN, local power of LRT; Section 4.5 Le Cam derivation.
- **[White, 1982]** "Maximum likelihood estimation of misspecified models." Econometrica 50(1):1-25. Relation: Pseudo-true parameters; theoretical basis for studying estimand under misspecification.
- **[Aitchison and Silvey, 1958]** "Maximum-likelihood estimation of parameters subject to restraints." Annals Math. Stat. 29(3):813-828. Relation: Constrained MLE asymptotics; directly supports zero-first-order-gain proposition.
- **[Casella and Berger, 2002]** "Statistical Inference," 2nd ed. Duxbury. Relation: Delta method; bias-scaling derivation in Section 4.5.
- **[Lawless, 2003]** "Statistical Models and Methods for Lifetime Data," 2nd ed. Wiley. Relation: Standard reference for lifetime data analysis; Weibull models, competing risks.
- **[Meeker and Escobar, 1998]** "Statistical Methods for Reliability Data." Wiley. Relation: Standard reference for reliability data; Weibull inference.
- **[Bancroft, 1944]** "On biases in estimation due to the use of preliminary tests of significance." Annals Math. Stat. 15(2):190-204. Relation: Origin of pretest estimators; Section 5 adaptive procedure.
- **[Burnham and Anderson, 2002]** "Model Selection and Multimodel Inference," 2nd ed. Springer. Relation: AIC/BIC context; Section 5 information-criteria comparators.

### Competing (Novelty Threats)

- **[Claeskens and Hjort, 2003]** "The focused information criterion." JASA 98(464):900-916. Relation: Selects models by estimated MSE of a focus parameter (e.g., MTTF) under local misspecification; the paper's zero-first-order-gain proposition and Section 4.5 derivation sit within this framework; no application to masked competing-risk series data.
- **[Hjort and Claeskens, 2003]** "Frequentist model average estimators." JASA 98(464):879-899. Relation: Local misspecification framework and asymptotic risk of post-model-selection estimators; foundational companion to FIC paper.
- **[Claeskens and Hjort, 2008]** "Model Selection and Model Averaging." Cambridge University Press. Relation: Book unification of FIC/AIC/BIC; Section 5 framing and Section 4.5 local-alternatives derivation should position against Chapter 5.
- **[McCool, 1975]** "Multiple comparison for Weibull parameters." IEEE TR 24(3):186-192. Relation: Tests equality of Weibull shape parameters across populations; no consequence analysis, no masked data.
- **[Hart, 2024/2025]** "Independent competing risks in common shape-parameter Weibull systems." IEEE TR 74(3):3137-3151. Relation: Published in target venue; formalizes estimation assuming common shape holds; does not study misspecification, masking, or model selection.
- **[Judge and Bock, 1978]** "The Statistical Implications of Pre-Test and Stein-Rule Estimators in Econometrics." North-Holland. Relation: Canonical MSE/risk treatment of pretest estimators; the n=100 risk hump is their prediction.
- **[Leeb and Potscher, 2003/2005]** Econometric Theory. Relation: Show post-selection inference is non-uniform; Section 5 honest framing relies on this understanding.
- **[Pascual, 2005]** "Maximum likelihood estimation under misspecified lognormal and Weibull distributions." Comm. Stat. 34(3):503-524. Relation: Asymptotic bias of MLE under Weibull misspecification; different setting (cross-family, no series structure).

### Complementary

- **[Craiu and Lee, 2005]** "Model selection for the competing-risks model with and without masking." Technometrics 47(4):457-467. Relation: Model selection for masked competing risks using piecewise-constant hazards; not Weibull series system; no consequence analysis.
- **[Flehinger et al., 1996/1998/2002]** Technometrics / Biometrika / Lifetime Data Analysis. Relation: Parametric masked competing risks program from IBM group; series-system context using Weibull; no model selection or consequence analysis.
- **[Reiser et al., 1995]** "Bayesian inference for masked system lifetime data." Applied Statistics 44(1):79-90. Relation: Bayesian estimation and model comparison for masked series systems.
- **[Kuo and Yang, 2000]** "Bayesian reliability modeling for masked system lifetime data." Stat. Prob. Lett. 47(3):229-241. Relation: Bayesian model selection by predictive approach for masked systems.
- **[Sen, Basu and Banerjee, 2001]** Handbook of Statistics Vol. 20. Relation: Standard review of masked competing-risks analysis; C1-C2-C3 context.
- **[Giles and Giles, 1993]** "Pre-test estimation and testing in econometrics." J. Econ. Surveys 7:145-197. Relation: Review of pretest theory relevant to Section 5 framing.
- **[Danilov and Magnus, 2004]** "On the harm that ignoring pretesting can cause." J. Econometrics 122:27-46. Relation: Quantifies MSE consequences of ignoring pretest step; confirms risk hump phenomenon.
- **[Claeskens and Hjort, 2006 Cox]** "Focused information criteria for Cox hazard regression." JASA 101:1449-1464. Relation: Only FIC application to survival/lifetime context found; no extension to Weibull or masked data.
- **[McCool, 1979]** J. Stat. Plan. Infer. 3:39-68. Relation: Analysis-of-variance framework assuming common Weibull shape; no misspecification study or masked data.
- **[Hart, 2024/2025]** IEEE TR 74(3). Relation: Directly assumes and formalizes common-shape Weibull competing risks; motivates studying robustness of this assumption.

### Tangential

- **[Wellek, 2010]** "Testing Statistical Hypotheses of Equivalence and Noninferiority," 2nd ed. CRC. Relation: Equivalence testing concept is analogous to the paper's "safe zone" framing but no technical connection exploited.
- **[Wald, 1943]** Transactions AMS 54:426-482. Relation: Asymptotic theory of Wald test; Wald-LR-LM equivalence.
- **[Silvey, 1959]** Annals Math. Stat. 30:389-407. Relation: Score test / Lagrange multiplier test; supports LRT equivalence claims.
- **[Leeb and Potscher, 2003]** Econometric Theory 19:100-142. Relation: Post-selection distributional theory; relevant to Section 5 honest framing.
- **[Leeb and Potscher, 2005]** Econometric Theory 21:21-59. Relation: Facts about model selection inference; supports acknowledging limitations in Section 5.

---

## Search Log

All searches performed via WebSearch on 2026-06-10.

1. "Claeskens Hjort focused information criterion 2003 JASA model selection focus parameter"
2. "Hjort Claeskens 2003 frequentist model average estimators JASA local misspecification"
3. "Claeskens Hjort 2008 model selection and model averaging Cambridge book"
4. "FIC focused information criterion survival analysis Cox model lifetime data reliability"
5. "Claeskens Hjort focused information criterion Cox hazard regression 2006 JASA survival"
6. "pretest estimation Bancroft 1944 Judge Bock 1978 statistical implications pre-test estimators risk"
7. "Danilov Magnus 2004 on the harm that ignoring pretesting can cause pretest estimator risk hump"
8. "Magnus 1999 2002 pretest estimation ridge regression weighted average least squares econometrics"
9. "Leeb Potscher 2003 2005 finite sample model selection post-selection inference risk uniformly"
10. "Giles Giles 1993 pre-test estimation review econometrics risk mean squared error"
11. "McCool 1974 inference Weibull common shape parameter equality test competing risks reliability"
12. "McCool 1975 IEEE Transactions Reliability multiple comparison Weibull shape parameters testing homogeneity"
13. "McCool 1974 Weibull populations inference analysis single classification shape equality likelihood ratio"
14. "common shape Weibull competing risks test inference hypothesis equal shape series reliability 2000 2010"
15. "Hart 2024 IEEE Transactions Reliability common shape parameter Weibull competing risks inference DOI"
16. "Aitchison Silvey 1958 constrained maximum likelihood asymptotic distribution restricted estimators"
17. "Silvey 1959 the Lagrangian multiplier test Annals Mathematical Statistics constrained estimation score test"
18. "van der Vaart 1998 asymptotic statistics Cambridge local power LRT contiguous alternatives Le Cam"
19. "Le Cam 1960 locally asymptotically normal statistical experiments contiguous alternatives power"
20. "Flehinger Reiser Yashchin 1996 estimating component reliability from masked system life data Technometrics"
21. "Flehinger Reiser Yashchin 1998 estimation reliability masked competing risks Technometrics OR Lifetime Data"
22. "Flehinger Reiser Yashchin 2001 masked competing risks masking diagnosis reliability Biometrika Technometrics"
23. "Reiser Guttman Lin Usher Guess 1995 Bayesian inference masked competing risks series system"
24. "Sen Basu Banerjee 2001 masked competing risks review estimation series system components"
25. "Kuo Yang 2000 Bayesian masked system life data competing risks Weibull"
26. "consequence analysis OR consequence of misspecification Weibull shape parameter series system model selection bias"
27. "misspecification Weibull common shape model selection bias MTTF reliability component lifetime"
28. "effect of misspecification Weibull lognormal mean selection models reliability 2017 Physica A"
29. "Pascual 2005 maximum likelihood estimation misspecified lognormal Weibull MLE quantiles bias"
30. "White 1982 maximum likelihood estimation misspecified models Econometrica pseudo-true parameters KL"
31. "Wellek 2010 testing statistical hypotheses of equivalence practical significance model closeness"
32. "FIC focused information criterion Weibull reliability lifetime data engineering application"
33. "Bancroft 1944 biases preliminary test significance estimation statistics original paper"
34. "Judge Bock 1978 statistical implications pretest Stein-rule estimators North-Holland publication details"
35. "Casella Berger 2002 statistical inference second edition Duxbury delta method asymptotic"
36. "Wald 1943 tests of statistical hypotheses concerning several parameters Annals Mathematical Statistics"

Coverage notes:
- Focused on verifying existence before listing any reference.
- McCool 1974 technical report (ARL TR 74-0180) was not verified as a published journal article; McCool 1975 (IEEE TR) and 1979 (JSPI) are the verified peer-reviewed works.
- Hart 2024/2025 (IEEE TR 74(3):3137-3151, DOI 10.1109/TR.2024.3458173) is a genuine novelty competitor in the target venue; verified via Strathprints institutional repository.
- FIC has been applied to Cox models but no application to Weibull series or masked data was found in any search.
- No paper combining pretest estimation with Weibull reliability functionals or masked series-system data was found.
- The 2017 Physica A paper on Weibull vs. lognormal misspecification effect on mean was found but not included in BibTeX because it studies cross-family misspecification (different from within-family shape constraint) and is only tangentially related.
