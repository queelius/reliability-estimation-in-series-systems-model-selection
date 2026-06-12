# Format Validator Report

**Date**: 2026-02-25
**Paper**: "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"

## Summary

The paper builds cleanly with zero warnings/errors. All figures resolve. All cross-references resolve. The document is 19 pages using standard LaTeX article class with 1-inch margins. No target venue is specified.

## Build Verification

- **Build command**: `latexmk -pdf paper.tex` -- SUCCESS
- **Output**: `paper.pdf` (784,111 bytes, 19 pages)
- **Warnings**: 0
- **Errors**: 0

## Findings

### MINOR: 8 labels defined but never referenced

- **Location**: `paper.tex`
- **Labels**: `app:ideal-case`, `app:sensitivity`, `eq:loglik`, `eq:sys_hazard`, `eq:sys_reliability`, `fig:lrt-vs-aic-bic`, `sec:baseline`, `tab:model-hierarchy`
- **Problem**: These labels are defined but never `\ref{}`ed in the text. Notable: `tab:model-hierarchy` (Table 1) and `fig:lrt-vs-aic-bic` (Figure 7) are never cross-referenced, meaning readers are not directed to them. The appendix sections (`app:sensitivity`, `app:ideal-case`) are also not cross-referenced from the main text.
- **Severity**: Minor
- **Suggestion**: Add cross-references or remove unused labels. Tables and figures should always be referenced in the body text. The appendices should be referenced at least once (e.g., "Appendix A provides additional sensitivity analysis").

### MINOR: Figure placement may cause page breaks

- **Location**: All figures use `[htbp]` placement
- **Problem**: With 10 figures and 7 tables in 19 pages, the placement algorithm may push content across page boundaries unpredictably. The `[htbp]` specifier is appropriate but some figures (especially the full-page ones like Figure 5 at 0.85\textwidth) may benefit from explicit placement.
- **Severity**: Minor
- **Suggestion**: Review the compiled PDF for any awkward page breaks. Consider `[t]` or `[p]` for large figures.

### MINOR: No document class appropriate for target venue

- **Location**: Line 1: `\documentclass[11pt]{article}`
- **Problem**: The paper uses the generic `article` class. If targeting a specific venue (IEEE, Springer, etc.), the appropriate document class should be used. The state file indicates no target venue.
- **Severity**: Minor (appropriate for preprint)
- **Suggestion**: When a venue is selected, switch to the venue-specific document class.

### SUGGESTION: Consider adding line numbers for review

- **Problem**: Line numbers are helpful for reviewers to reference specific locations.
- **Suggestion**: Add `\usepackage{lineno}` and `\linenumbers` during review stage.

### SUGGESTION: Consider hyperref configuration

- **Problem**: `hyperref` is loaded but not configured. Default colored link boxes may appear in the PDF.
- **Suggestion**: Add configuration for clean PDF output: `\hypersetup{colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}`

## Graphics Verification

All 10 included graphics files exist:
1. `image/consequence_analysis.pdf` -- OK
2. `image/lrt_divergence_analysis.pdf` -- OK
3. `image/lrt_vary_p_rejection_rate.pdf` -- OK
4. `image/lrt_vary_q_rejection_rate.pdf` -- OK
5. `image/lrt_vary_m_rejection_rate.pdf` -- OK
6. `image/lrt_vs_aic_bic_divergence.pdf` -- OK
7. `image/adaptive_selection.pdf` -- OK
8. `image/5_system_mttf3_by_scale3.pdf` -- OK
9. `image/5_system_shape3_fig.pdf` -- OK
10. `image/ideal_case_n100_p0_q1.pdf` -- OK

## Cross-Reference Integrity

- Labels defined: 29
- Labels referenced: 21
- Orphan references (ref to undefined label): 0
- All references resolve correctly: PASS

## Confidence: HIGH
