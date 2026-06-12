# Logic Checker Report

**Reviewer role**: proof correctness, claim support, logical chain integrity.
**Manuscript reviewed**: `qrei/manuscript.tex` (primary), `paper/paper.tex` (cross-checked).
**Date**: 2026-05-03

## Summary

The paper makes empirical claims supported by simulation tables. There is no formal theorem requiring proof. Property 1 (Weibull closure) is cited from Barlow-Proschan 1975 and is correct. The reasoning chain from "alignment observation" to "adaptive procedure works" is sound. There is one important *latent* logical gap: the paper observes the bias-detectability alignment but does not derive it from any structural argument. This is the user-flagged "structural insight" question and it is the dominant logic finding.

**Severity counts**: critical 0, major 2, minor 3, suggestions 2.

## Major Findings

### MAJ-L1: Empirical alignment observed but not derived (the structural-insight gap)
**Location**: Sections 1, 3.3, and Conclusion. Cited as the central thesis throughout.
**Quoted text** (Section 3.3, lines 180-181):
> "Figure 1 reveals the quantitative alignment between detectability and consequence. The LRT's power curve rises faster than the bias curve: by the time the MTTF bias reaches engineering-significant levels, the LRT already rejects reliably. This rate asymmetry is what makes the adaptive procedure in Section 5 effective."

**Problem**: The "rate asymmetry" is the paper's headline finding. As written, it is presented as an empirical observation about Huairu-2013 plus shape perturbations. There is no derivation showing that this asymmetry is *structural* and so should hold for other configurations. The available scaling argument (sketched in literature-context Section 5) is straightforward:

1. By delta-method around homogeneous reduced fit, MTTF bias is O(CV²) and is *not* attenuated by sample size $n$ (specification bias).
2. By contiguous-alternatives theory (van der Vaart §15), LRT non-centrality is $n \cdot O(\text{CV}^2)$, so the CV at which power reaches a fixed level shrinks like $1/\sqrt{n}$.
3. The asymmetry arises because bias is unattenuated by $n$ while detection-threshold-CV shrinks with $n$.

**The user's prompt suggests a plausible derivation route.** I checked it. The "O(CV⁴) vs O(CV²)" scaling stated there is *not quite right*: both quantities are leading-order O(CV²) under contiguous alternatives. The asymmetry is in the role of $n$, not in the polynomial order of CV alone.

**Logical impact**: without the derivation, the paper's main thesis depends on a single baseline. Reviewers will reasonably ask whether the alignment generalizes. With one paragraph of contiguous-alternatives analysis (probably 250 words plus one display equation), the paper's central claim is upgraded from "we observed it for Huairu-2013" to "we predict and verify it from first principles."

**Suggestion**: add a "Theoretical Justification" subsection (between current Sections 4 and 5) that:
- Defines the local-alternative direction: $k_j = k_0 (1 + \epsilon_j)$ with $\sum \epsilon_j = 0$ and $\sum \epsilon_j^2 = (m-1) \text{CV}^2$.
- States MTTF bias = $\text{MTTF}_0 \cdot (\frac{1}{2} \beta_2 \text{CV}^2 + o(\text{CV}^2))$ for some constant $\beta_2$ depending on $\Gamma$ and the scale ratios. Just sketch, not derive in full.
- States LRT non-centrality = $n \cdot c \cdot \text{CV}^2$ for $c$ depending on FIM block structure (here cite the FIM sibling paper for the numerical $c$).
- Concludes: at fixed $n$, the detection-CV threshold scales as $1/\sqrt{n}$ while bias is unattenuated. The alignment is therefore a structural property of the problem, with the constant of proportionality determined by the specific baseline.

This is **the single most valuable revision** the paper could make. It addresses every "what about other configurations?" reviewer comment in advance.

### MAJ-L2: "Sample size independence of bias" claim is correct but the language is loose
**Location**: Section 3.2, lines 174-175.
**Quoted text**:
> "Third, the bias is largely independent of sample size: a 50-fold increase from $n = 100$ to $n = 5000$ changes the bias at CV $\approx 27\%$ from $+3.2\%$ to $+2.6\%$, confirming that this is a specification bias, not a finite-sample artifact."

**Problem**: The claim is true and the data supports it (Table 2 shows bias drifting only modestly with $n$ at fixed CV). But the inference "this is a specification bias, not a finite-sample artifact" is the *correct conclusion*; what the data show is *consistency with* that conclusion, not direct evidence. To make this rigorous:
- At $n = 100$, Monte Carlo finite-sample noise on bias estimates is non-negligible (binomial standard error of order $1/\sqrt{500} \approx 0.045$, scaled by RMSE).
- The drift from 3.2% to 2.6% with 50× sample size is consistent with both pure specification bias plus noise *and* a slowly converging finite-sample effect.

**Fix**: replace "confirming that this is a specification bias" with "consistent with this being a specification bias rather than a finite-sample artifact, since the difference is within Monte Carlo error of the bias estimates." Or better: delete the sentence and let Table 2 speak. The substantive claim is fine.

## Minor Findings

### MIN-L1: "Sub-linear bias" language scrubbed but a residue remains in `.papermill.md` (not in manuscript)
**Location**: `.papermill.md` line 137 ("prediction bias grows sub-linearly, LRT power super-linearly").
**Verification**: I grepped both `qrei/manuscript.tex` and `paper/paper.tex` for "sub-linear / super-linear / sublinear / superlinear". *No matches.* The Feb-27 review correctly flagged this as factually wrong; the manuscript text was fixed. The metadata file still contains the stale phrase, which is non-load-bearing but should be cleaned up if `.papermill.md` is published anywhere.

