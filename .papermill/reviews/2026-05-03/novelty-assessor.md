# Novelty Assessor Report

**Reviewer role**: contribution clarity, differentiation, significance.
**Manuscript reviewed**: `qrei/manuscript.tex`.
**Date**: 2026-05-03

## Summary

The paper has *one* genuinely novel contribution and *two* contributions that are framing repackaging of known techniques applied to a specific setting. The framing in the abstract and introduction conflates the three. With honest restructuring, the novelty case is solid for QREI and probably acceptable for IEEE TR. As-is, a sharp reviewer at IEEE TR may push back on the "adaptive procedure" claim.

**Severity counts**: critical 0, major 3, minor 2, suggestions 2.

## Major Findings

### MAJ-N1: The headline contribution is real and worth defending more carefully
**The actual novelty**: quantitative consequence analysis of common-shape misspecification for Weibull series systems under realistic masked plus right-censored data. This intersection (Weibull series, masked, common-shape vs heterogeneous, prediction-bias quantification) is unoccupied in the literature, as confirmed by the literature scout.

**Current framing weakness**: the Introduction (lines 51-52) frames the novelty as "the right question" rather than as "an unanswered question." This is a rhetorical move that some reviewers will flag as posturing. A factually equivalent but harder-to-attack framing:

> "Existing work has established that the LRT can detect shape heterogeneity [cite], that the common-shape model is computationally simpler [cite], and that masked-data MLE is consistent under regularity conditions [cite]. What is *not* established is whether the prediction error introduced by the common-shape constraint is engineering-significant when shapes differ slightly. We provide the first quantitative answer to this question."

**Fix**: rewrite the "wrong question / right question" pair as a gap statement. This costs nothing rhetorically and removes a snipe target.

### MAJ-N2: The "MSE surprise" is the most novel finding and is undersold
**Quoted text** (Section 3.3, lines 178-179):
> "A surprising finding is that the full model has lower MSE than the reduced model at moderate sample sizes ($n \leq 1000$), even when the reduced model is correctly specified ($\text{CV} = 0$)."

**Why it's undersold**: this is genuinely counter-intuitive and contradicts the standard parsimony argument. It is *the* finding most likely to make a reader say "huh." But:
- It is buried in Section 3.3 Discussion.
- It is not in the abstract.
- It is not in the contributions list (Contribution 1 mentions it in passing as a "surprisingly").
- The mechanism is asserted not derived (see logic-checker MIN-L2).

**Fix**: elevate to its own contribution. Suggested rewrite of contributions:

> Contribution 1: Bias-detectability alignment (as currently stated).
> Contribution 2 (new): Failure of the parsimony argument for system-level MTTF. The full model has lower MTTF MSE than the reduced model even when the reduced model is correctly specified. We trace this to the asymmetric variance amplification of the constrained estimator through the nonlinear MTTF integral.
> Contribution 3 (the current Contribution 2): Adaptive selection (revised, see MAJ-N3).

This gives the paper three contributions instead of two and makes the most novel one prominent. Three contributions also reads as a more conventional structure for journal reviewers.

### MAJ-N3: The adaptive procedure is empirical evaluation, not invention. Claim should reflect this.
**Quoted text** (Contributions, line 65):
> "Adaptive model selection: An LRT-based procedure exploits this alignment, achieving RMSE within 2.5% of the always-full strategy at $n \geq 500$..."

**Problem**: LRT-based nested model selection is textbook (Wilks 1938, every reliability textbook). The procedure described in Section 5.1 is: "fit both, compute $\Lambda$, use the smaller model if $\Lambda < \chi^2_{m-1, 1-\alpha}$." This is not a new procedure. The contribution is *evaluating* it for *this* problem and showing it works.

A subtler question: does the *alignment exploitation* framing add novelty? Marginally. The fact that LRT-based selection profile happens to be favorable for this prediction problem is a property of the data-generating process, not of the procedure. The "exploits" framing slightly mystifies what is going on (the procedure does the same thing it always does; the alignment is a property of the world).

**Fix**: rephrase as evaluation:

> "Adaptive model selection performance: We evaluate the standard LRT-based selection rule at $\alpha = 0.05$ on this problem. The selection rule achieves RMSE within 2.5% of always-full at $n \geq 500$ while selecting the reduced model > 90% of the time when data support it. The procedure's effectiveness is a direct consequence of the alignment property of contribution 1."

This is honest, defends against the "you didn't invent the LRT" critique, and is rhetorically stronger because it explains *why* the procedure works.

## Minor Findings

### MIN-N1: The "Property 1" framing is fine but could go further
The Weibull closure property is a property of the family. Calling it "Property 1" implies the paper is establishing a property; it is recalling a known one (correctly cited to Barlow-Proschan). The framing is non-deceptive but suggests originality where there is none. A reader skimming will see "Property 1" and think it is a contribution.

**Fix**: rename as "Lemma" or "Fact" with the inline citation kept. Or leave as-is; this is taste.

### MIN-N2: The contribution count in the Introduction does not match the structure of the paper
The Introduction lists 2 contributions. Sections 3, 4, 5 each have substantive results. After MAJ-N2 fix, the Introduction would list 3 and the structure would line up. As-is there is a slight mismatch.

## Suggestions

### SUG-N1: Add a "What this paper is not" sentence
A brief paragraph clarifying that this paper does *not*:
- propose new estimators
- derive new closure properties
- introduce a new test statistic
... and *does*:
- quantify a previously-unmeasured prediction error
- characterize an empirical alignment property
- identify a counter-intuitive variance phenomenon

This pre-empts "you've done less than you claim" reactions.

### SUG-N2: Cite the Focused Information Criterion (Claeskens-Hjort 2003, 2008)
FIC is the conceptual ancestor of "consequence analysis." Even one citation acknowledges the lineage and gives reviewers a place to ground the framing. The paper does not need to use FIC machinery, but should signal awareness.

## Differentiation Map

Where this paper fits among the things it could be confused with:

| Reference work | What it does | What's missing that this paper provides |
|----------------|--------------|------------------------------------------|
| Sarhan (2001, 2004), Tan (2007) | Estimates parameters under masking | Does not study common-shape vs full constraint |
| Usher (1996) | Weibull masked-data MLE specifically | No model selection or consequence analysis |
| Craiu and Lee (2005) | Model selection for masked competing risks | Selects between *families* not *constraints* within a family |
| Pascual (2005) | Misspecification consequences for Weibull vs lognormal | No masking, no series structure |
| White (1982) | MLE under misspecification, abstract | No specific application |
| Pareek-Kundu-Kumar (2009) | Common-shape Weibull competing risks | No masking, no consequence analysis |

The unoccupied cell is exactly this paper's cell. Novelty is real.

## Verdict

The novelty is genuine but the framing is uneven. The most novel finding (MSE surprise) is undersold; the least novel claim (adaptive procedure as invention) is somewhat oversold. Neither problem is severe. With ~30 minutes of rewriting (mostly the Introduction and the contribution list), the novelty story is clean enough for any of the four target venues.

For the venue question (QREI vs IEEE TR vs Technometrics vs LDA): the *novelty profile* by itself does not select among these. Novelty is sufficient for QREI and IEEE TR; Technometrics and LDA would expect more theoretical contribution, which is exactly what the structural derivation (logic-checker MAJ-L1) would supply.

Confidence: high.
