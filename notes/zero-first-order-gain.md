# Zero First-Order Gain Proposition

**Date:** 2026-06-10 (thesis verification session)
**Status:** derivation sketch for complete data (exact); masked/censored case
conjectured and empirically supported; needs write-up as Proposition in the
planned theory section.
**Verification:** `notes/verify-zero-gain.py` (FIM projection, three scale
configurations), plus the n=5000 variance equality in
`results/consequence/data-consequence.csv` (VarF = VarR = 8.4 at CV=0).

## Statement

Let a series system have independent Weibull components, evaluated at a
*common-shape* parameter point (k_1 = ... = k_m = k, arbitrary scales).
Consider any smooth functional g of the **system lifetime distribution**
(system MTTF, R(t) at fixed t, quantiles). Then the asymptotic variance of
the MLE plug-in estimate of g is **identical** under the full model
(2m parameters) and the common-shape model (m+1 parameters):

> Imposing the (true) common-shape constraint yields exactly **zero
> first-order efficiency gain** for system-level prediction, at any scale
> configuration, not just exchangeable ones.

Consequence: the finite-n MSE ordering between the two models is decided by
*second-order* effects, and the simulations show these favor the **full**
model (paired t = -3.65 at n=100; replicated in the independent adaptive
dataset; effect vanishes by n=5000 exactly as first-order theory requires).
"Parsimony reduces variance" fails for system-level prediction here: the
reduced model's only first-order advantage is nil, and its finite-sample
behavior is strictly worse.

## Derivation sketch (complete data)

Reparameterize component j as (k_j, eta_j) with eta_j = lambda_j^{-k_j}, so
the component cumulative hazard is eta_j t^{k_j} and the system cumulative
hazard is H(t) = sum_l eta_l t^{k_l}.

**Gradient structure.** Any functional g of the system distribution depends
on theta only through H(.). At a common-k point, for any such g:

- dg/dk_j = eta_j * c_k   (one scalar c_k common to all j)
- dg/deta_j = c_eta       (one scalar c_eta common to all j)

i.e. grad g = (c_k * eta, c_eta * 1). [Check for MTTF = Gamma(1+1/k) s^{-1/k},
s = sum eta_j: dg/dk_j = -eta_j * int t^k ln t e^{-s t^k} dt, dg/deta_j =
-int t^k e^{-s t^k} dt.]

**FIM structure.** With complete data (T, J), at a common-k point J is
independent of T with P(J=j) = eta_j / s. Writing A = 1/k + ln T,
B = T^k ln T, C = T^k, the score components are

- dl/dk_j   = 1{J=j} A - eta_j B
- dl/deta_j = 1{J=j}/eta_j - C

and direct computation of E[score outer products] gives the blocks

- I_kk      = (E[A^2]/s) diag(eta) + (E[B^2] - 2E[AB]/s) eta eta'
- I_k,eta   = (E[A]/s) I_m + (E[BC] - (E[AC]+E[B])/s) eta 1'
- I_eta,eta = diag(1/(s eta_j)) + (E[C^2] - 2E[C]/s) 1 1'

**Projection identity.** The reduced model's tangent space (embedded in the
full space) is V = {v : k-block of v has equal entries}. The first-order
variance gap for g is zero iff Sigma * grad g is in V, equivalently
grad g is in I(V). Take v = (a 1, gamma eta) in V. Using the block structure:

- (I v)_k-block   = [a c1 + gamma(alpha + beta s)] * eta   (proportional to eta)
- (I v)_eta-block = [a alpha + a beta s + gamma/s + ...] * 1 (constant)

Matching (c_k eta, c_eta 1) gives two linear equations in (a, gamma),
generically solvable. Hence grad g lies in I(V) **exactly**, for any eta. QED
(complete data).

**Numerical confirmation** (complete-data FIM via 4e5 MC score outer
products, k=1.18): relative first-order gap

| scales | rel. variance gap |
|---|---|
| (900 x5) exchangeable | 1.5e-05 |
| baseline (994.37, 908.95, 840.11, 940.13, 923.16) | 9.7e-06 |
| strongly unequal (1500, 1200, 900, 600, 300) | 2.2e-05 |

All at MC noise level: gap is approximately 0.

## Masked/censored case (conjecture)

Under C1-C2-C3 masking, the failure-observation likelihood term is
log(sum_{j in C} h_j(t)) + log R(t); at common k, sum_{j in C} h_j(t) =
k t^{k-1} sum_{j in C} eta_j, so candidate sets enter only through
eta-sums and the same (alpha I + beta eta 1') block structure plausibly
survives with masking-moment coefficients; censored terms involve only the
symmetric system R(t). Empirical support: simulated VarF = VarR at n=5000
under p=0.215, q=0.825. Proof to be completed in the theory-section rework
(papermill:proof task).

## Why the full model wins at finite n (informal)

The pooled common-shape error is *coherent* across components: one shape
error hits all m cumulative hazards in the same direction, and then passes
through the nonlinear lambda_s(k) = (sum eta_j)^{-1/k} and Gamma(1+1/k)
maps. The full model's m shape errors are imperfectly correlated and
partially diversify inside the system functional. First-order these wash
out (proposition above); second-order the coherent error costs more.
Empirical decomposition at CV=0, n=100: VarR = 417 > VarF = 348 while
Bias^2_R = 0.6 < Bias^2_F = 14.1. The gap is variance-driven, and net MSE
favors the full model.
