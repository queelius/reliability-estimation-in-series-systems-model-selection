# Unified Review: weibull-series-consequence (2026-06-10/11 session)

**Target:** working-tree `paper/paper.tex` (348 lines, 11pp, uncommitted condensed draft, mtime 2026-02-28). Git HEAD holds a stale longer draft; the working tree is the real current manuscript.
**Method note:** the multi-agent orchestrator was killed twice by the account spend limit, so this review was completed inline by the lead session: data verification first (notes/verify-thesis-claims.py, notes/verify-zero-gain.py), then logic, methodology, prose, citation, and format passes. Prior art was surveyed by a dedicated background agent (prior-art.md in this directory). Dedup baseline: the 2026-05-03 eight-specialist review of the near-identical qrei variant.
**Companion documents:** `prior-art.md` (novelty threats, 18 ready BibTeX entries), `notes/zero-first-order-gain.md` (new proposition + derivation sketch), `.papermill/state.md` thesis v4 (refined 2026-06-10).

## Verdict

**MAJOR REVISION toward thesis v4, and the planned rework is the right move.** The simulation evidence is solid and internally consistent (every headline number re-verified against the CSVs this session). What separates the current draft from a strong IEEE TR submission is not data but theory and framing: the draft asserts mechanisms it does not derive, in one place with a wrong citation, while the actual derivations (delta-method bias scaling, Le Cam noncentrality with an empirically confirmed constant, and a new zero-first-order-gain proposition) are now verified and waiting in notes/. Without the rework the paper remains a competent simulation study better suited to QREI; with it, the IEEE TR switch is justified.

## New findings (not in the 2026-05-03 review)

### Critical

**NEW-C1. The masking assumptions stated in Section 2.2 do not imply the likelihood in Eq. (3).** `paper.tex:87` states only C1 (containment, K_i in C_i) and C3 (masking non-informative about theta). The reduced likelihood form R(t) * sum_{j in C} h_j(t) used in Eq. (3) (`paper.tex:93`) additionally requires C2 (symmetric masking: candidate-set probability equal across members conditional on cause). Without C2 the masking probabilities do not factor out and the equation is wrong as a consequence of the stated assumptions. Fix: state all three conditions, name them C1-C2-C3 per the foundation framework, and cite the foundation paper (towell2025masked). One sentence plus a citation swap.

### Major

**NEW-M1. The MSE mechanism sentence is unsupported and miscited.** `paper.tex:175`: "the constraint forces all shape estimation error into a single degree of freedom, which propagates through the nonlinear MTTF integral with greater amplification ... [White-1982]". Problems: (a) White (1982) concerns MLE under misspecification; at CV = 0 the reduced model is correctly specified, so the citation does not apply to the claim it decorates. (b) As stated, the claim collides with constrained-MLE asymptotics (Aitchison-Silvey 1958: imposing a true constraint weakly reduces asymptotic variance of any smooth functional), and a referee who knows that result will object. The resolution is the new zero-first-order-gain proposition (notes/zero-first-order-gain.md): at any common-shape point the constraint provides exactly zero first-order variance reduction for any functional of the system lifetime distribution, so the finite-n ordering is decided at second order, where the data show the full model wins. Verified numerically this session: relative first-order gap ~1e-5 across equal, baseline, and strongly unequal scales (complete-data FIM projection); derivation sketch checks out for complete data via the (k, eta = lambda^-k) parameterization; masked/censored case is conjectured, supported by the simulated variance equality at n = 5000 (8.4 vs 8.4). Action: replace the sentence with the proposition (statement in text, proof in appendix), keep White (1982) only where pseudo-true parameters are discussed (CV > 0).

**NEW-M2. The headline alignment claim is stated without its sample-size qualifier.** Abstract (`paper.tex:41`) and Conclusion (`paper.tex:299`): "by the time it reaches 1.5% (CV ~ 20%) the LRT already rejects at nearly 80%". True at n = 500 (0.790); false at n = 100 (0.200) and an understatement at n = 1000 (0.968). The correct general statement is the two-regime safety property of thesis v4: detection-led safety for n >~ 1000 (CV50 ~ 3.5/sqrt(n) lies below the ~18% bias boundary), noise-dominance safety for n <~ 500 (4-10% sampling RMSE dwarfs the <= 3% specification bias through CV ~ 27%), with the honest exception window at small n and extreme CV (n = 100, CV ~ 30-40%) where the pretest hump costs up to ~18% RMSE.

