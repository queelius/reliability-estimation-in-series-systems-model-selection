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

## Simulation Code Organization

The `results/` directory contains simulation experiments organized by scenario:

- `results/5_system_scale3/` - Simulations varying scale parameter of component 3
- `results/5_system_shape3/` - Simulations varying shape parameter of component 3
- `results/lrt/` - Likelihood ratio test simulations
  - `divergence/` - Type I error and power analysis
  - `vary_m/` - Effect of number of components
  - `vary_p/` - Effect of masking probability
  - `vary_q/` - Effect of censoring level

### Simulation Script Pattern
```r
library(tidyverse)
library(parallel)
library(boot)
library(wei.series.md.c1.c2.c3)

theta <- c(shape1 = 1.2576, scale1 = 994.3661, ...)
N <- c(100)        # Sample sizes
P <- c(0.215)      # Masking probability
Q <- c(0.825)      # Censoring quantile
B <- 1000          # Bootstrap replicates
```

### Visualization Pattern
Python scripts in `figure/` subdirectories:
- Read CSV data from parent directory
- Use matplotlib/seaborn for plotting
- Generate PDF figures for `paper/image/`

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
1. Run the relevant R simulation script in `results/[scenario]/`
2. Run corresponding Python plotting script in `results/[scenario]/figure/`
3. Figures are saved as PDFs in `paper/image/`
4. Rebuild the paper from `paper/` directory

### Update GitHub Pages
1. Rebuild paper: `cd paper && latexmk -pdf paper.tex`
2. Copy PDF: `cp paper/paper.pdf docs/`
3. Commit and push

### Update Citations
- Edit `paper/refs.bib` (BibTeX format)
- Uses IEEEtranN bibliography style

## Important Files
- `paper/paper.tex` - Main LaTeX document
- `paper/refs.bib` - Bibliography database
- `paper/image/` - All figure PDFs
- `docs/` - GitHub Pages site with published PDF
- `results/` - Simulation code and data
