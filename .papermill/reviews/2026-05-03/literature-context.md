# Literature Context Packet

**Paper**: When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems
**Compiled**: 2026-05-03

This packet merges findings from the prior comprehensive literature scout (2026-02-27) with verification against the current bibliography and ecosystem state.

## 1. Literature Scoreboard for Cited Bib Entries

The bib (`qrei/refs.bib`) contains 22 entries; only 13 are cited in the qrei manuscript:

**Cited and grounding the work**: `barlow1975` (Weibull closure), `Huairu-2013` (baseline), `wilks1938` (LRT theory), `akaike1974`, `schwarz1978`, `byrd1995` (L-BFGS-B), `White-1982` (MLE under misspecification), `Craiu-2005` (model selection for masked competing risks), `Usher-1988`, `Lin-1993`, `Joh-1989` (frequentist masked-data MLE), `towell2023reliability` (foundation, but stale, should be `towell2025masked`), `towell2023weibull` (R package, archived, should be `maskedcauses`).

**Not cited but in bib (silent indictment)**:
- `Amma-2001` (Sarhan): masked system life data, exponential. Closest to the present problem in literature. The omission is conspicuous.
- `Amma-2004` (Sarhan): linear failure rate model with masked data. Direct competitor for "two-parameter family with masked data."
- `Zhibi-2007` (Tan): exponential component reliability from uncertain life data, series and parallel. Direct relevance.
- `Zhibi-2005` (Tan): masked binomial system testing. Less direct.
- `Lin-1996`: Bayes estimation of component reliability from masked system-life data.
- `Usher-1996`: Weibull component reliability prediction with masked data. Most directly competitive prior work to this paper.
- `burnham2002` (model selection AIC/BIC monograph), `lawless2003` (Lifetime Data textbook), `meeker1998` (Statistical Methods for Reliability Data textbook): all standard references that reviewers expect to be cited.

## 2. The Most Important Missing Citations

### 2A. Cross-ecosystem (the user-flagged criticality)