**NEW-M3. Appendix B asserts a wrong mechanism for AIC.** `paper.tex:336`: "AIC is liberal (8.2-12.4%, with false positive rate increasing with n because its fixed penalty does not scale)". The false-positive rate of AIC under H0 converges to P(chi2_4 > 8) = 9.2%; it does not increase with n. The observed 8.2 -> 12.4% drift is within Monte Carlo noise (binomial SE ~ 1.3% at 500 reps; verified rates 9.8, 8.8, 8.2, 12.4, 10.8% across n). The correct statement: AIC's false-positive rate does not vanish as n grows (unlike BIC's), stabilizing near 9.2%, hence "liberal at every n". The "~2x" abstract-level characterization survives.

**NEW-M4. Specification bias and finite-sample estimation bias are conflated in Table 1.** The n = 100 column contains a +0.36% pure estimation bias visible at CV = 0 (where specification bias is zero by construction); the text reads the whole column as misspecification bias. The two sources are additive to leading order and the paper never separates them. Cheap structural fix: compute the population-level bias curve directly (pseudo-true reduced parameters by KL projection at each CV; deterministic numerical optimization, no Monte Carlo), plot it under the simulated curves. This proves n-independence by construction, isolates the specification component, and nails the leading-order coefficient (empirically bias ~ 0.30-0.35 * CV^2 at n = 5000, local exponent ~ 2.15 over CV 5-41%).

**NEW-M5. The MSE counterexample is presented without its strongest confirmation or its error bars.** Verified this session: paired per-replication tests give t = -3.65 (n = 100), -1.80 (n = 500), -1.84 (n = 1000) in the consequence data, independently replicated in the adaptive dataset (t = -4.82, -3.07, -2.32), and the effect vanishes at n = 5000 (t = +0.24), exactly as first-order theory requires once the proposition is in hand. Table 3 stops at n = 1000, so the paper hides the vanishing, which is confirmatory evidence, not a weakness. The decomposition also shows the effect is variance-driven (VarR = 417 > VarF = 348 at n = 100) while bias-squared favors the reduced model (0.6 vs 14.1): the draft's "variance" wording in the abstract is right, but Section 3.3 says "MSE" and neither reports the decomposition. Action: extend the table to n = 5000, add paired-test significance or MC standard errors, report the variance/bias-squared split.

