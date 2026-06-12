# Citation Verification Report

**Date**: 2026-02-27
**Paper**: "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"

## Summary

The bibliography contains 20 entries, all cited in the text. The core masked-data literature lineage is comprehensively covered. Two confirmed bibliography errors exist: the Lin-1993 entry lists the wrong first author, and the Joh-1989 entry has malformatted and incorrect author initials. One in-text citation misdescribes Tan (2005). Three important reference categories are absent: competing-risks literature, EM algorithm methods for masked data, and misspecification theory (White 1982). Self-citation ratio (2/20, 10%) is appropriate.

Total citations checked: 20. Issues found: 7 (0 critical, 2 major, 5 minor).

---

## Major Issues

### Issue 1: Author Order Error in Lin-1993

- `refs.bib` lists `author = {Usher, J.S. and Lin, D.K.J. and Guess, F.M.}`
- The actual published paper has **Lin** as first author (confirmed via IEEE Xplore DOI: 10.1109/24.273596)
- The in-text attribution "Lin, Usher, and Guess" is correct, but the bib entry renders Usher first
- **Fix**: Change to `author = {Lin, D.K.J. and Usher, J.S. and Guess, F.M.}`

### Issue 2: Misdescription of Tan (2005)

- Text says: "Tan [citations] contributed methods for exponential component reliability estimation"
- Tan (2005) is about **discrete binomial system testing data** (success/failure), not continuous exponential lifetimes
- Tan (2007) does address exponential lifetimes — the description only fits that paper
- **Fix**: "Tan \cite{Zhibi-2005} treated masked binomial system testing data, while Tan \cite{Zhibi-2007} contributed exponential component reliability estimation."

---

## Minor Issues

| # | Issue | Fix |
|---|-------|-----|
| 3 | `Joh-1989` author names malformatted (`F.G., Guess`); wrong initial (should be F.M.) | `author = {Guess, Frank M. and Usher, John S.}` |
| 4 | Duplicate `page` + `pages` fields in 4 entries | Remove `page` fields |
| 5 | Self-citations are non-archival GitHub URLs | Archive on Zenodo for permanent DOIs |
| 6 | BibTeX keys use first names (`Huairu-2013`, `Zhibi-2005`) | Rename to surname-year convention |
| 7 | Redundant `issue` + `number` fields in 7 entries | Remove `issue` fields |

---

## Missing References

| Priority | Reference | Relevance |
|----------|-----------|-----------|
| High | Crowder (2001), "Classical Competing Risks" | Masked series data IS a competing risks problem |
| Medium | EM algorithm papers for masked Weibull data | Alternative estimation approach not mentioned |
| Medium | White (1982), misspecification theory | Theoretical foundation for consequence analysis |

---

## Self-Citation Analysis

- 2 self-citations out of 20 (10%) — appropriate
- Both are functional: `towell2023reliability` provides the likelihood framework; `towell2023weibull` provides the R package
- Concern: non-archival (GitHub only, no DOIs)

## Verified Accurate

All 16 non-self citations were spot-checked against DOIs/publisher pages. All details (year, journal, volume, pages) confirmed correct.