| Citation | What It Is | Why The Paper Needs It |
|----------|------------|------------------------|
| `towell2025masked` (foundation) | "Masked Causes of Failure in Series Systems: A Likelihood Framework", DOI 10.5281/zenodo.18725577. Develops the C1-C2-C3 framework, the likelihood used in Eq. (3) of this paper, and the partial identifiability theorem. | Paper cites `towell2023reliability` (master's project on GitHub) as if it were the canonical likelihood reference. The 2025 foundation paper supersedes it. Reviewers will see the GitHub-only reference and downgrade rigor. |
| `towell2025weibull-series` (sibling) | Weibull-FIM paper, draft v0.1.0. Closed-form per-observation FIM for the homogeneous Weibull series (the very model this paper studies as the "reduced" alternative). | Provides the asymptotic variance theory backing the empirical bias-detectability claims. The two papers are perfect complements: this one shows behavior empirically, while the FIM paper explains the rate scaling theoretically. The omission orphans both papers. |
| `maskedcauses` (R package) | Live successor to `wei.series.md.c1.c2.c3`. Hosted at github.com/queelius/maskedcauses, version 0.10.0. | Paper cites the archived package. Cannot send reviewers to a dead artifact. |

### 2B. Standard reliability and model-selection literature the paper omits

| Citation | Status in this paper | Comment |
|----------|---------------------|---------|
| Pareek, Kundu, Kumar (2009), J. Stat. Comput. Simul. | Not in bib | Most cited "common-shape Weibull competing risks" paper. Direct comparator. |
| Pascual (2005), J. Quality Technology | Not in bib | Precedent for misspecification consequence analysis (Weibull vs lognormal). |
| McCool (1970, 1976), Technometrics | Not in bib | Classical LRT for Weibull shape equality between samples, a direct precedent. |
| Crowder (2001), *Classical Competing Risks* | Not in bib | Standard textbook reference for competing-risks masking. |
| Claeskens & Hjort (2003, 2008), Focused Information Criterion | Not in bib | FIC formalizes "consequence for specific prediction" and is the conceptual ancestor of this paper's "consequence analysis" framing. Citing it strengthens novelty argument. |
| Sarhan (2001) `Amma-2001` | In bib, uncited | Should be cited in Related Work. |
| Usher (1996) `Usher-1996` | Not in bib | Weibull-specific masked data, direct precedent. The most damaging omission. |
| Pareek-Kundu-Kumar | Not in bib | See above. |

## 3. Competing and Similar Work, Where This Paper Sits

### 3A. Claim of novelty, verified

The paper claims (Section 1): "The model selection question, common shape versus heterogeneous shapes, has not, to our knowledge, been studied systematically for masked data, nor has the consequence of misspecification been quantified."

**This claim survives a literature search.** Existing work splits cleanly into three baskets:

1. **Estimation under masked competing risks/series** (Sarhan 2001/2004, Usher-Hodgson 1988, Lin-Usher-Guess 1993, Usher 1996, Guo et al. 2013, Towell 2023/2025): assumes a model and estimates parameters. Does not study what happens when the wrong model is fit.
2. **Model selection for competing risks with masking** (Craiu & Lee 2005): closest comparator. Selects between *cause-specific hazard families* (Weibull vs lognormal vs ...), not between *constraints on a Weibull family* (common shape vs free shapes).
3. **Misspecification consequences in reliability** (Pascual 2005, White 1982 in general): not in masked-data setting.

**Verdict**: the intersection of (i) Weibull series, (ii) masked plus censored data, (iii) common-shape vs heterogeneous-shape constraint, and (iv) consequence quantification for the engineering prediction (MTTF/R(t)) is genuinely unoccupied territory. The paper's positioning is honest.

### 3B. Adaptive procedure novelty, calibrated

The paper claims as a contribution (Contribution 2): an "LRT-based adaptive procedure exploits this alignment, achieving RMSE within 2.5%..."

**Calibration**: LRT for nested model selection is textbook (Wilks 1938, Lehmann & Romano 2005, every reliability textbook). The contribution here is not the *mechanism* of LRT-based selection. It is the empirical demonstration that, *for this specific problem*, the LRT's selection profile is favorably matched to the prediction-bias profile. In other words, the contribution is *evaluation*, not *invention*. Phrasing in current draft slightly oversells. See novelty-assessor for fix.

## 4. Topical Venue Landscape

| Venue | Fit | Direct precedents |
|-------|-----|-------------------|
| Quality and Reliability Engineering International (QREI) | Strong topical match. Published Guess and Usher (1989) (cited as `Joh-1989` in this paper's bib). Engineering-practical framing aligned with house style. | Yes, Joh-1989. |
| IEEE Transactions on Reliability | Strong topical match. Published Usher-Hodgson 1988 and Lin et al. 1993, the foundational masked-data papers in this paper's intellectual lineage. Higher prestige and circulation. | Yes, multiple. |
| Technometrics | Moderate fit. Published Craiu-Lee 2005 (model selection for competing risks). Demands more theory or an unusually strong empirical case. | Yes, Craiu-Lee 2005 is the closest match the paper itself cites. |
| Lifetime Data Analysis | Moderate fit. Specialized in lifetime data theory. Would expect more theoretical contribution (such as the FIM scaling argument). | Many adjacent papers. |
| Reliability Engineering and System Safety | Strong topical match (published all three Sarhan papers and both Tan papers, which are uncited in this draft). Probably a back-up if QREI rejects. | Yes, multiple. |

## 5. The Theoretical Gap That Could Be Closed

The paper observes empirically that bias and detection power are "favorably aligned" but does not derive *why*. A standard scaling argument is available:

- **MTTF bias**: under common-shape misspecification, the leading-order Taylor expansion of MTTF around the homogeneous reduced fit yields O(CV²) bias in the system MTTF integral. (This is a one-page derivation given the Weibull closure result and standard delta-method.)
- **LRT power**: under contiguous local alternatives (Le Cam 1960; van der Vaart 1998 §15), the non-centrality parameter of the LRT scales as $n \cdot \kappa^\top I(\theta_0) \kappa$ where $\kappa$ is the local-alternative direction in $\mathbb{R}^{m-1}$. With shape heterogeneity parametrized by CV, $\kappa \sim O(\text{CV})$, so the non-centrality is $O(n \cdot \text{CV}^2)$ and power scales correspondingly. Effective scaling is $O((\sqrt{n} \cdot \text{CV})^2) = O(n \cdot \text{CV}^2)$ in the non-centrality. As $n$ grows, the *threshold* CV at which power reaches a fixed level shrinks like $1/\sqrt{n}$. (This is the standard $\sqrt{n}$-consistency result.)
- **The asymmetry is then exact**: bias is O(CV²) but is *not* attenuated by $n$ (it's a specification bias). Power, in CV units at fixed sample size, scales such that detection occurs at CV $\sim 1/\sqrt{n}$. So there is a transition CV at fixed $n$ where the LRT becomes powerful, and below that CV the bias is at most $O(1/n)$, well below practical engineering thresholds for any reasonable $n$.

**The user's tentative scaling argument is qualitatively correct.** It does not rise to the level of an "O(CV⁴) vs O(CV²)" alignment as written in the user prompt, however. Both bias and the *boundary CV* for fixed power are O(CV²) in the appropriate sense. The asymmetry comes from *attenuation by sample size*: bias is unattenuated, while power's detection threshold shrinks. Adding this argument (one or two paragraphs, with a clean local-alternative analysis) would substantially strengthen the paper without ballooning its scope.

## 6. The Single-System Validity Question

The Huairu-2013 baseline is one configuration: 5 components, scales 840-994, shapes 1.13-1.26 (CV ≈ 4%). The paper varies CV via a perturbation around this configuration (uniformly spaced shapes about a mean of 1.18) but does not vary $m$, scale ratio (max/min $\lambda_j$), or shape mean.

**Lit-survey verdict**: the *qualitative* alignment between bias and detection should hold for any well-designed system because the underlying scaling argument (Section 5 above) is generic. The *quantitative* boundary ("CV ≈ 15% for 1% bias") is system-specific and depends on:
- $m$: more components dilute single-component perturbations, leading to a flatter bias curve.
- Failure-mode dominance: if one component is dominant, the system MTTF approaches that component's MTTF, regardless of others. Common-shape will hide the dominant component poorly.
- Censoring level: heavier censoring reduces information about both shape and scale heterogeneity.

Appendix C (`vary_m`, `vary_p`, `vary_q`) does some of this for *power* but not for *bias*. Adding a bias-vs-{m, q} table (or even a sentence noting that the alignment is robust because of the underlying scaling) would close this gap.

## 7. Summary For The Specialist Reviewers

- The novelty claim (consequence analysis for masked Weibull series) survives literature search.
- The adaptive procedure is empirical evaluation, not invention.
- The paper has a real theoretical scaffold available (local alternatives plus delta method) that it does not use.
- Cross-citation hygiene is the most pressing problem: stale foundation citation, missing sibling FIM paper, archived R package reference.
- Multiple standard references (Sarhan, Tan, Usher 1996, Pareek et al., Pascual, Crowder, Burnham-Anderson, Lawless, Meeker-Escobar) should be added. Some are already in the bib but uncited.
