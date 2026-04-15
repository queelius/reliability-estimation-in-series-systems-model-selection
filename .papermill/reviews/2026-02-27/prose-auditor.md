# Prose Auditor Report

**Date**: 2026-02-27
**Paper**: "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"

## Overall Writing Quality

The paper is well-written with clear, direct prose. The narrative arc is strong: the "wrong question/right question" framing in the introduction is effective, and the paper maintains focus throughout. The writing is appropriate for QREI's applied engineering audience.

## Strengths

1. **Strong opening hook**: The turbine engine example in the introduction immediately grounds the abstract problem in engineering reality
2. **Clear question framing**: "This is the wrong question. The right question is: when the reduced model is wrong, does it produce predictions that are wrong enough to change an engineering decision?" -- excellent rhetorical move
3. **Concise abstract**: The abstract efficiently conveys all key findings with specific numbers
4. **Consistent terminology**: Full/reduced model terminology is used consistently throughout
5. **Good use of tables and figures**: Data is presented clearly with appropriate precision

## Issues

### Major

#### P1: Repetitive Central Message
- **Problem**: The paper's central finding (bias <1% through CV~15%, LRT rejects at 80% by CV~20%) is stated nearly verbatim in the abstract, Section 1.2 (Contributions), Section 3.3 (Discussion), Section 5.4 (Discussion), and Section 6 (Conclusion) -- five times with almost identical wording
- **Impact**: Reads as padding and reduces the paper's impact through diminishing returns
- **Suggestion**: State the finding precisely once (Section 3), reference it concisely elsewhere. The conclusion should synthesize rather than repeat

### Minor

#### p1: Section 4 (LRT) Ordering
- **Problem**: The LRT section (Section 4) comes after the consequence analysis (Section 3), but the consequence analysis already uses LRT rejection rates (Figure 1). This creates a forward reference
- **Impact**: Mild reader confusion -- the LRT is used before it is formally introduced
- **Suggestion**: Either move the LRT formulation to Section 2 (framework) or add a brief forward reference in Section 3

#### p2: Table 2 Mixed Units
- **Problem**: RMSE is reported in "time units" while bias is in %. A reader comparing across rows needs to know that MTTF_true varies with CV (it changes from ~222 at CV=0 to a different value at CV=41%). The table caption says "time units" but does not clarify that the true MTTF is approximately constant across CVs (only shapes change, not scales, so system MTTF changes modestly)
- **Suggestion**: Add MTTF_true column or express RMSE as % of true MTTF (as done in Table 4)

#### p3: "Well-Designed System" Not Formally Defined
- **Problem**: The term "well-designed system" appears several times but is never formally defined beyond the informal description "components age similarly (k_j ~ k) but differ in durability (lambda_j)"
- **Suggestion**: Define precisely: "We define a well-designed series system as one whose component shape parameters have CV_k < X%"

#### p4: Appendix Brevity
- **Problem**: The two appendices (A: Data Quality Effects, B: AIC/BIC Comparison) are quite brief -- each is essentially one paragraph plus one table/figure. For a journal paper, these could be incorporated into the main text
- **Suggestion**: Consider merging Appendix A content into Section 4 and Appendix B into Section 4 as well, which would fill out the LRT section

#### p5: Section 5 "Three Strategies" but Code Has Four
- **Problem**: Section 5.2 says "We compare three strategies" (always-full, always-reduced, adaptive LRT). But the simulation code (adaptive-selection.R) also implements a fourth strategy: adaptive-CV (threshold on estimated CV). This fourth strategy is not mentioned in the paper
- **Impact**: Not a prose error per se, but a missed opportunity or a vestige of earlier drafts
- **Suggestion**: Either mention the CV-based strategy and explain why it was dropped, or ensure the paper matches the code

#### p6: Missing Transition Between Sections 3 and 4
- **Problem**: Section 3 ends with Figure 1 showing the alignment. Section 4 starts with the LRT formulation. There is no transition sentence explaining why we now present the LRT details
- **Suggestion**: Add a brief transition, e.g., "Having established that bias and detectability are favorably aligned, we now examine the LRT's properties in detail."

### Notation

- **Consistent**: Bold theta for parameter vectors, k_j and lambda_j for component parameters, Lambda for LRT statistic
- **Minor inconsistency**: The paper uses both "MTTF" and "$\text{MTTF}$" but this is typographically fine
- **Custom command**: \v{x} for \boldsymbol{x} is used appropriately

### Figures

- **Figure 1**: Effective dual-axis plot. The green band for "acceptable bias" is a nice touch. However, the left axis scale (0-10%) makes the low-CV bias values hard to read
- **Figure 2**: Four-panel figure is informative. Panel (c) for n=100 shows noisy curves that might benefit from smoothing or error bars
- **Figure 3**: AIC/BIC comparison is clear. The bar chart for Type I error is well-designed

## Overall: The writing is strong and appropriate for the venue. The main prose issue is repetition of the central finding. The narrative structure works but could be tightened by integrating the appendices and adding transitions.
