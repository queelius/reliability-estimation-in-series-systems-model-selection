# QREI Submission Directory Design

**Date:** 2026-02-26
**Venue:** Quality and Reliability Engineering International (Wiley)
**Portal:** https://wiley.atyponrex.com/journal/QRE

## Directory Structure

```
qrei/
├── README.md                    # Submission checklist + portal URL
├── cover-letter.tex             # Compilable cover letter
├── cover-letter.pdf             # Compiled cover letter
├── manuscript.tex               # paper.tex + keywords + DAS + COI
├── manuscript.pdf               # Compiled PDF for peer review
├── refs.bib                     # Copy of bibliography
├── image/                       # All 10 figure PDFs (unchanged names)
│   ├── consequence_analysis.pdf
│   ├── lrt_divergence_analysis.pdf
│   ├── lrt_vary_p_rejection_rate.pdf
│   ├── lrt_vary_q_rejection_rate.pdf
│   ├── lrt_vary_m_rejection_rate.pdf
│   ├── lrt_vs_aic_bic_divergence.pdf
│   ├── adaptive_selection.pdf
│   ├── 5_system_mttf3_by_scale3.pdf
│   ├── 5_system_shape3_fig.pdf
│   └── ideal_case_n100_p0_q1.pdf
└── Makefile                     # Build manuscript + cover letter
```

## Manuscript Adaptations (vs paper.tex)

1. **Keywords**: Add 5 keywords after abstract — Weibull distribution, series systems, masked failure data, model selection, likelihood ratio test
2. **Data Availability Statement**: Before references — simulation code available on GitHub
3. **Conflict of Interest**: Declaration of no COI
4. **ORCID**: Add to author block (0000-0001-6443-9897)
5. No structural or content changes

## Cover Letter

- Addressed to Editor-in-Chief
- 3 paragraphs: what the paper does, why it fits QREI, key findings
- Mentions no COI, single author, ORCID

## README Checklist

- Pre-submission verification items (build, word count, figure count)
- Portal URL and login instructions
- File upload mapping (which file designation for each file)

## Implementation Steps

1. Create `qrei/` directory
2. Copy `paper.tex` → `qrei/manuscript.tex` and add keywords, DAS, COI, ORCID
3. Copy `refs.bib` → `qrei/refs.bib`
4. Copy all 10 figure PDFs into `qrei/image/`
5. Create `qrei/Makefile` to build manuscript.pdf and cover-letter.pdf
6. Create `qrei/cover-letter.tex`
7. Build both PDFs
8. Create `qrei/README.md` with submission checklist
9. Verify: clean build, abstract ≤ 230 words, all figures present
