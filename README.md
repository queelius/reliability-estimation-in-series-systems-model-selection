# When Does Model Simplification Matter?

**Consequence Analysis for Weibull Series Systems**

[Read the paper (PDF)](https://queelius.github.io/weibull-series-consequence/paper.pdf)

When a reliability engineer simplifies a series system model by assuming all components share a common Weibull shape parameter, how much accuracy is lost -- and can the data even tell the difference? This paper shows these two questions have a quantitatively aligned answer.

## Key Findings

### Bias and power are aligned

The common-shape model's MTTF prediction bias and the likelihood ratio test's detection power are aligned as functions of shape heterogeneity:

| Shape CV | MTTF Bias | LRT Power (n=500) | Recommendation |
|----------|-----------|-------------------|----------------|
| < 5% | < 0.2% | < 7% | Use reduced model confidently |
| 5--14% | 0.2--0.9% | 7--37% | Safe zone: bias negligible, test lacks power |
| 14--21% | 0.9--1.5% | 37--97% | Transition: test detects meaningful bias |
| > 27% | > 2.9% | > 99% | Use full model |

The test lacks power precisely where the consequence of using the wrong model is negligible, and has high power precisely where bias warrants switching models.

### The traditional parsimony argument is wrong

A bias-variance decomposition reveals that the full model has **lower MTTF variance** than the reduced model even when the reduced model is correctly specified (CV = 0). At n = 100: full variance = 348, reduced variance = 417. The constraint k_1 = ... = k_m forces all shape estimation error into one degree of freedom, amplifying its propagation through the nonlinear MTTF integral.

### Adaptive model selection works

An LRT-based adaptive procedure achieves RMSE within 2.5% of the always-full strategy at n >= 500, while selecting the simpler model over 90% of the time when appropriate.

### The LRT is well-calibrated; information criteria are not

| Criterion | Type I Error | Behavior |
|-----------|-------------|----------|
| LRT (alpha = 0.05) | 4.6--6.8% | Well-calibrated |
| AIC | 8.2--12.4% | Liberal (~2x nominal) |
| BIC | 0--0.2% | Over-conservative |

## Repository Structure

```
.
├── paper/                    # LaTeX source and figures
│   ├── paper.tex            # Main manuscript
│   ├── refs.bib             # Bibliography
│   ├── Makefile             # Build automation
│   └── image/               # Figures (PDF)
├── qrei/                    # QREI submission variant
│   ├── manuscript.tex       # Journal-formatted manuscript
│   └── cover-letter.tex     # Cover letter
├── results/                 # Simulation code and data
│   ├── consequence/         # Consequence analysis (MTTF bias, MSE)
│   │   └── figure/          # Including bias-variance decomposition
│   ├── adaptive/            # Adaptive model selection
│   ├── lrt/                 # Likelihood ratio test simulations
│   │   ├── divergence/      # Type I error and power vs shape CV
│   │   ├── vary_m/          # Effect of number of components (m = 2-8)
│   │   ├── vary_p/          # Effect of masking probability (p = 0.05-0.70)
│   │   ├── vary_q/          # Effect of censoring level (q = 0.50-1.00)
│   │   └── nomasking/       # Ideal case baseline (p=0, q=1)
│   ├── 5_system_scale3/     # Scale parameter sensitivity
│   ├── 5_system_shape3/     # Shape parameter sensitivity
│   └── sim_utils.R          # Shared vectorized simulation utilities
├── docs/                    # GitHub Pages (paper PDF)
└── CLAUDE.md                # Development guidance
```

### Data Pipeline

```
R scripts (Monte Carlo) → CSV → Python analysis → PDF figures → LaTeX paper
```

Each experiment in `results/` contains an R script that runs simulations, a CSV of raw results, and a `figure/` subdirectory with a Python analysis script that produces publication-quality PDFs.

## Building the Paper

```bash
cd paper
latexmk -pdf paper.tex
```

Or with Make:

```bash
cd paper
make            # build paper.pdf
make docs       # copy PDF to docs/ for GitHub Pages
```

## Dependencies

### R Packages
- [`wei.series.md.c1.c2.c3`](https://github.com/queelius/wei.series.md.c1.c2.c3) -- Weibull series system with masked data
- [`algebraic.mle`](https://github.com/queelius/algebraic.mle) -- Maximum likelihood estimation utilities
- [`algebraic.dist`](https://github.com/queelius/algebraic.dist) -- Algebraic distribution functions
- [`md.tools`](https://github.com/queelius/md.tools) -- Masked data tools
- `tidyverse`, `ggplot2`, `parallel`, `boot`

### Python
- `matplotlib`, `seaborn`, `pandas`, `numpy`

### LaTeX
Standard distribution with `amsmath`, `amsthm`, `graphicx`, `natbib`, `hyperref`

## Related Work

- Towell (2025). *Masked Causes of Failure in Series Systems: A Likelihood Framework*. [DOI:10.5281/zenodo.18725577](https://doi.org/10.5281/zenodo.18725577) -- the C1-C2-C3 likelihood framework this paper builds on
- [`wei.series.md.c1.c2.c3`](https://github.com/queelius/wei.series.md.c1.c2.c3) -- R package implementing the parametric models

## Citation

```bibtex
@article{towell2026consequence,
  title={When Is Model Simplification Safe? Consequence and Detectability for Common-Shape Weibull Series Systems under Masked Data},
  author={Towell, Alexander},
  year={2026},
  note={Preprint},
  url={https://github.com/queelius/weibull-series-consequence}
}
```

## License

Creative Commons Attribution 4.0 International (CC-BY-4.0).

## Author

**Alexander Towell**
ORCID: [0000-0001-6443-9897](https://orcid.org/0000-0001-6443-9897)
[lex@metafunctor.com](mailto:lex@metafunctor.com)
