# Citation Verifier Report

**Reviewer role**: citation accuracy, missing references, bibliography integrity.
**Manuscript reviewed**: `qrei/manuscript.tex` and `qrei/refs.bib`.
**Date**: 2026-05-03

## Summary

The bibliography has 22 entries and the manuscript cites 13 of them. Nine entries are unused. There is one critical issue (stale ecosystem citations), one major issue (missing sibling paper), and several minor cleanups. The bibliography is structurally sound but tells a stale story about the author's own work.

**Severity counts**: critical 1, major 3, minor 4, suggestions 2.

## Critical Findings

### CRIT-C1: Foundation paper citation is stale
**Location**: 5 cite-points throughout the manuscript (Introduction, Section 2.2, Section 2.3, Section 2.4, Discussion).
**Quoted (current)**:
- Bib entry: `@Misc{towell2023reliability, ...url = {https://github.com/queelius/reliability-estimation-in-series-systems}}`
- Cite-points: e.g. line 51: "...detect the difference between models \citep{towell2023reliability}."

**Problem**: this citation points to the author's master's project (2023) on GitHub. The canonical reference for the C1-C2-C3 likelihood framework is the 2025 foundation paper:

> Towell, Alexander. "Masked Causes of Failure in Series Systems: A Likelihood Framework." 2025. DOI: 10.5281/zenodo.18725577.

**Verified**: `~/github/papers/masked-causes-in-series-systems/CITATION.cff` confirms the foundation paper exists with this DOI. The bibtex key in the ecosystem is `towell2025masked`. The foundation paper is preprint with Zenodo DOI; replacing the GitHub URL with a DOI substantially upgrades reviewer perception.

**Reviewer impact**: a reviewer who follows the link in `towell2023reliability` will land on a GitHub repo for a master's project. This is *not* a load-bearing reference for a journal paper. It implies (incorrectly) that the likelihood framework underlying this paper has not been peer-archived. The 2025 foundation paper has a Zenodo DOI which counts as archival.

**Fix**:
1. Replace the bib entry with:
```bibtex
@unpublished{towell2025masked,
  author = {Towell, Alexander},
  title  = {Masked Causes of Failure in Series Systems: {A} Likelihood Framework},
  year   = {2025},
  doi    = {10.5281/zenodo.18725577},
  note   = {Preprint}
}
```
2. Replace all `\citep{towell2023reliability}` with `\citep{towell2025masked}` (5 places).
3. In Section 2.2 (defining the likelihood), name the conditions: "...under conditions C1, C2, C3 of \citet{towell2025masked}."

This is the **single most consequential bibliography fix**. Cost: ~10 minutes. Benefit: substantial.

## Major Findings

### MAJ-C1: Sibling FIM paper is not cited
**Location**: Section 3.3 (the MSE Discussion paragraph), Section 4 (LRT formulation).
**Status**: not in bib at all.

**Problem**: the sibling Weibull-FIM paper (`~/github/papers/masked-series-companions/weibull-masked-fim/`) provides closed-form per-observation Fisher information for the homogeneous Weibull series, *exactly the reduced model studied here*. This is the asymptotic variance theory that backs the empirical bias-detectability claims. The omission orphans both papers.

**Specific places to cite**:
- Section 3.3 (MSE surprise discussion): the FIM paper has the closed-form variance of $\hat{k}$ for the reduced model. Citing it gives the variance amplification its theoretical justification.
- Section 4 introduction (LRT formulation): the FIM paper's masking-invariance result (the $I_{kk}$ block is unaffected by masking) is directly relevant to LRT power scaling.
- Section 5 (adaptive procedure): a sentence connecting the empirical alignment to the underlying FIM block structure provides theoretical grounding.