**NEW-M6. The uniqueness claim lost its proof in condensation and is imprecisely stated.** `paper.tex:106`: "The common-shape constraint is the only single-parameter restriction that yields a Weibull system lifetime." (a) The constraint k_1 = ... = k_m removes m-1 parameters; "single-parameter restriction" is not the right description (it is reduction TO a single shared shape). (b) The cleaner true statement is a characterization: the system lifetime is Weibull if and only if all shapes are equal, by linear independence of distinct powers t^k (the HEAD draft's dropped Remark argued exactly this, correctly). Restore the characterization with its two-line proof.

**NEW-M7. R(t) prediction results were dropped though the data exists.** The condensed draft evidences only MTTF bias, while abstract and conclusion speak of "predictions" generally. data-consequence.csv contains R(MTTF/2), R(MTTF), R(2*MTTF) under truth, full, and reduced models for every replication. Either reinstate an R(t) bias table/figure (cheap) or scope the prose to MTTF. The v4 proposition covers all system functionals, so reinstating strengthens the story.

### Minor

**NEW-m1. Optimizer asymmetry, undisclosed.** `results/sim_utils.R:215-258`: full-model fits use parscale = theta0; reduced-model fits omit parscale (mixing k ~ 1.2 with lambda ~ 900) and instead add a Nelder-Mead polish, keeping the better fit. The n = 5000 variance equality argues no material distortion, but the asymmetry belongs in the simulation-design appendix.
**NEW-m2. Silent replication filtering.** Full-model nonconvergence and Lambda < 0 replications are dropped (consequence-analysis.R lines ~178, ~208); reduced-model convergence is recorded but never filtered. Quantified: <= 1/500 dropped at CV = 0 (so the CV = 0 headline results are unaffected), up to 13/500 at CV = 30%. State the filtering and counts in the paper.
**NEW-m3. No Monte Carlo standard errors anywhere.** Example: the 4.6-6.8% Type I range has binomial SE ~ 1%, so all five values are consistent with exactly 5%; presenting the range without SE invites over-reading. Add SEs or a global MC-uncertainty note.
**NEW-m4. Table 3 rounding obscures a true claim.** "Within 2.5% of always-full at n >= 500" is correct in exact data (max 2.38%, at CV = 6%, n = 500), but displayed 1-decimal values imply 3.3% at (n = 1000, CV = 5.5). Add a decimal or state the exact max overhead.
**NEW-m5. n = 100 overhead range slightly off.** Claimed "8-18%"; exact 5.8-17.7%. Say "6-18%" or "up to 18%".
**NEW-m6. Units inconsistency.** Table 1 mixes relative bias (%) with RMSE in time units; Table 3 uses RMSE as % of true MTTF. Harmonize (relative throughout).
**NEW-m7. Target-vs-actual CV confusion.** Section 3.1 says "9 levels (0-30%)" (target) while tables show actual CV up to 41.1%; one clause fixes it.
**NEW-m8. Reproducibility of the archived package.** Simulations cite wei.series.md.c1.c2.c3 (now archived per ecosystem records); add a version/availability note or point to the maintained successor (maskedcauses).
**NEW-m9. Wilks regularity caveat.** The chi2_{m-1} null is interior (no boundary issue), but identifiability of the full model under masking/censoring deserves one sentence with a pointer to the foundation framework.

### Suggestions

**NEW-S1.** Add the calibrated power law to Section 4: ncp ~ 0.5 * n * CV^2 (stable to +/- 0.03 across n in [1000, 10000], CV in [2.7%, 27%]) and CV50 ~ 3.5/sqrt(n) (log-log slope -0.468 vs theoretical -0.5). One paragraph and one fit line; it is the empirical heart of the decoupling and the data already supports it.
**NEW-S2.** Typeset Eq. (3) as delta_i [log R + log sum_{j in C_i} h_j] (algebraically identical, cleaner, makes NEW-C1's dependence on C2 visible).
**NEW-S3.** Appendix C data (vary_p, vary_q) can calibrate the noncentrality constant as a function of masking and censoring, c_D(p, q), connecting to the FIM sibling paper. Optional but distinctive.
**NEW-S4.** Title: with v4 the arresting candidate is along the lines of "Safe to Simplify: Consequence and Detectability for Common-Shape Weibull Series Systems under Masked Data". Decide at rework time (prior MAJ-8 remains open).

## Prior findings still open (2026-05-03 review; draft unchanged since 2026-02-28)

- CRIT-1 stale ecosystem citations (towell2023reliability -> towell2025masked, DOI 10.5281/zenodo.18725577; add towell2025weibull-fim): **open**, confirmed in working-tree refs.bib and all five cite-points.
- MAJ-1 alignment observed but not derived: **open**; v4 + notes/ now contain the derivation plan and verified constants (this is the rework's Section 4.5).
- MAJ-2 single-baseline limitation: **open**; partially mitigated by the planned derivation (constants become formulas evaluable at any design point) plus appendix factor sweeps.
- MAJ-3 MSE surprise undersold: **open**; superseded and sharpened by NEW-M1/NEW-M5 (now a provable proposition plus confirmatory vanishing).
- MAJ-4 adaptive procedure framed as invention: **open** in draft; v4 reframes as pretest-estimator evaluation (see prior-art.md: Bancroft 1944, Judge-Bock 1978).
- MAJ-5 Related Work thin, 9 bib entries uncited: **open**, verified (lawless2003, meeker1998, Lin-1996, Usher-1996, Amma-2001, Amma-2004, Zhibi-2005, Zhibi-2007, burnham2002 all unused).
- MAJ-6 AIC/BIC-adaptive comparators absent from the strategy comparison: **open**.
- MAJ-7 qrei/ build artifacts not gitignored: **open**, re-verified (git check-ignore fails on qrei/manuscript.aux).
- MAJ-8 neutral title: **open** (see NEW-S4).

## Novelty assessment (grounded in prior-art.md)

Five threats ranked there; net position is favorable if the paper does the engagement work:

1. **FIC (Claeskens-Hjort 2003/2006/2008): highest risk, must be engaged in Section 4.5.** FIC selects on estimated MSE of a focus parameter (MTTF is exactly such a focus) under LOCAL O(1/sqrt(n)) misspecification. Differentiators: this paper treats fixed, n-independent misspecification bias; FIC has never been applied to Weibull series or masked data; the zero-first-order-gain proposition is a structural zero, stronger than FIC's small-number comparisons. The referee question "why not just apply FIC to MTTF?" needs an explicit answer in the paper: the proposition implies FIC would select the full model essentially everywhere, agreeing with our recommendation by a different route, while our closed-form bias and power formulas serve the engineering decision directly at fixed n.
2. **Pretest estimation (Bancroft 1944; Judge-Bock 1978; Danilov-Magnus 2004; Leeb-Potscher 2003/2005): owns the Section 5 risk hump.** The n = 100 hump is the classical pretest phenomenon. Cite and frame Section 5 as confirmation of pretest theory in the masked Weibull setting with quantitative calibration, which no pretest work covers.
3. **McCool (1975, 1979): closest prior art on testing equal Weibull shapes** (multi-sample, no masking, no consequence analysis). Must cite as the starting point.
4. **Hart (2024/2025, IEEE TR): benign venue competitor.** Formalizes estimation assuming common shape; no misspecification, masking, or selection. Cite as motivation; corroborates IEEE TR topical fit.
5. **Pascual (2005): cross-family Weibull misspecification bias precedent;** distinguish within-family constraint case.

**Genuinely novel after the survey:** the consequence-vs-detectability decoupling under fixed misspecification in the masked series-system setting; the zero-first-order-gain proposition (no prior derivation found of an exact structural zero for the common-shape constraint on system-level functionals); the calibrated safe-zone constants under masking/censoring. The 18 BibTeX entries in prior-art.md cover every citation slot the rework needs.

## Verified-numbers ledger (this session)

| Claim (location) | Status |
|---|---|
| Property 1 closure formula lambda_s = (sum lambda_j^-k)^(-1/k) (`paper.tex:103`) | correct |
| Eq. (3) algebra: sum_{j in C} (h_j/h) f = R sum_{j in C} h_j (`paper.tex:93`) | correct given C1-C2-C3 (see NEW-C1) |
| chi2 df = m-1 = 4 (`paper.tex:194`) | correct, interior null |
| Type I 4.6-6.8% (`paper.tex:198`) | matches data (0.046-0.068); all within MC noise of 5% |
| Power table values (`paper.tex:202-218`) | match data |
| Bias < 1% through CV ~ 14% at n >= 500; 1.5% at CV ~ 20.5% (`paper.tex:171`) | matches data |
| Bias largely n-independent: +3.2% -> +2.6% at CV ~ 27% (`paper.tex:171`) | matches data (3.22 -> 2.59) |
| Full lower MSE at n <= 1000, CV = 0 (`paper.tex:175`) | supported; marginal per-dataset at n = 500/1000, replicated across datasets; gone at n = 5000 (report it) |
| Adaptive within 2.5% of always-full at n >= 500 (`paper.tex:286`) | exact max 2.38%; table rounding obscures (NEW-m4) |
| n = 100 overhead 8-18% (`paper.tex:286`) | exact 5.8-17.7% (NEW-m5) |
| Selection rate > 90% at low CV (`paper.tex:286`) | matches (89-95%) |
| Masking 6x, censoring 2.5x, components 5x power effects (Table 4) | 48->8 (6x), 17->43 (2.5x), 77->16 (4.8x): ok |
| AIC 8.2-12.4%, BIC <= 0.2% (`paper.tex:336`) | rates match; mechanism wrong (NEW-M3) |
| ncp ~ 0.5 n CV^2; CV50 ~ 3.5/sqrt(n) (new, for Section 4/4.5) | verified, ledger in notes/verify-thesis-claims.py output |

## Prose assessment

The condensed draft is well written: the abstract leads with the real question, sections are short and load-bearing, and the condensation mostly tightened the paper (the cut roadmap paragraph and model-hierarchy table are not missed at 11pp, though the "Goldilocks" physical argument for common-shape vs common-scale was a real loss and could return in one sentence). Three prose-level concerns: (1) "The existing literature on this question focuses almost entirely on whether a likelihood ratio test can detect the difference between models [towell2023reliability]" attributes the strawman to a single self-citation; rewrite to characterize the actual literature (estimation-focused: Usher, Lin-Guess, Sarhan, Tan; selection-adjacent: Craiu-Lee, McCool) and then pose the consequence question as new. (2) The "This is the wrong question. The right question is..." rhetoric works, but only if the related-work characterization underneath it is accurate (see (1)). (3) The Conclusion's first two paragraphs restate the Contributions nearly verbatim; with Section 4.5 added, the conclusion should instead state the decoupling formula, the proposition, and the two-regime guidance. Notation: CV vs CV_k drift, MTTF units (hours? cycles?) never stated, variance-vs-MSE wobble (NEW-M5).

## Prioritized rework checklist (mapped to thesis v4)

1. **Section 4.5 Theoretical Justification** (v4 pillar i+ii): delta-method bias = c_B CV^2 + population KL-projection curve (fixes NEW-M4); Le Cam ncp = c_D n CV^2 with empirical c_D = 0.50 +/- 0.03 and CV50 ~ 3.5/sqrt(n) (NEW-S1); two-regime safety statement replacing unqualified claims (NEW-M2). Engage FIC here (novelty threat 1).
2. **Zero-first-order-gain Proposition** (v4 pillar iii): statement in Section 3.3 or 4.5, complete-data proof in appendix, masked-case remark; replaces the White-1982 mechanism sentence (NEW-M1); cite Aitchison-Silvey 1958. Run papermill:proof for the masked-data extension.
3. **MSE evidence upgrade** (v4 pillar iii): extend Table 3 to n = 5000, paired-test significance, variance/bias-squared decomposition (NEW-M5); add MC SEs globally (NEW-m3).
4. **Assumptions fix** (NEW-C1): state C1-C2-C3; cite towell2025masked.
5. **Citation hygiene** (prior CRIT-1 + prior-art): swap towell2023reliability -> towell2025masked, add towell2025weibull-fim, paste the 18 prior-art entries, expand Related Work with the FIC/pretest/McCool/Hart positioning paragraph (prior MAJ-5).
6. **Section 5 reframe** (v4 pillar ii): pretest-estimator evaluation with Bancroft/Judge-Bock framing; add AIC/BIC-adaptive comparators (prior MAJ-4, MAJ-6).
7. **Smaller fixes:** AIC mechanism sentence (NEW-M3), uniqueness characterization (NEW-M6), R(t) results (NEW-M7), units/rounding/CV-labeling (NEW-m4-m7), optimizer + filtering disclosure (NEW-m1, NEW-m2), package availability (NEW-m8), Wilks caveat (NEW-m9), qrei gitignore (prior MAJ-7), title (NEW-S4/prior MAJ-8).
8. **Repo hygiene:** commit the working tree before the rework starts; the only real draft currently exists as uncommitted changes plus stale HEAD.

## Venue note

Prior review recommended staying with QREI; state.md switched primary to IEEE TR on the strength of the planned structural derivation. This review supports IEEE TR conditional on executing items 1-3 above. Hart (2024/2025) in IEEE TR demonstrates the venue currently publishes common-shape Weibull competing-risks work. Without the derivation, fall back to QREI.

## Severity counts (new findings only)

Critical 1, Major 7, Minor 9, Suggestions 4. Prior review items re-verified still open: 1 critical, 8 major.
