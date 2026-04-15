# Logic Check Report

**Date**: 2026-02-27
**Paper**: "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"
**Reviewer focus**: Proof correctness, assumption sufficiency, logical chain integrity, claim support

## Summary

The paper's logical structure is generally sound — the main claims follow from the simulation evidence presented. However, one critical characterization ("sub-linear" bias growth) is contradicted by the data, one major claim conflates data from different experimental conditions, and one explanation is speculative without supporting evidence. No formal proofs are presented; the paper relies entirely on simulation evidence, which is appropriate for its empirical contribution.

---

## Critical Issues

### L1: "Sub-linear" bias characterization is wrong — data shows super-linear growth

- **Location**: Section 3.2, description of MTTF bias vs shape CV
- **Problem**: The paper characterizes MTTF bias growth as "sub-linear" in shape CV. However, fitting a power law to the simulation data yields an exponent of approximately 1.8, meaning bias grows as ~CV^1.8 — this is **super-linear**, not sub-linear.
- **Evidence**: At CV=5%, bias ≈ 0.3%. At CV=20%, bias ≈ 4.5%. If linear, 20/5 = 4x increase would give 1.2%. Actual 4.5% / 0.3% = 15x increase, far exceeding linear.
- **Impact**: This is a factual error in the characterization of the paper's central result.
- **Severity**: Critical
- **Confidence**: High

---

## Major Issues

### L2: Section 3.4 conflates CV=20.5% and CV=27.4% data points

- **Location**: Section 3.4, around line 246
- **Problem**: The text discusses results at "moderate CV levels" but references data points from both CV=20.5% and CV=27.4% conditions without clearly distinguishing them. The claim about the full model having lower MSE is supported at one CV level but the magnitude cited comes from a different CV level.
- **Severity**: Major
- **Confidence**: High

### L3: MSE explanation at CV=0 is speculative

- **Location**: Section 3.4
- **Problem**: The paper observes that the full model achieves lower MSE than the reduced model even at CV=0 (where the reduced model is correctly specified) and offers an explanation involving "nonlinear functional of parameters." This explanation is plausible but entirely speculative — no theoretical argument or additional simulation is provided to support it.
- **Severity**: Major
- **Confidence**: High

---

## Minor Issues

| # | Issue | Location |
|---|-------|----------|
| L4 | "2.6" factor in Section 4.3 inconsistent with "2.5x" in conclusion | Lines 344 vs 482 |
| L5 | Chi-squared approximation validity not discussed for small n | Section 4.1 |
| L6 | Adaptive procedure Type I error not explicitly validated | Section 5.2 |
| L7 | "Well-designed system" definition is circular (parameters near baseline → baseline is well-designed) | Section 2.1 |

---

## Logical Chain Assessment

| Chain | Status |
|-------|--------|
| Common-shape assumption → MTTF bias | **Supported** by simulation evidence |
| Bias magnitude → practical consequence | **Supported** — MTTF metric is directly interpretable |
| LRT detects violations when they matter | **Supported** — alignment demonstrated empirically |
| Adaptive procedure improves over fixed choice | **Supported** but overhead magnitude needs correction |
| Censoring degrades detection | **Supported** by vary-q experiment |
| Masking degrades detection | **Supported** by vary-p experiment |

---

## Overall Assessment

**Logically sound with specific corrections needed.** The critical "sub-linear" characterization must be fixed — it's a factual error about the paper's own data. The major issues require either additional evidence or adjusted claims. The overall logical framework (consequence → detection → adaptive) is well-constructed and the main conclusions follow from the evidence.
