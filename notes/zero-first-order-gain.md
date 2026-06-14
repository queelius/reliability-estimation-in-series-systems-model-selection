# The Common-Shape Conjugacy Identity

**Date:** 2026-06-10, completed 2026-06-14 (thesis verification + proof phase)
**Status:** complete-data case proved in closed form for general m and general
scales; masked/censored case reduced to four structural proportionalities
(P1)-(P4) that are verified numerically to Monte Carlo precision. Both
corollaries (zero variance gain, zero linear bias) follow from one identity.
**Verification:** `notes/verify-zero-gain.py` (complete-data FIM projection,
three scale configs), `notes/verify-masked-zero-gain.py` (masked+censored FIM
projection, ncp constant, population KL bias curve), and
`notes/verify-structural-lemma.py` ((P1)-(P4) and gradient structure for both
complete and masked data, in (k, eta) coordinates).

## The single identity

Work in the parameterization (k_1,...,k_m, eta_1,...,eta_m) with
eta_l = lambda_l^{-k_l}, so the component cumulative hazard is eta_l t^{k_l}
and the system cumulative hazard is H(t) = sum_l eta_l t^{k_l}. Fix a
common-shape point theta_0 with k_1 = ... = k_m = k and arbitrary scales
(arbitrary eta). Let V = {v : the k-block of v is constant across components}
be the reduced model's tangent space (embedded in the full 2m-dim space), and
let I be the Fisher information at theta_0. For a smooth functional g of the
system lifetime distribution (system MTTF, R(t) at fixed t, a quantile),

> **Conjugacy Identity.**  I^{-1} grad g  lies in V.
> Equivalently, the k-block of I^{-1} grad g is constant across components.

Everything below is a corollary. The name "conjugacy" is because the identity
says grad g is I-conjugate to the constraint directions (the shape contrasts):
grad g' I^{-1} A' = 0, where A is the (m-1) x 2m contrast operator on the
k-block whose rows are the constraints k_l - k_{l+1} = 0.

## Why it holds: the 2D closure

Two structural facts, both at the common-shape point.

**Gradient structure (exact).** Because g depends on theta only through the
system law, and at common k the system cumulative hazard is H(t) = s t^k with
s = sum_l eta_l, g depends on eta only through the sum s. Hence

- d g / d eta_l = g'(s), the SAME scalar for every l, so grad_eta g = c_eta * 1;
- d H(t) / d k_l = eta_l t^k ln t at common k, so d g / d k_l = eta_l * c_k,
  i.e. grad_k g = c_k * eta.

So grad g = (c_eta * 1, c_k * eta) lies in the 2D space
P = span{(1, 0), (0, eta)}. Verified to machine precision (residuals 1e-10)
in verify-structural-lemma.py for MTTF and R(MTTF), complete and masked.

**Fisher information structure (closed form for complete data).** With
W = T^k ~ Exponential(s) and failed component J independent of W with
P(J=l) = eta_l / s, the complete-data score at theta_0 is

- dl/d eta_l   = 1{l=J}/eta_l - t^k
- dl/d k_l     = (1/k)[ (1 + ln W) 1{l=J} - eta_l W ln W ]

and taking expectations of score outer products gives blocks

