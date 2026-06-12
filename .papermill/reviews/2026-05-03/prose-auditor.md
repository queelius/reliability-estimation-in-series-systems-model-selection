# Prose Auditor Report

**Reviewer role**: writing quality, narrative arc, notation consistency.
**Manuscript reviewed**: `qrei/manuscript.tex`.
**Date**: 2026-05-03

## Summary

The writing is professional and engineering-appropriate. The narrative arc is clean: motivation, problem, finding, exploitation, conclusion. The two prose-level concerns are: (1) the title is neutral while the actual finding is more arresting, and (2) one symbol overload ('p') was flagged in the prior review and may not be fully resolved. Notation is otherwise consistent.

**Severity counts**: critical 0, major 1, minor 4, suggestions 3.

## Major Findings

### MAJ-P1: Title is descriptive but not load-bearing for the actual finding
**Quoted text** (line 27):
> "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"

**Problem**: the title asks a question but does not signal the finding. The most arresting result of the paper is *not* "we did consequence analysis" but "the LRT's power outpaces the prediction bias." A reader scanning a journal table of contents will not know what the paper offers.

**Alternative titles to consider**:
1. "Detection Outpaces Bias: Adaptive Model Selection for Weibull Series Systems with Masked Data"
2. "When Does Common-Shape Misspecification Matter? Bias and Detection in Weibull Series Systems"
3. "Common-Shape Simplification of Weibull Series Systems: Detection Power Outpaces Prediction Bias"

The current title is *fine*. It is not wrong. But for IEEE TR (and the open-access circulation that comes with it), a title that signals the finding is worth considering. For QREI house style, the current title is on-brand (QREI publishes many "When does X matter?" papers).

**Recommendation**:
- For QREI: keep current title, possibly add a subtitle. "When Does Model Simplification Matter? Detection Power Outpaces Bias in Weibull Series Systems with Masked Data."
- For IEEE TR: change to one of options 1-3 above.

This is the one prose-level decision that varies by venue.

## Minor Findings

### MIN-P1: Symbol overload ('p') is partially mitigated but worth a re-check
**Locations**: $p$ as masking probability (Section 2.4: "$p = 0.215$"); $p$ never appears in the manuscript text as either parameter count or p-value.

**Verification**: I grepped for "p =", "p-value", and the AIC/BIC discussion. The AIC and BIC formulas are not stated explicitly (they are referenced via citation only). No conflict with masking probability appears. The prior 2026-02-27 critique is mitigated by the current text simply not using $p$ for parameter count.

**Status**: minor. The symbol overload is not currently active. But if Appendix D's AIC/BIC formulas are made more explicit in revision (which a careful reviewer might request), the overload comes back. Author should be aware.

**Suggestion**: leave as-is unless the AIC/BIC discussion expands.

### MIN-P2: "Wrong question / right question" pivot reads as posturing
**Quoted text** (Introduction, lines 51-52):
> "The existing literature on this question focuses almost entirely on whether a likelihood ratio test can *detect* the difference between models. This is the wrong question. The right question is: when the reduced model is wrong, does it produce predictions that are wrong enough to change an engineering decision?"

**Problem**: rhetorical "the wrong question / the right question" framing is brittle. A reader will reasonably ask: was it really the wrong question? Existing detection-focused work has applications too. The framing implies that prior workers asked the wrong question, when in fact they asked a different question.

**Fix**: replace with a gap statement (see novelty MAJ-N1 for the suggested rewrite). This is editorial polish, not substantive change.

### MIN-P3: One inconsistency in CV terminology
**Locations**:
- Section 1: "MTTF bias remains below 1\% through CV $\approx 15\%$"
- Section 3.2: "below 1\% through shape CV $\approx 14\%$ at $n \geq 500$"
- Conclusion: "below 1\% through CV $\approx 15\%$"

**Issue**: the body text says CV ≈ 14% (the most precise number), the abstract and conclusion round to 15%. This is fine if "approximately" is taken seriously, but a careful reader will catch the discrepancy. Looking at Table 2: at CV=13.7%, $n=500$, bias is 0.9%. So "1% threshold not crossed until CV ≈ 14%" is the precise statement. The "15%" version is colloquial.

**Fix**: pick one number and use it consistently. I recommend "CV ≈ 14%" in the abstract and "CV ≈ 14%, n=500" in the conclusion to be precise, *or* the explicit statement "below 1% for all CV ≤ 13.7% at $n=500$" if the table's value is preferred.