**Suggested bib entry** (consistent with FIM paper's own bib):
```bibtex
@unpublished{towell2025weibull-fim,
  author = {Towell, Alexander},
  title  = {Closed-Form {F}isher Information for Homogeneous {W}eibull Series Systems with Masked Failure Causes},
  year   = {2025},
  note   = {Preprint, draft v0.1.0}
}
```

**Cost**: ~15 minutes (add bib entry, 2-3 cite-points, optional half-paragraph in Section 3.3 connecting empirical MSE to closed-form FIM result).

### MAJ-C2: R package citation points to archived repo
**Location**: Section 2.4 (line 135), Data Availability statement (line 350).
**Quoted text**:
- Section 2.4: "...use the \texttt{wei.series.md.c1.c2.c3} R package \citep{towell2023weibull}..."
- Data Availability: "The R package used for all simulations is available at \url{https://github.com/queelius/wei.series.md.c1.c2.c3}."

**Problem**: per the project memory, `wei.series.md.c1.c2.c3` is **archived**. The live successor is `maskedcauses` (version 0.10.0) at `~/github/rlang/maskedcauses/` and on GitHub at `github.com/queelius/maskedcauses`.

**Reviewer impact**: a reviewer who tries to install the package will land on an archived repo. This makes the work appear unmaintained. If the simulation code itself was run with the old package, that is fine and should be stated; but the *forward-facing recommendation to readers* should point to the current package.

**Fix options**:
1. Keep `wei.series.md.c1.c2.c3` citation for the simulations (since that is what was actually used) and add a note: "Subsequent versions of this package are available as `maskedcauses` (\url{https://github.com/queelius/maskedcauses})." This is honest about what was used and forward-points readers to the maintained successor.
2. Update Data Availability statement to point to `maskedcauses` for current users.

Either is fine. The Data Availability statement is the more critical one to update.

### MAJ-C3: Multiple uncited references in bib that should be in Related Work
**Location**: Section 1.1 (Related Work, lines 53-57).
**Current text** (Related Work paragraphs, paraphrased): the section has two paragraphs. The first cites Usher-1988, Lin-1993, Joh-1989, Huairu-2013, and towell2023reliability. The second cites barlow1975 and Craiu-2005, then states that the model selection question (common shape versus heterogeneous shapes) has not, to the author's knowledge, been studied systematically for masked data, nor has the consequence of misspecification been quantified.

**Problem**: Related Work is two short paragraphs. The bib has 9 uncited entries, several of which are directly relevant prior art:
- `Amma-2001` (Sarhan 2001): masked system life data, exponential. Direct precedent.
- `Amma-2004` (Sarhan 2004): linear failure rate model with masked data.
- `Zhibi-2005`, `Zhibi-2007` (Tan): masked data estimation, exponential and binomial.
- `Lin-1996`: Bayesian masked-data estimation.
- `Usher-1996`: Weibull masked data specifically. **The most directly competitive prior work.**
- `burnham2002`, `lawless2003`, `meeker1998`: standard textbook references.

**Reviewer impact**: any reviewer who has worked on masked failure data will notice the missing references. The Sarhan and Tan papers in particular have hundreds of citations in this literature. Their absence in Related Work is a credibility issue.

**Fix**: extend Section 1.1 with one paragraph:
> "Beyond MLE, Bayesian approaches \citep{Lin-1996} and direct estimation methods \citep{Amma-2001, Amma-2004, Zhibi-2007} have been developed for masked component reliability. \citet{Usher-1996} considered Weibull-specific masked-data inference. None of this prior work systematically studied the common-shape constraint or its consequence for system-level prediction."

This pre-empts "what about the Sarhan / Tan / Usher 1996 papers?" reactions. ~15 minutes of writing.

## Minor Findings

### MIN-C1: Lin-1993 author order check
**Bib entry**: `@article{Lin-1993, author = {Lin, D.K.J. and Usher, J.S. and Guess, F.M.}, ...}`
**Verified**: this matches what the prior 2026-02-27 review identified as the *correct* author order for Lin et al. 1993 in IEEE Trans. Reliability vol 42 no 4. The previous error has been fixed.

### MIN-C2: Joh-1989 entry author names format
**Bib entry**: `@article{Joh-1989, author = {Guess, Frank M. and Usher, John S.}, ...}`
**Verified**: matches the 1989 Quality and Reliability Engineering International paper. Author names are spelled out. Style is consistent with other entries.

### MIN-C3: "Joh-1989" is an unintuitive bib key
The key `Joh-1989` (presumably standing for "John") is non-mnemonic. Standard practice would be `guess1989` or `GuessUsher1989`. Not a publication blocker but a minor cleanup. The 2026-02-27 review noted the same issue.

### MIN-C4: Page-range hyphens vs en-dashes
Some bib entries use single hyphens for page ranges (`pages = {550--555}` is correct double-hyphen for LaTeX; `pages = {550-555}` would be a single-hyphen error). I scanned the bib and all page ranges use the LaTeX-correct double-hyphen `--`. Good.

## Suggestions

### SUG-C1: Archive the foundation paper Zenodo DOI in CrossRef
The foundation paper has a Zenodo DOI but is not in CrossRef (Zenodo DOIs are DataCite-registered, not CrossRef). For maximum reviewer reachability, consider also depositing on arXiv (stat.ME). This is outside the scope of this paper but worth noting for the foundation paper itself.

### SUG-C2: Add 2-3 conceptual citations
Even without expanding the literature review substantially, three citations would professionalize the framing:
1. Claeskens and Hjort (2003) *Focused Information Criterion*. The conceptual ancestor of "consequence-focused model selection."
2. Pareek, Kundu, Kumar (2009) "Estimation in Weibull competing risks model." Direct comparator.
3. Pascual (2005) *J. Quality Technology*, "Model selection for Weibull and lognormal." Precedent for "consequence of misspecification" framing.

These are not blockers but would strengthen the literature positioning, especially for IEEE TR or Technometrics.

## Bibliography Integrity Check

| Aspect | Status |
|--------|--------|
| All cited keys exist in bib | yes (verified, no broken \cite) |
| All bib keys cited | no (9 unused; recommend cull or use, see MAJ-C3) |
| Page ranges use `--` | yes |
| Author names consistent format | mostly yes (some abbreviations vary) |
| DOIs included where available | mostly yes |
| Years correct | yes (foundation paper exception, see CRIT-C1) |
| URLs work | not verified for external papers; the two Towell self-citation URLs are stale (see CRIT-C1, MAJ-C2) |

## Verdict

The most pressing fix is CRIT-C1 (replace `towell2023reliability` with `towell2025masked`). Together with MAJ-C1 (add sibling FIM paper) and MAJ-C2 (clarify R package status), these are roughly 30 minutes of work that materially upgrade the paper's reviewer-facing apparatus. MAJ-C3 (extend Related Work with uncited refs) is another 15 minutes for substantial credibility gain.

Confidence: high.
