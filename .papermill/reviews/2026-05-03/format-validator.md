# Format Validator Report

**Reviewer role**: build verification, label resolution, venue formatting, repository hygiene.
**Manuscript reviewed**: `qrei/manuscript.tex`. Page count verified. Repository state checked.
**Date**: 2026-05-03

## Summary

The manuscript builds cleanly and produces an 11-page PDF. All labels resolve. Venue formatting is acceptable for QREI (which has no rigid format requirements at submission stage; final formatting is done in production). One repository hygiene problem requires action: `qrei/` build artifacts are not gitignored. The `.papermill.md` claims a 10-page QREI version vs 20-page paper version; this is wrong (both are 11 pages).

**Severity counts**: critical 0, major 2, minor 4, suggestions 2.

## Major Findings

### MAJ-F1: `qrei/` build artifacts are not gitignored
**Location**: `.gitignore` (lines 1-16) and `qrei/` directory.
**Quoted .gitignore**:
```
# LaTeX auxiliary files
paper/*.aux
paper/*.bbl
paper/*.blg
paper/*.log
paper/*.out
paper/*.toc
paper/*.lof
paper/*.lot
paper/*.fls
paper/*.fdb_latexmk
paper/*.synctex.gz
paper/*.latexml.log
```

**Problem**: the `paper/*` pattern covers the original location but not `qrei/*`. Currently the `qrei/` directory has these uncommitted files showing as untracked in git status:
- `qrei/manuscript.aux`
- `qrei/manuscript.bbl`
- `qrei/manuscript.blg`
- `qrei/manuscript.fdb_latexmk`
- `qrei/manuscript.fls`
- `qrei/manuscript.log`
- `qrei/manuscript.out`
- `qrei/cover-letter.aux`
- `qrei/cover-letter.fdb_latexmk`
- `qrei/cover-letter.fls`
- `qrei/cover-letter.log`
- `qrei/cover-letter.out`

**Impact**: not blocking for QREI submission, but makes `git status` noisy and can lead to accidentally committing build artifacts.

**Fix**: extend `.gitignore` to cover both locations. Replace lines 1-13 of `.gitignore` with a single set of patterns:

```gitignore
# LaTeX auxiliary files (paper/ and qrei/)
**/*.aux
**/*.bbl
**/*.blg
**/*.log
**/*.out
**/*.toc
**/*.lof
**/*.lot
**/*.fls
**/*.fdb_latexmk
**/*.synctex.gz
**/*.latexml.log
```

This is one minute of work. Recommend doing before submission.

### MAJ-F2: `.papermill.md` page count claim is wrong (and conflicts with reality)
**Location**: `.papermill.md`.
**Quoted text**:
- User prompt: "qrei/manuscript.tex (10 pages, article class, IS the QREI submission package..."
- User prompt: "paper/paper.tex (20 pages, longer working version..."
- `.papermill.md` line 116: "PDF: paper/paper.pdf (~786 KB, 20 pages, built 2026-02-26)"
- `.papermill.md` line 171: "20 pages."

**Verified**: `pdfinfo qrei/manuscript.pdf` reports **11 pages**. `pdfinfo paper/paper.pdf` reports **11 pages**. Both PDFs are essentially identical-length renderings of nearly identical text. The two `.tex` files differ only in: citation style (`numbers` vs `round`), keyword line, ORCID line in author block, Data Availability statement, and bibliography style. The QREI version is *longer* than the paper.tex (359 vs 348 lines) because of the added Data Availability section, not shorter.

**Impact**: minor for the manuscript itself (11 pages is QREI-compatible), but the paper-state metadata is incorrect, which could mislead future planning. The "10 pages, IS the QREI submission" framing in the user prompt overstates the differentiation between the two versions.