### MIN-P4: Figure 1 (alignment) caption could be tighter
**Quoted text** (Figure 1 caption, lines 184-186):
> "The alignment between prediction consequence and statistical detectability at $n = 500$. Left axis (blue): MTTF bias of the reduced model. Right axis (red): LRT rejection rate. The green band marks the $\pm 1\%$ engineering-acceptable bias zone. Detection power outpaces prediction bias: the test lacks power precisely where bias is negligible, and reaches high power before bias becomes engineering-significant."

**Issue**: this is the headline figure of the paper. The caption is functional but could be more declarative. Consider:
> "Bias-detectability alignment at $n = 500$: the LRT power curve (red, right axis) crosses 80% rejection at the same CV where the reduced-model MTTF bias (blue, left axis) reaches 1.5%. The green band marks the $\pm 1\%$ engineering-acceptable zone. The asymmetry: bias remains < 1% through CV ≈ 14%, while LRT power exceeds 80% by CV ≈ 20%."

Concrete numbers in the caption increase scanability.

## Suggestions

### SUG-P1: The Conclusion's three paragraphs read as bullet points dressed up
The Conclusion has three paragraphs (LRT outpaces bias / traditional argument fails / Limitations / Future). Each is a single self-contained idea. Consider unifying into a single tighter paragraph for the first two findings, then a separate Limitations paragraph. As-is the structure feels like a list.

### SUG-P2: Section 5.4 Discussion is one short paragraph
**Quoted text** (lines 290-293):
> "The adaptive procedure succeeds because of the bias-detectability alignment (Figure 1): the LRT has low power precisely where the consequence of misspecification is small, and high power where the consequence is large. The 'incorrect' selections at moderate CV carry negligible penalty because the reduced model's bias is still below 1\% at those CVs. Since both fits are already required to compute $\Lambda$, the procedure adds no cost."

This is fine but somewhat repetitive of points already made. Could be merged into 5.3 Results discussion. Alternatively, expand: discuss when the procedure *fails* (low $n$, high masking, etc.) for symmetry. Current section just rehearses the success story.

### SUG-P3: One typographic point
"Sel.~Red. (\%)" in Table 4 header is a non-standard contraction. "Selected reduced (\%)" or "Reduced selected (\%)" would be cleaner. This is taste.

## Notation Audit

| Symbol | Meaning | Conflict? |
|--------|---------|-----------|
| $\theta$ | full parameter vector | No |
| $\theta_R$ | reduced parameter vector | No |
| $k_j, \lambda_j$ | shape, scale of component $j$ | No |
| $k$ | common shape (reduced model) | Briefly conflicts with subscripted $k_j$, but disambiguation is always clear from context |
| $T_j, T$ | component, system lifetime | No |
| $C_i$ | candidate set | No |
| $\delta_i$ | failure indicator | No |
| $K_i$ | true failed component | No |
| $R(t)$ | reliability function | No |
| $h(t)$ | hazard | No |
| $f(t)$ | density | No |
| $n$ | sample size | No |
| $m$ | number of components | No |
| $p$ | masking probability | No conflict in current text |
| $q$ | censoring quantile | No |
| $\Lambda$ | LRT statistic | No |
| $\alpha$ | significance level | No |

Notation is clean. No internal conflicts in the qrei manuscript text.

## Narrative Arc Audit

1. Section 1 (Introduction): motivates with turbine, defines the choice, frames the question. Good. (one prose issue: the "wrong question / right question" framing, see MIN-P2)
2. Section 2 (Model Framework): defines the system, the data, the closure property, the baseline. Clean.
3. Section 3 (Consequence Analysis): the headline empirical result. Well-organized.
4. Section 4 (LRT): brief, supports the alignment story. Good.
5. Section 5 (Adaptive): the operational payoff. Good.
6. Section 6 (Conclusion): wraps up. Three paragraphs, possibly too short.
7. Appendices A, B (data-quality, AIC/BIC): supplementary.

The arc is well-formed. There is no scaffolding visible to the reader; every section earns its place. This is a sign of mature drafting.

## Verdict

The prose is publication-ready. The one notable decision is the title, which depends on venue. The other concerns are polish items. No prose-level finding is a publication blocker.

Confidence: high.
