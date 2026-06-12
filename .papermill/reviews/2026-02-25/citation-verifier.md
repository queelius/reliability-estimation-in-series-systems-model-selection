# Citation Verifier Report

**Date**: 2026-02-25
**Paper**: "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"

## Summary

The bibliography has 24 entries. 20 are cited in the text; 4 are unused. All cited keys resolve correctly. Citation formatting is consistent (IEEEtranN + natbib numeric style). Several entries have minor formatting issues.

## Findings

### MINOR: Four bibliography entries are never cited

- **Location**: `paper/refs.bib`
- **Entries**:
  1. `efron1987better` (Efron, "Better Bootstrap Confidence Intervals") -- relevant to Appendix A bootstrap CIs but not cited
  2. `nelson1982` (Nelson, "Applied Life Data Analysis") -- a standard reference
  3. `towell2023algebraic-mle` (Algebraic MLE R package) -- used in the code but not cited in paper
  4. `Fran-1991` (Guess, Hodgson, Usher, "Estimating system and component reliabilities") -- related work
- **Severity**: Minor
- **Suggestion**: Either cite these where relevant or remove from the bibliography. The `efron1987better` reference should be cited if bootstrap CIs are mentioned in Appendix A. The `towell2023algebraic-mle` package should be cited since it is used in the simulations.

### MINOR: Author formatting in Joh-1989

- **Location**: `paper/refs.bib` entry `Joh-1989`
- **Problem**: Authors listed as `F.G., Guess and J.S., Usher` -- initials and surnames are reversed. Should be `Guess, Frank M. and Usher, John S.` to match the journal article format.
- **Severity**: Minor (may cause incorrect rendering)
- **Suggestion**: Fix to `author = {Guess, Frank M. and Usher, John S.}`

### MINOR: Self-citations as non-archival sources

- **Location**: `refs.bib` entries `towell2023reliability`, `towell2023weibull`, `towell2023algebraic-mle`
- **Problem**: Three entries reference the author's own GitHub repositories as `@Misc` and `@Manual`. These are not peer-reviewed, archived publications. The foundation paper (`towell2023reliability`) is cited 3 times and is central to the paper's methodology. If this paper has been published or submitted, the citation should be updated.
- **Severity**: Minor (but affects credibility for formal submission)
- **Suggestion**: If the foundation paper has been submitted or published, update the citation. If not, acknowledge it as a preprint/technical report. Consider archiving on arXiv or Zenodo for permanent DOIs.

### MINOR: Inconsistent use of `page` vs `pages` fields

- **Location**: Multiple bib entries (e.g., `Amma-2001` has both `page` and `pages` fields)
- **Problem**: Several entries have redundant `page` and `pages` fields. BibTeX uses `pages`; the `page` field is non-standard and ignored.
- **Severity**: Minor (cosmetic, no effect on output)
- **Suggestion**: Remove `page` fields; keep only `pages`.

### SUGGESTION: Missing references that could strengthen the paper

1. **White (1982)**: "Maximum Likelihood Estimation of Misspecified Models" -- foundational for understanding MLE behavior under misspecification
2. **Vuong (1989)**: "Likelihood Ratio Tests for Model Selection" -- relevant to the LRT methodology
3. **Ibrahim, Chen, Sinha (2001)**: "Bayesian Survival Analysis" -- relevant as an alternative modeling paradigm
4. **Crowder (2001)**: "Classical Competing Risks" -- the masked series system is a competing risks problem

## Bibliography Integrity

- All 20 cited keys resolve to valid entries: PASS
- No undefined references in compiled PDF: PASS
- Citation style consistent (numeric, IEEEtranN): PASS
- 4 unused entries: WARN
- 1 malformatted author entry: WARN

## Confidence: HIGH
