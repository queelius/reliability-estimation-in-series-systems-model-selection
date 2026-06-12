# Format Validator Report

**Date**: 2026-02-27
**Paper**: "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"

## Build Verification

- **Build status**: Manuscript builds cleanly with `latexmk -pdf`
- **LaTeX warnings**: Only one standard package info message (infwarerr); no undefined references, no missing figures
- **Page count**: 10 pages (including references)
- **Figure count**: 3 figures (consequence_focused, adaptive_selection, lrt_vs_aic_bic_divergence)
- **Table count**: 5 tables

## Label Resolution

All labels resolve correctly:
- `\ref{fig:alignment}` -> Figure 1
- `\ref{fig:adaptive}` -> Figure 2
- `\ref{fig:lrt-vs-aic-bic}` -> Figure 3
- `\ref{tab:series-sys}` -> Table 1
- `\ref{tab:consequence}` -> Table 2
- `\ref{tab:power-by-cv}` -> Table 3
- `\ref{tab:adaptive}` -> Table 4
- `\ref{tab:data-quality}` -> Table 5
- `\ref{sec:framework}`, `\ref{sec:baseline}`, etc. -- all resolve
- `\ref{app:data-quality}` -> Appendix A
- `\ref{app:aic-bic}` -> Appendix B

## QREI Formatting Assessment

### Current Format
- **Document class**: `article` with 11pt font, 1-inch margins
- **Bibliography**: IEEEtranN style with natbib (numbers)
- **No QREI-specific formatting** applied

### QREI Requirements (Quality and Reliability Engineering International, Wiley)
1. **Author guidelines**: QREI uses the standard Wiley LaTeX template
2. **Citation style**: Author-date (not numbered) -- **the current numbered citation style is incorrect for QREI**
3. **Page limit**: No strict page limit but typical papers are 15-20 pages in the journal's format
4. **Required sections**: Data Availability Statement, Conflict of Interest -- **both present, good**
5. **Keywords**: Present -- **good**
6. **ORCID**: Present -- **good**
7. **Abstract**: Should be under 250 words -- current abstract is ~130 words, fine

### Required Changes for QREI Submission

#### Critical
1. **Citation style must change** from numbered [1] to author-date (Barlow and Proschan, 1975). QREI follows the standard Wiley author-date format
2. **Document class/template**: Should use the Wiley LaTeX template (wiley-article class or similar)

#### Major
3. **Running heads**: QREI requires short running title and author surname
4. **Correspondence author**: Should be designated explicitly
5. **Word count**: Should be provided

#### Minor
6. **Figure quality**: Figures are PDF vector graphics -- good
7. **Table style**: Currently uses `\hline` throughout. Wiley style prefers `booktabs` (with `\toprule`, `\midrule`, `\bottomrule`)
8. **Hyperlink colors**: Current blue links should be removed for print submission

## Manuscript Structure

### Current Structure
1. Introduction (1 page)
   - 1.1 Related Work
   - 1.2 Contributions
2. Model Framework (2 pages)
3. Consequence Analysis (2 pages)
4. Likelihood Ratio Testing (1 page)
5. Adaptive Model Selection (2 pages)
6. Conclusion (1 page)
A. Data Quality Effects (0.5 page)
B. Information Criteria Comparison (0.5 page)

### Assessment
- The structure is clean and logical
- At 10 pages with generous margins, this is a compact paper
- The appendices are very brief and could be integrated into the main text without exceeding typical QREI length

## Cover Letter

A cover letter is present (cover-letter.tex). It:
- Addresses the QREI editor
- Summarizes the paper's contribution
- States no prior publication or submission elsewhere
- Declares no conflicts of interest
- Is professional and appropriately brief

## File Inventory

### Present and Correct
- `manuscript.tex` -- main source
- `refs.bib` -- bibliography
- `image/` -- 12 PDF figures (3 used in manuscript, others available)
- `cover-letter.tex` and `cover-letter.pdf`
- `Makefile` -- build automation
- `README.md` -- submission notes

### Build Artifacts (should be excluded from submission)
- `manuscript.aux`, `.bbl`, `.blg`, `.fdb_latexmk`, `.fls`, `.log`, `.out`
- `cover-letter.aux`, `.fdb_latexmk`, `.fls`, `.log`, `.out`

## Summary

The manuscript builds cleanly and resolves all references. The primary formatting gap is that it uses a generic article class with numbered citations rather than the QREI/Wiley template with author-date citations. This will need to be addressed before submission. The cover letter and required QREI sections (data availability, conflict of interest, keywords, ORCID) are all present.
