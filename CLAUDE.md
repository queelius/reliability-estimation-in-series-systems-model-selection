# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research project on **model selection for reliability estimation in series systems** with Weibull-distributed component lifetimes. The project uses simulation studies to assess the sensitivity of maximum likelihood estimators (MLEs) to deviations from well-designed systems and evaluates the appropriateness of a reduced homogeneous-shape model using likelihood ratio tests.

The primary deliverable is a research paper authored in LaTeX with figures generated from R and Python simulation scripts.

## Project Structure

```
.
├── paper/                  # LaTeX source and figures
│   ├── paper.tex          # Main manuscript
│   ├── refs.bib           # Bibliography
│   ├── ieee-with-url.csl  # Citation style
│   └── image/             # Figures (PDF)
├── results/               # Simulation code and data
│   ├── 5_system_scale3/   # Scale parameter sensitivity
│   ├── 5_system_shape3/   # Shape parameter sensitivity
│   ├── lrt/               # Likelihood ratio test simulations
│   └── ...
├── docs/                  # GitHub Pages site
│   ├── index.md           # Site homepage
│   ├── _config.yml        # Jekyll config
│   └── paper.pdf          # Published PDF (tracked)
└── README.md              # Project overview
```

## Dependencies

### LaTeX
Standard LaTeX distribution with packages:
- `amsmath`, `amsthm`, `amssymb` - Mathematical typesetting
- `graphicx` - Figure inclusion
- `hyperref`, `url` - Hyperlinks and URLs
- `natbib` - Bibliography management
- `tikz` - Graphics

### R Packages
The simulation code relies on several custom R packages:
- `algebraic.mle` - Maximum likelihood estimation utilities
- `algebraic.dist` - Algebraic distribution functions
- `md.tools` - Masked data tools
- `wei.series.md.c1.c2.c3` - Weibull series system with masked data support

Standard packages: `tidyverse`, `ggplot2`, `boot`, `parallel`

### Python
Python scripts use: `matplotlib`, `seaborn`, `pandas`, `numpy`

## Building the Paper

```bash
cd paper
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

Or use latexmk:
```bash
cd paper
latexmk -pdf paper.tex
```

After building, copy to docs/ for GitHub Pages:
```bash
cp paper/paper.pdf docs/
```

## Data Pipeline Architecture

Simulation data flows: **R script → CSV → Python analysis script → PDF figures → paper**

1. R scripts in `results/[experiment]/` run Monte Carlo simulations, appending rows to a CSV file (e.g., `data-lrt-divergence.csv`)
2. Python scripts in `results/[experiment]/figure/` read the CSV, compute summary statistics (rejection rates, CIs), and produce publication-quality PDF figures
3. Python scripts save figures to both the local `figure/` dir and directly to `paper/image/` (or subdirectories `paper/image/fig-lrt/`, `paper/image/fig/`)

## Simulation Code Organization

- `results/5_system_scale3/` - Scale parameter sensitivity (bootstrap CIs)
- `results/5_system_shape3/` - Shape parameter sensitivity (bootstrap CIs)
- `results/lrt/` - Likelihood ratio test simulations:
  - `divergence/` - Type I error and power vs shape CV
  - `vary_m/` - Effect of number of components (m = 2–8)
  - `vary_p/` - Effect of masking probability (p = 0.05–0.70)
  - `vary_q/` - Effect of censoring level (q = 0.50–1.00)
  - `nomasking/` - Ideal case baseline (p=0, q=1)
  - `reduced1/`, `reduced2/`, `reduced3/` - Individual component reduction tests

### Baseline 5-Component System

All simulations share this well-designed baseline (shape CV ≈ 4%):

| Component | Shape (k) | Scale (λ) | MTTF |
|-----------|-----------|-----------|------|
| 1 | 1.2576 | 994.37 | ~913 |
| 2 | 1.1635 | 908.95 | ~857 |
| 3 | 1.1308 | 840.11 | ~799 |
| 4 | 1.1802 | 940.13 | ~881 |
| 5 | 1.2034 | 923.16 | ~863 |

Default experimental conditions: masking p=0.215, censoring quantile q=0.825, 500 replications per condition.

### LRT Implementation Pattern

R scripts fit both models per replication:
- **Full model**: `mle_lbfgsb_wei_series_md_c1_c2.c3()` with L-BFGS-B, `parscale = theta`, `max_iter = 1000`
- **Reduced model**: `optim()` with `fnscale = -1` (maximize log-likelihood), common shape across all components
- **Test statistic**: `Lambda = -2 * (loglik_R - loglik_F)`, compared to χ²(m-1)
- Non-convergent fits are silently skipped via `tryCatch()` — only successful results are appended

### Python Analysis Pattern

Scripts in `figure/` subdirectories:
- Read parent CSV, group by experimental factors, compute rejection rates with binomial standard errors
- Validate Type I error control at CV=0 (should ≈ α=0.05)
- Save summary CSVs alongside figure PDFs
- Some scripts also print LaTeX table code to stdout

## Key Concepts

### Well-Designed Series System
A 5-component series system where all components have similar failure characteristics:
- All shape parameters near 1.1-1.3 (slightly increasing hazard)
- All scale parameters around 900-1000
- No single weak component dominates system failure

### Full vs Reduced Models
- **Full Model**: Each component has its own shape and scale (2m parameters)
- **Reduced Model**: All components share a common shape (m+1 parameters)

### Masked Data
- Only system-level failure times observed
- Candidate set C_i indicates which components might have caused failure
- Right-censoring when observation period ends before failure

## Common Tasks

### Regenerate Figures
```bash
# 1. Run R simulation (long-running, produces CSV)
cd results/lrt/divergence
Rscript lrt-divergence.R

# 2. Run Python analysis (reads CSV, produces PDFs)
cd results/lrt/divergence/figure
python3 analyze_divergence.py

# 3. Rebuild paper
cd paper && latexmk -pdf paper.tex
```

### Update GitHub Pages
```bash
cd paper && latexmk -pdf paper.tex
cp paper/paper.pdf docs/
```

### Update Citations
- Edit `paper/refs.bib` (BibTeX format)
- Uses IEEEtranN bibliography style with `natbib` (`[numbers]` style)

### Custom LaTeX Commands
- `\v{x}` renders as `\boldsymbol{x}` (for vectors)
