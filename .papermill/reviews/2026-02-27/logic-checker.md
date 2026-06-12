# Logic Checker Report

**Date**: 2026-02-27
**Paper**: "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"

## Summary

The paper's logical structure is sound. The central argument flows cleanly: (1) quantify consequence of misspecification, (2) quantify detectability, (3) show they align favorably, (4) exploit the alignment with an adaptive procedure. No formal proofs are presented -- the paper relies entirely on simulation evidence, which is appropriate for its empirical claims.

## Findings

### Major Issues

#### M1: "Rejects at 80%" Claim is Slightly Overstated
- **Location**: Abstract, Section 3.3, Section 6 (Conclusion), repeated throughout
- **Claim**: "by the time it reaches 1.5% (CV ~ 20%) the LRT already rejects at 80%"
- **Data**: At actual CV = 20.5% and n=500, the rejection rate is 78.1% (from raw simulation data)
- **Severity**: Minor overstatement but it appears in the abstract and conclusion
- **Suggestion**: Round to "nearly 80%" or "approximately 80%" or report 78% directly

#### M2: "Full Model Has Lower MSE Even at CV=0" Claim Needs Qualification
- **Location**: Section 3.3, Section 6
- **Claim**: "the full model has lower MSE than the reduced model at practical sample sizes -- even when the reduced model is correctly specified (CV = 0)"
- **Data**: This holds at n=100 (ratio 0.867), n=500 (0.980), n=1000 (0.984), but at n=5000 the ratio is 1.002 -- the full model's MSE is marginally higher
- **Severity**: The phrase "practical sample sizes" is doing the heavy lifting. The claim is correct for n <= 1000 but reverses at n=5000
- **Suggestion**: Add "at n <= 1000" or "at moderate sample sizes" as qualification. The reversal at n=5000 is expected (more data overcomes the variance penalty of extra parameters) and would actually strengthen the narrative

### Minor Issues

#### m1: Bias-Variance Decomposition Invoked but Not Shown
- **Location**: Section 3.3
- **Claim**: "A bias-variance decomposition reveals the mechanism: the constraint k_1 = ... = k_m forces all shape estimation error into a single degree of freedom..."
- **Problem**: The bias-variance decomposition is mentioned but the actual numbers (variance of full vs reduced, bias^2 components) are not presented in any table or figure
- **Suggestion**: Either add a brief table showing the decomposition at CV=0 for one sample size, or soften the language to "we conjecture that" or "this is consistent with a mechanism where..."

#### m2: "Only Single-Parameter Restriction" Claim
- **Location**: Section 2.3
- **Claim**: "The common-shape constraint is the only single-parameter restriction that yields a Weibull system lifetime"
- **Problem**: This is stated without proof. While it is likely true (constraining all shapes equal reduces the sum of power functions to a single power function), a brief justification would strengthen the claim
- **Suggestion**: Add one sentence of justification, e.g., "since a sum of power functions (t/lambda_j)^{k_j} reduces to a single power function only when all exponents are equal"

#### m3: Direction of Bias Explanation
- **Location**: Section 3.2
- **Claim**: "the reduced model systematically overestimates MTTF because the common-shape fit overestimates the weaker components"
- **Problem**: The mechanistic explanation is plausible but not proven. The common-shape estimate pools toward the mean shape; components with lower shapes (weaker hazard growth) would have their shapes overestimated, potentially making them appear more reliable. But the MTTF depends on all components through a min() operation, so the actual mechanism is more subtle
- **Suggestion**: Soften to "likely because" or provide a more precise mechanistic explanation

### Logical Chain Assessment

The paper's core logical chain is:

1. MTTF bias is small when CV is small -- **supported by Table 2, verified against raw data**
2. LRT power is low when CV is small -- **supported by Table 3, verified against raw data**
3. LRT power grows faster than bias -- **supported by Figure 1, verified: at CV=20.5%, bias=1.5% while rejection=78%**
4. Therefore an adaptive procedure works -- **supported by Table 4 and Figure 2**
5. The procedure adds no computational cost -- **logically correct since both fits are required for the test**

The chain is sound. The main vulnerability is that it relies on a single baseline system configuration, which the paper acknowledges in its limitations.

## Confidence: HIGH

The logical structure is clean and well-supported by evidence. The issues identified are minor overstatements rather than logical errors.
