# Format Validation Report

**Date**: 2026-02-27

## Summary

The paper **builds successfully** with `latexmk -pdf paper.tex`. Output: 20 pages, 787,603 bytes. Final pdflatex pass is completely clean — zero errors, zero warnings. All 10 figures found as PDF vector graphics. All 20 citation keys resolve. All cross-references resolve (no "??"). Production-ready as preprint.

## Build Status: SUCCESS

## Issues (all minor)

### BibTeX Quality (4 issues)
1. Inverted author names in `Joh-1989` — Fix: `author = {Guess, F.M. and Usher, J.S.}`
2. `Huairu-2013` uses `@article` for conference paper — Fix: `@inproceedings`
3. Non-standard `issue` field in 7 entries — Fix: use `number`
4. Duplicate `page` + `pages` fields in 4 entries — Fix: remove `page`

### Cross-References (2 issues)
5. 4 labels defined but never referenced: `eq:sys_reliability`, `eq:sys_hazard`, `eq:loglik`, `sec:baseline`
6. Density row in `align` block gets equation number but no label — add `\nonumber`

### Formatting (3 issues)
7. `hyperref` without `\hypersetup{}` — default colored link boxes
8. `tikz` and `subcaption` packages loaded but unused
9. 20 pages may exceed IEEE Transactions limits (appendix ~5 pages → supplementary)

## All Figures Found (10/10)
All PDF vector graphics embedded without error.
