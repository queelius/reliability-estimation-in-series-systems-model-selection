# Model Selection for Reliability Estimation in Series Systems

This repository contains the research paper, simulation code, and supplementary materials for studying model selection in series systems with Weibull-distributed component lifetimes.

## Key Findings

**When can reliability engineers safely use a simpler model?**

- For **well-designed systems** (components with similar failure characteristics), a reduced homogeneous-shape Weibull model is statistically indistinguishable from the full heterogeneous model—even with 30,000 observations
- This means practitioners can confidently use the simpler model, which:
  - Halves the parameter count from 2m to m+1
  - Renders the system itself Weibull-distributed
  - Reduces estimator variance without sacrificing accuracy
- However, deviations in even a **single component's shape parameter** quickly provide evidence against the reduced model

### Practical Guidelines

| Divergence Level | CV of Shape Parameters | Recommendation |
|-----------------|------------------------|----------------|
| Low | < 10% | Use reduced model confidently |
| Moderate | 10-20% | Depends on sample size |
| High | > 25% | Use full heterogeneous model |

## Repository Structure

```
.
├── paper/                  # LaTeX source and figures
│   ├── paper.tex          # Main manuscript
│   ├── refs.bib           # Bibliography
│   └── image/             # Figures (PDF)
├── results/               # Simulation code and data
│   ├── 5_system_scale3/   # Scale parameter sensitivity
│   ├── 5_system_shape3/   # Shape parameter sensitivity
│   ├── lrt/               # Likelihood ratio test simulations
│   │   ├── divergence/    # Type I error and power analysis
│   │   ├── vary_m/        # Effect of system complexity
│   │   ├── vary_p/        # Effect of masking probability
│   │   └── vary_q/        # Effect of censoring level
│   └── ...
├── docs/                  # GitHub Pages site
└── CLAUDE.md              # Development guidance
```

## Building the Paper

```bash
cd paper
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

Or using latexmk:
```bash
cd paper
latexmk -pdf paper.tex
```

## Dependencies

### R Packages
- `wei.series.md.c1.c2.c3` - Weibull series system with masked data
- `algebraic.mle` - Maximum likelihood estimation utilities
- `tidyverse`, `ggplot2`, `parallel`, `boot`

### Python Packages
- `matplotlib`, `seaborn`, `pandas`, `numpy`

### LaTeX
Standard distribution with `amsmath`, `amsthm`, `graphicx`, `natbib`, `hyperref`

## Citation

```bibtex
@article{towell2024modelselection,
  title={Model Selection for Reliability Estimation in Series Systems},
  author={Towell, Alex},
  year={2024},
  note={Preprint}
}
```

## Related Work

This paper builds on [Towell (2023)](https://github.com/queelius/reliability-estimation-in-series-systems), which developed the likelihood model for masked and censored series system data.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Alex Towell**
[lex@metafunctor.com](mailto:lex@metafunctor.com)
