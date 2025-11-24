# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research project on **model selection for reliability estimation in series systems** with Weibull-distributed component lifetimes. The project uses simulation studies to assess the sensitivity of maximum likelihood estimators (MLEs) to deviations from well-designed systems and evaluates the appropriateness of a reduced homogeneous-shape model using likelihood ratio tests.

The primary deliverable is a research paper authored in LaTeX (`paper.tex`) with figures generated from R and Python simulation scripts.

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

The paper is compiled using standard LaTeX toolchain:

```bash
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

Or use a Makefile-style command:
```bash
latexmk -pdf paper.tex
```

This generates `paper.pdf` (which is gitignored).

## Project Structure

### Main Document
- `paper.tex` - The complete research paper in LaTeX format
  - Uses standard LaTeX article class
  - References figures in `image/` directory
  - Bibliography in `refs.bib` with natbib/IEEEtranN style
  - Custom command: `\v{theta}` for bold vector notation

### Simulation Code Organization
The `results/` directory contains simulation experiments organized by scenario:

- `results/5_system_scale3/` - Simulations varying scale parameter of component 3
  - `boot-prob-scale3-vary.R` - Main simulation script with bootstrap
  - `data.csv` - Simulation output data
  - `figure/` - Python plotting scripts for visualization

- `results/5_system_shape3/` - Simulations varying shape parameter of component 3
  - Similar structure to scale3 experiments

- `results/lrt/` - Likelihood ratio test simulations
  - `reduced1/`, `reduced2/`, `reduced3/` - Different reduced model scenarios
  - `nomasking/` - LRT simulations without masking
  - `fig/` - Contour plots and visualization outputs

- `results/2_system_theta/` - Two-component system experiments

- `results/MTTF/` - Mean time to failure analysis

- `results/proxmox/` - Additional simulation variants

### Simulation Script Pattern
Simulation scripts typically follow this structure:
```r
# Load required libraries
library(tidyverse)
library(parallel)
library(boot)
library(wei.series.md.c1.c2.c3)

# Define theta (true parameter values)
theta <- c(shape1 = 1.2576, scale1 = 994.3661, ...)

# Set experimental parameters
N <- c(100)        # Sample sizes
P <- c(0.215)      # Masking probability
Q <- c(0.825)      # Censoring quantile
B <- 1000          # Bootstrap replicates
n_cores <- 2L      # Parallel cores

# Run simulations
# ... parallel processing with mclapply
# Output to CSV
```

### Visualization Pattern
Python scripts in `figure/` subdirectories:
- Read CSV data from parent directory
- Use matplotlib/seaborn for plotting
- Generate PDF figures for inclusion in the paper

## Key Concepts

### Well-Designed Series System
A 5-component series system where all components have similar failure characteristics:
- All shape parameters near 1.1-1.3 (slightly increasing hazard)
- All scale parameters around 900-1000
- No single weak component dominates system failure

This baseline configuration appears throughout the simulation scripts in `results/`.

### Full vs Reduced Models
- **Full Model**: Each component has its own shape and scale (2m parameters)
- **Reduced Model**: All components share a common shape (m+1 parameters)
  - Simplifies to a Weibull series system
  - Appropriate for well-designed systems
  - Evaluated using likelihood ratio tests

### Masked Data
- Only system-level failure times observed
- Candidate set C_i indicates which components might have caused failure
- Right-censoring when observation period ends before failure

## Mathematical Notation (used throughout)
- `m` - Number of components in series system
- `n` - Sample size (number of observed systems)
- `k_j` - Shape parameter of component j
- `λ_j` (lambda_j) - Scale parameter of component j
- `θ` (theta) - Complete parameter vector
- Bold symbols represent vectors (e.g., `\v\theta` in LaTeX)

## Common Tasks

### Regenerate Figures
Most figures are generated from simulation data. To update:
1. Run the relevant R simulation script in `results/[scenario]/`
2. Run corresponding Python plotting script in `results/[scenario]/figure/`
3. Figures are saved as PDFs in `image/` directory
4. Rebuild the paper: `pdflatex paper.tex && bibtex paper && pdflatex paper.tex && pdflatex paper.tex`

### Add New Simulation Scenario
1. Create subdirectory in `results/` with descriptive name
2. Write R script following the established pattern
3. Output results to CSV
4. Create `figure/` subdirectory with Python plotting scripts
5. Save figure PDFs to `image/` directory
6. Reference figures in `paper.tex` using `\includegraphics{image/filename.pdf}`

### Update Citations
- Edit `refs.bib` (BibTeX format)
- Cite in text using `\cite{key}` syntax
- Uses IEEEtranN bibliography style

## Important Files
- `paper.tex` - Main LaTeX document
- `refs.bib` - Bibliography database
- `image/` - All figure PDFs referenced in the paper
- `results/` - Simulation code and data
- `cspell.json` - Spell checker configuration
- `.gitignore` - Ignores LaTeX auxiliary files and generated PDFs