- I_{eta,eta} = (1/s) diag(1/eta)                            (diagonal)
- I_{eta,k}   = (1/k)[ c1 I_m + kappa * 1 eta' ],   c1 = (1+E ln W)/s
- I_{k,k}     = (1/k^2)[ (e2/s) diag(eta) + psi * eta eta' ]

with scalar moment constants c1, kappa, e2, psi (functions of s only). The
load-bearing consequence is that I maps the 2D space
U = span{(eta, 0), (0, 1)} into P:

- (P1) I_{eta,eta} eta = (1/s) 1                  proportional to 1
- (P2) I_{k,eta}   eta = (1/k)(c1 + kappa s) eta  proportional to eta
- (P3) I_{eta,k}   1   = (1/k)(c1 + kappa s) 1    proportional to 1
- (P4) I_{k,k}     1   = (1/k^2)(e2/s + psi s) eta proportional to eta

**Closure.** (P1)-(P4) say I : U -> P. Since both are 2-dimensional and I is
invertible, I : U -> P is a bijection, so I^{-1} : P -> U. As grad g in P, we
get I^{-1} grad g in U, and every vector in U has a constant k-block. That is
the Conjugacy Identity. QED for complete data, general m, general scales.

Concretely, solving I v = grad g with the ansatz v = (b eta, a 1) in U reduces
to a 2x2 linear system in (a, b); it is solvable whenever the scalar
D = (e2/s + psi s) - s (c1 + kappa s)^2 is nonzero (equivalently I is
nonsingular on the relevant subspace). The unique solution has k-block a 1,
constant. See verify-zero-gain.py: relative residual of the gain term is
~1e-5 for scales (900 x5), baseline, and (1500,1200,900,600,300).

## Masked and censored data

The gradient structure is unchanged (g is still a functional of the system
law). The FIM blocks change: under C1-C2-C3 masking the failure term is
log R(t) + log sum_{l in C} h_l(t), and at common shape
sum_{l in C} h_l(t) = k t^{k-1} sum_{l in C} eta_l, so candidate sets enter
through eta-sums; censored observations contribute only the symmetric
log R(tau). The masked FIM is not block-diagonal in the same way, but the only
thing the proof needs is (P1)-(P4). These are verified to Monte Carlo
precision for the paper's design (p = 0.215, q = 0.825, m = 5, 3,000,000
simulated observations) in verify-structural-lemma.py:

| proportionality | complete resid | masked+censored resid |
|---|---|---|
| (P1) I_ee eta ~ 1   | 1.5e-3 | 5.3e-4 |
| (P2) I_ke eta ~ eta | 1.7e-3 | 4.8e-4 |
| (P3) I_ek 1   ~ 1   | 1.4e-3 | 4.2e-4 |
| (P4) I_kk 1   ~ eta | 1.6e-3 | 3.6e-4 |

(residuals at the sqrt(N) Monte Carlo floor). End-to-end, the relative
first-order variance gain for MTTF and R(t) is below 1e-5 in every
configuration tested, complete and masked. So the Conjugacy Identity, hence
both corollaries below, holds in the paper's masked, censored setting. A fully
analytic masked-case proof reduces to showing (P1)-(P4) survive the
candidate-set averaging; this is left as a remark, consistent with the
program's verify-to-0.5% precedent.

## Corollary 1: zero first-order efficiency gain (the MSE result)

By Aitchison and Silvey (1958), imposing a true constraint a(theta) = 0 (here
the m-1 shape contrasts, Jacobian A) changes the constrained-MLE asymptotic
variance of g from var_F = grad g' I^{-1} grad g to

  var_R = var_F - grad g' I^{-1} A' (A I^{-1} A')^{-1} A I^{-1} grad g.

The subtracted gain term vanishes iff A I^{-1} grad g = 0, i.e. iff
I^{-1} grad g in ker A = V. That is exactly the Conjugacy Identity. So

> imposing the (true) common-shape constraint yields **exactly zero**
> first-order variance reduction for any system-level functional, at any
> scale configuration.

Equivalently: the unconstrained MLE of the shape contrasts is asymptotically
uncorrelated with the unconstrained MLE of any system functional. Parsimony
buys no first-order efficiency for system-level prediction. The finite-n MSE
ordering is therefore decided at second order, and the simulations show it
favors the FULL model: at CV = 0, paired t = -3.65 (n=100), replicated in the
adaptive dataset (t = -4.82, -3.07, -2.32), vanishing at n = 5000 (t = +0.24)
as first-order theory requires. Decomposition at n=100: Var_R = 417 >
Var_F = 348 while Bias^2 favors the reduced model (0.6 vs 14.1). The effect is
variance-driven and is the coherent-vs-diversified shape-error story: the
pooled common-shape error hits all m cumulative hazards in the same direction,
where the full model's m shape errors partially diversify inside the system
functional.

## Corollary 2: the misspecification bias is O(CV^2), no linear term

Let the true shapes be k_l = kbar + delta_l with sum delta_l = 0, so the shape
CV is proportional to ||delta||. The reduced model's pseudo-true parameter
theta_R*(delta) is the KL projection of the truth onto the reduced family V.
The system-MTTF misspecification bias is B(delta) = g(theta_R*(delta)) -
g(theta_true(delta)). At delta = 0 the truth lies in V, so B(0) = 0 and
theta_R*(0) = theta_true(0).

To first order, KL projection gives theta_R*(delta) - theta_0 =
P_V^I(delta_full), the I-orthogonal projection of the full-space shift
delta_full = (delta, 0) onto V (minimizer of the leading quadratic KL form
(1/2)(theta_R - theta_true)' I (theta_R - theta_true) over V). Hence, writing
r = P_V^I e_{k_j} - e_{k_j} (which satisfies r perp_I V, i.e. r' I v = 0 for
all v in V),

  dB/d delta_j |_0 = grad g . P_V^I e_{k_j} - grad g . e_{k_j} = grad g . r.

Now use the Conjugacy Identity I^{-1} grad g in V:

  grad g . r = (I (I^{-1} grad g)) . r = (I^{-1} grad g)' I r = 0,

because r perp_I V and I^{-1} grad g in V. So **dB/d delta = 0**: the linear
term of the misspecification bias vanishes, and B(delta) = O(||delta||^2) =
O(CV^2). The same identity that kills the variance gain kills the linear bias.

Verification (verify-masked-zero-gain.py, population KL projection, fully
deterministic, masked + censored): bias at CV = 0 is -0.001% (zero); forward
and reversed shape directions give identical bias (+0.018% both at CV 2.74%),
confirming B is even in delta; and B / CV^2 = 0.21 to 0.28 through CV ~ 14%,
agreeing with the n = 5000 simulation (which gives the leading coefficient
c_B ~ 0.30-0.35). The deterministic projection becomes numerically unstable
above CV ~ 27% (optimizer divergence); the quadratic law is asserted only in
the engineering-relevant regime CV < ~20%, where it matches simulation.

## Corollary 3 (empirical, not from the identity): detection scales as n CV^2

Separately, the LRT noncentrality parameter under local shape heterogeneity is
ncp = (H delta)' (A I^{-1} A')^{-1} (H delta) per the standard Le Cam local
power expansion, scaling as c_D * n * CV^2. The theoretical per-observation
constant evaluated at the paper's design is c_D = 0.487 (verify-masked-
zero-gain.py, Check 2), matching the empirical c_D = 0.50 +/- 0.03 recovered
from the divergence simulations across n in [1000, 10000]. Hence the
detectable threshold is CV50 ~ 3.5/sqrt(n) (empirical log-log slope -0.468 vs
the theoretical -0.5). This is the detectability half of the decoupling; it is
governed by the SAME A I^{-1} A' that appears in Corollary 1, which is why the
two phenomena share the constant-k-block geometry but scale differently in n
(bias is an n-free population quantity; detection accumulates with n).

## The decoupling, in one sentence

At a common-shape point, system-level prediction sees the shape constraint as
invisible to first order (Conjugacy Identity), so misspecification bias is
second-order in heterogeneity (O(CV^2), n-free) and the common-shape
constraint provides zero variance gain; meanwhile the likelihood sees the
shape contrasts directly, so detection accumulates as n CV^2. Bias and
detectability are decoupled in n and coupled only through the shared shape
geometry.