### MIN-L2: "MSE surprise" claim is correct as stated, but the explanation is asserted, not demonstrated
**Location**: Section 3.3, lines 178-179.
**Quoted text**:
> "A bias-variance decomposition reveals the mechanism: the constraint $k_1 = \cdots = k_m$ forces all shape estimation error into a single degree of freedom, which propagates through the nonlinear MTTF integral with greater amplification than the distributed errors of the unconstrained estimator [White 1982]."

**Problem**: the data show MSE_full < MSE_reduced at CV=0 for $n=100$ (MSE 422 vs 498) and similar at $n=500, 1000$, with the gap closing as $n$ increases. The claimed mechanism (one-DOF constraint amplification through nonlinear functional) is plausible but is *asserted, not derived*. White (1982) is about MLE under misspecification generally and does not establish this specific mechanism for the constrained-shape Weibull system. A reviewer could legitimately ask: where is the calculation that shows the variance amplification factor is *larger* under the constrained estimator?

**Fix**: either (a) demonstrate it numerically using one paragraph of analysis (e.g., compare $\text{Var}(\widehat{\text{MTTF}})$ from delta-method using full-FIM vs reduced-FIM), or (b) soften the framing: "Empirically, the constraint amplifies MTTF estimation variance more than it reduces parameter-level variance. A formal derivation of this amplification is beyond the present scope."

The FIM sibling paper has the homogeneous-Weibull FIM in closed form. Adding (a) would take ~half a page. It is also the cleanest empirical bridge to the FIM paper.

### MIN-L3: Type I error claim (4.6%-6.8%) holds in a strict sense, with one minor caveat
**Location**: Section 4.1, line 201; Conclusion.
**Quoted text**: "Under perfect homogeneity ($\text{CV}_k = 0$), the LRT rejection rate ranges from 4.6\% to 6.8\% across all sample sizes tested ($n = 100$ to $10{,}000$)..."

**Verification**: the underlying CSV (`summary_divergence.csv` line 2-6) confirms reject rates 0.054, 0.056, 0.046, 0.068, 0.046 across $n=100, 500, 1000, 5000, 10000$ at CV=0. Min 0.046 (4.6%), max 0.068 (6.8%). Claim is exact.

**Minor caveat**: with 500 reps each, the binomial Wilson 95% CI for a 5% rejection rate is roughly [3.4%, 7.3%]. So 4.6% and 6.8% are both within nominal-rate CI of $\alpha = 0.05$. The "well-calibrated" framing is supported, but a careful reader will want either (a) more reps for tighter CI, or (b) a sentence noting that all five rejection rates are within Monte Carlo error of $\alpha = 0.05$.

## Suggestions

### SUG-L1: Property 1 is cited correctly but could note one cosmetic point
The Weibull closure property as stated requires $T_j$ independent. The paper states "Let $T_1, \ldots, T_m$ be independent." Good. The series-system framing assumes this elsewhere. Internally consistent.

### SUG-L2: Equation (3) (the masked-likelihood) could benefit from a sanity-check pointer
The likelihood is stated correctly assuming C1-C2-C3 (the foundation paper's sufficient conditions). The current paper writes "the masking mechanism is non-informative about $\v\theta$ [towell2023reliability]." This is fine but understated: the C1-C2-C3 conditions are formal, named, and provable from the foundation paper. Updating the citation to `towell2025masked` *and* naming the conditions ("under conditions C1, C2, C3 of [towell2025masked]") gives the reader a hook to find the rigor. This is mostly a citation hygiene point but improves logical traceability.

## Cross-checks Performed

I verified the following against simulation outputs:

| Manuscript claim | Source | Verified |
|------------------|--------|----------|
| Bias = 1.5% at CV ≈ 20.5%, $n=500$ | Table 2 row 7 | yes (`summary_consequence.csv` row 7: bias_red_pct=1.49) |
| LRT power ≈ 79% at CV ≈ 20.5%, $n=500$ | Section 1 + Fig 1 | yes (`summary_divergence.csv` target_cv=0.15: reject=0.7896 → "nearly 80%") |
| Bias < 1% through CV ≈ 14%, $n \geq 500$ | Section 3.2 | yes (Table 2: at CV=13.7%, $n=500$, bias=0.9%) |
| Type I error 4.6-6.8% across $n$ | Section 4.1 | yes |
| LRT power < 8% at CV=2.7%, $n \leq 1000$ | Section 4.1 | yes (rejection rates 0.048, 0.062, 0.052) |
| Adaptive RMSE within 2.5% of full at $n=500$ | Conclusion | yes (Table 4: at CV=20.5%, $n=500$, full=4.4, adaptive=4.5; ratio=1.023) |
| Selects reduced > 90% at low CV | Conclusion | yes (Table 4: 89-95% at CV ≤ 5.5%) |

All numerical claims survive verification.

## Logical Chain Audit

1. Premise: well-designed series systems have similar shapes, different scales. (Asserted; reasonable.)
2. Premise: common-shape constraint yields Weibull system lifetime (Property 1, established).
3. Question: when shapes differ slightly, is the common-shape model still acceptable?
4. Operational answer: define "acceptable" via prediction bias on system-level functionals.
5. Empirical finding: bias is small until CV exceeds 15%, when LRT also gains power.
6. Conclusion: alignment makes adaptive LRT-based selection cheap and effective.

Each step is supported. The key weakness is that step 5 is empirical only, and step 6 inherits that weakness. The cure is the structural argument flagged in MAJ-L1.

## Verdict

The paper's logical structure is sound. The main verifiable claims hold. The single major opportunity is to add a structural derivation of the alignment, which would lift the paper from "demonstrated for Huairu-2013" to "structural property derived and verified." This is feasible in one to two pages and uses only standard tools (delta method, Wilks/Le Cam contiguous alternatives).

Confidence: high.