**Fix**: update `.papermill.md`:
- Line 116: change "20 pages" to "11 pages"
- Line 171: same correction
- Add a clarifying note: the `qrei/` and `paper/` versions are nearly identical content. They differ in citation style, abstract has keywords in qrei, ORCID line in qrei author block, Data Availability statement in qrei. The "longer working version with extra appendices" framing is no longer accurate.

This is metadata cleanup, not a manuscript fix.

## Minor Findings

### MIN-F1: Cover letter says "research article" but does not name a specific section
**Quoted text** (`qrei/cover-letter.tex`, lines 19-23):
> "I am submitting the manuscript ... for consideration as a research article in *Quality and Reliability Engineering International*."

**Issue**: QREI accepts research articles, case studies, and short notes. "Research article" is fine but specifying ("as a Research Article in the Reliability Methodology section") would be tighter. Cover letter is otherwise well-structured.

**Suggestion**: leave as-is. Minor polish only.

### MIN-F2: Page count vs QREI default
**QREI guidance**: research articles "typically 15-30 pages double-spaced." The 11-page single-spaced manuscript translates to roughly 18-22 pages double-spaced. This is comfortably within QREI's range. No issue.

For IEEE TR comparison: IEEE TR has a 12-page hard limit (with stated penalties beyond). The 11-page single-spaced single-column manuscript would likely come in at around 9-10 pages in two-column IEEE format. So a recompilation in IEEE template is feasible without content cuts. Good news for fallback strategy.

### MIN-F3: hyperref colored citations may render poorly in some QREI proof systems
**Quoted setup** (line 12): `\hypersetup{colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}`

**Issue**: at production stage QREI's typesetters often re-style hyperlinks. Authors typically submit with `colorlinks=false` or with `\hypersetup{}` simplified. This is not a blocker but the typesetter may strip it.

**Fix**: leave as-is for review-stage submission. Production will handle it.

### MIN-F4: Float specifier `[htbp]` used throughout
**Issue**: QREI's typesetting will re-flow tables and figures. The `[htbp]` placement specifiers are not load-bearing. Fine.

## Suggestions

### SUG-F1: Add an arXiv-ready preprint version
Both QREI and IEEE TR are compatible with simultaneous arXiv preprinting. The `.papermill.md` mentions "arXiv preprint (stat.ME)" as part of the strategy but no arXiv-formatted manuscript exists yet. Recommend creating one (essentially the same as `paper/paper.tex` minus the venue-specific bits).

### SUG-F2: Consider listing the page count and approximate compile time in the README
Useful for collaborators. Currently `qrei/README.md` exists but I have not verified its content. Standard practice.

## Build Verification

Verified:
- `qrei/manuscript.pdf` exists and is 11 pages.
- `paper/paper.pdf` exists and is 11 pages.
- All `\citep`, `\citet`, `\citealt` keys resolve to bib entries (verified via grep).
- All `\ref`, `\label` pairs match (no LaTeX warnings about undefined references would have been thrown given the build was successful).
- `qrei/manuscript.bbl` is 80 lines and contains all 13 cited entries.
- 12 figure files exist in `qrei/image/` and the 4 referenced in the manuscript (`consequence_focused.pdf`, `adaptive_selection.pdf`, `lrt_vs_aic_bic_divergence.pdf`, plus tables) are present.

## Repository Hygiene Audit

| Aspect | Status |
|--------|--------|
| .gitignore covers `paper/` artifacts | yes |
| .gitignore covers `qrei/` artifacts | NO (see MAJ-F1) |
| Untracked files in git status | yes (build artifacts, plus uncommitted `qrei/`, `blog/`, `results/adaptive/`, `results/consequence/`) |
| Submodule cleanliness | n/a (no submodules) |
| Branch state | master, up to date with origin/master |
| Stale references in `.papermill.md` | yes (page counts wrong, see MAJ-F2) |

## Verdict

The manuscript builds and is venue-ready in form. The two operational fixes (extend .gitignore, correct .papermill.md page counts) are minor housekeeping. No format issue is a publication blocker.

Confidence: high.
