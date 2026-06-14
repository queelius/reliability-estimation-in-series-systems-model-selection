"""Verification for the conjugacy lemma and its three corollaries under the
paper's actual observation design: masked causes (Bernoulli C1-C2-C3,
p = 0.215) and right censoring (tau = 0.825 system quantile).

Check 1 (Proposition, masked+censored): at a common-shape point, the
  first-order variance reduction from the common-shape constraint is zero
  for system functionals (MTTF, R(t)). Uses MC estimate of the
  observed-data FIM via score outer products in (k, lambda) coordinates.

Check 2 (LRT noncentrality constant): theoretical ncp per observation,
  (H d)' (H Sigma H')^{-1} (H d) with d the simulation's shape-contrast
  direction, divided by CV^2; compare with the empirical
  c_D = 0.50 +/- 0.03 recovered from the divergence simulations.

Check 3 (Quadratic bias corollary): population KL projection. Computes the
  pseudo-true reduced parameters by maximizing the expected masked/censored
  reduced log-likelihood under the true heterogeneous-shape model
  (deterministic numerical integration, no Monte Carlo), then the relative
  MTTF bias B(CV). Verifies the linear term vanishes and extracts the
  quadratic coefficient c_B for comparison with the simulated 0.30-0.35.
  Writes the population bias curve to results/consequence/figure/
  population_bias.csv for the paper figure.

Run from the repo root: python3 notes/verify-masked-zero-gain.py
"""
import numpy as np
from scipy import integrate, optimize, special
import os

rng = np.random.default_rng(20260612)

m = 5
K0 = 1.18
SCALES = np.array([994.37, 908.95, 840.11, 940.13, 923.16])
P_MASK = 0.215
Q_CENS = 0.825

# ----------------------------------------------------------------- utilities
def system_reliability(t, k, lam):
    t = np.atleast_1d(t)
    return np.exp(-np.sum((t[:, None] / lam) ** k, axis=1))

def system_mttf(k, lam):
    f = lambda t: np.exp(-np.sum((t / lam) ** k))
    val, _ = integrate.quad(f, 0, np.inf, limit=300)
    return val

def system_quantile(q, k, lam):
    f = lambda t: system_reliability(t, k, lam)[0] - (1 - q)
    return optimize.brentq(f, 1e-6, 1e7)

def generate_shapes_with_cv(target_cv, mean_k=K0, mm=m):
    """Replicates results/sim_utils.R generate_shapes_with_cv."""
    if target_cv < 0.001:
        return np.full(mm, mean_k)
    half_range = target_cv * mean_k * np.sqrt(3)
    return np.linspace(mean_k - half_range, mean_k + half_range, mm)

def actual_cv(shapes):
    return np.std(shapes, ddof=1) / np.mean(shapes)

# ------------------------------------------------- check 1 and 2: masked FIM
def simulate_scores(N, k, lam, p, tau, batch=250_000):
    """MC scores of the observed-data (masked, censored) likelihood at theta,
    in (k_1..k_m, lam_1..lam_m) coordinates. Returns (2m x 2m) FIM estimate."""
    k = np.asarray(k, float); lam = np.asarray(lam, float)
    S = np.zeros((2 * m, 2 * m))
    done = 0
    while done < N:
        n = min(batch, N - done)
        X = lam * rng.weibull(k, size=(n, m))
        Tsys = X.min(axis=1)
        Kc = X.argmin(axis=1)
        delta = Tsys <= tau
        T = np.where(delta, Tsys, tau)
        # candidate sets: cause always in; others independently w.p. p
        Cm = rng.random((n, m)) < p
        Cm[np.arange(n), Kc] = True
        Cm[~delta] = False
        # pieces
        U = T[:, None] / lam                      # (n, m)
        H = U ** k                                # cumulative hazards (t/lam)^k
        lnU = np.log(U)
        h = (k / lam) * U ** (k - 1)              # hazards
        hC = np.where(Cm, h, 0.0).sum(axis=1)     # sum_{l in C} h_l
        hC = np.where(delta, hC, 1.0)             # avoid div by zero for censored
        dl_dk = np.where(Cm, h * (1.0 / k + lnU), 0.0) / hC[:, None] \
                - H * lnU                          # (n, m)
        dl_dlam = np.where(Cm, -(k / lam) * h, 0.0) / hC[:, None] \
                  + (k / lam) * H
        sc = np.concatenate([dl_dk, dl_dlam], axis=1)
        S += sc.T @ sc
        done += n
    return S / N

def loglik_obs(theta, t, delta, cand):
    """Per-observation loglik for the score sanity check."""
    kk, ll = theta[:m], theta[m:]
    Hc = np.sum((t / ll) ** kk)
    out = -Hc
    if delta:
        hh = (kk / ll) * (t / ll) ** (kk - 1)
        out += np.log(np.sum(hh[cand]))
    return out

def sanity_check_scores(k, lam, p, tau):
    """Compare analytic scores to numerical gradients on random observations."""
    worst = 0.0
    for _ in range(25):
        X = lam * rng.weibull(k, size=m)
        t = min(X.min(), tau); delta = X.min() <= tau
        cand = rng.random(m) < p
        cand[X.argmin()] = True
        if not delta:
            cand[:] = False
        theta = np.concatenate([k, lam]).astype(float)
        # analytic
        U = t / lam; H = U ** k; lnU = np.log(U)
        h = (k / lam) * U ** (k - 1)
        hC = np.sum(h[cand]) if delta else 1.0
        a_k = (np.where(cand, h * (1 / k + lnU), 0.0) / hC if delta else 0.0) - H * lnU
        a_l = (np.where(cand, -(k / lam) * h, 0.0) / hC if delta else 0.0) + (k / lam) * H
        ana = np.concatenate([np.atleast_1d(a_k) * 1.0, np.atleast_1d(a_l) * 1.0])
        # numerical
        num = np.zeros(2 * m)
        for i in range(2 * m):
            e = np.zeros(2 * m); e[i] = 1e-6 * max(1.0, abs(theta[i]))
            num[i] = (loglik_obs(theta + e, t, delta, cand)
                      - loglik_obs(theta - e, t, delta, cand)) / (2 * e[i])
        worst = max(worst, np.max(np.abs(ana - num) / (1e-8 + np.abs(num) + 1e-3)))
    return worst

def grad_mttf(k, lam, eps=1e-6):
    g = np.zeros(2 * m)
    th0 = np.concatenate([k, lam]).astype(float)
    for i in range(2 * m):
        a = th0.copy(); b = th0.copy()
        a[i] += eps * max(1, abs(th0[i])); b[i] -= eps * max(1, abs(th0[i]))
        g[i] = (system_mttf(a[:m], a[m:]) - system_mttf(b[:m], b[m:])) / (a[i] - b[i])
    return g

def grad_R(t, k, lam, eps=1e-6):
    g = np.zeros(2 * m)
    th0 = np.concatenate([k, lam]).astype(float)
    for i in range(2 * m):
        a = th0.copy(); b = th0.copy()
        a[i] += eps * max(1, abs(th0[i])); b[i] -= eps * max(1, abs(th0[i]))
        g[i] = (system_reliability(t, a[:m], a[m:])[0]
                - system_reliability(t, b[:m], b[m:])[0]) / (a[i] - b[i])
    return g

def contrast_matrix():
    Hm = np.zeros((m - 1, 2 * m))
    for r in range(m - 1):
        Hm[r, r] = 1.0; Hm[r, r + 1] = -1.0
    return Hm

# ------------------------------------------------------ check 3: KL projection
def expected_reduced_loglik_factory(k0, lam0, p, tau, ngrid=12000):
    """Expected per-observation reduced loglik under truth (k0, lam0) with
    Bernoulli masking and censoring at tau. Deterministic integration."""
    t = np.linspace(1e-9, tau, ngrid)
    U0 = t[:, None] / lam0
    H0 = U0 ** k0
    R0 = np.exp(-H0.sum(axis=1))
    h0 = (k0 / lam0) * U0 ** (k0 - 1)            # (T, m) cause hazards
    # subsets of the OTHER components per cause j: 2^(m-1) masks with probs
    others = [[l for l in range(m) if l != j] for j in range(m)]
    subsets, probs = [], []
    for j in range(m):
        Sj, Pj = [], []
        for code in range(2 ** (m - 1)):
            mask = np.zeros(m, bool); mask[j] = True
            nin = 0
            for bi, l in enumerate(others[j]):
                if (code >> bi) & 1:
                    mask[l] = True; nin += 1
            Sj.append(mask)
            Pj.append(p ** nin * (1 - p) ** (m - 1 - nin))
        subsets.append(np.array(Sj))             # (2^(m-1), m)
        probs.append(np.array(Pj))
    Rtau = float(system_reliability(np.array([tau]), k0, lam0)[0])

    def negE(theta_R):
        kap = theta_R[0]; lamR = theta_R[1:]
        UR = t[:, None] / lamR
        hR = (kap / lamR) * UR ** (kap - 1)      # (T, m)
        HRsum = (UR ** kap).sum(axis=1)
        val = 0.0
        for j in range(m):
            wj = h0[:, j] * R0                    # density of (t, cause j)
            inner = np.zeros_like(t)
            for mask, pr in zip(subsets[j], probs[j]):
                inner += pr * np.log(hR[:, mask].sum(axis=1))
            val += np.trapezoid(wj * (inner - HRsum), t)
        val += Rtau * (-np.sum((tau / lamR) ** kap))   # censored term
        return -val

    return negE

def pseudo_true_bias(k_true, lam_true, p, tau_q):
    """Relative MTTF bias of the KL-projected reduced model."""
    tau = system_quantile(tau_q, k_true, lam_true)
    negE = expected_reduced_loglik_factory(k_true, lam_true, p, tau)
    x0 = np.concatenate([[k_true.mean()], lam_true])
    res = optimize.minimize(negE, x0, method="Nelder-Mead",
                            options={"xatol": 1e-8, "fatol": 1e-12,
                                     "maxiter": 40000, "maxfev": 40000})
    res = optimize.minimize(negE, res.x, method="Nelder-Mead",
                            options={"xatol": 1e-9, "fatol": 1e-13,
                                     "maxiter": 40000, "maxfev": 40000})
    kap, lamR = res.x[0], res.x[1:]
    mttf_R = special.gamma(1 + 1 / kap) * np.sum(lamR ** (-kap)) ** (-1 / kap)
    mttf_T = system_mttf(k_true, lam_true)
    return (mttf_R - mttf_T) / mttf_T, res.x

# ================================================================== run
if __name__ == "__main__":
    k_common = np.full(m, K0)
    tau0 = system_quantile(Q_CENS, k_common, SCALES)
    print(f"Common-shape point: k={K0} x{m}, scales=baseline, "
          f"p={P_MASK}, tau={tau0:.1f} (q={Q_CENS})")

    err = sanity_check_scores(k_common, SCALES, P_MASK, tau0)
    print(f"\n[scores] worst rel. deviation analytic vs numerical: {err:.2e}")

    print("\n[FIM] simulating 2,000,000 masked/censored observations ...")
    I = simulate_scores(2_000_000, k_common, SCALES, P_MASK, tau0)
    Sg = np.linalg.inv(I)
    Hm = contrast_matrix()
    HSH = Hm @ Sg @ Hm.T

    print("\nCHECK 1: zero first-order gain under masking + censoring")
    mttf0 = system_mttf(k_common, SCALES)
    for name, dg in [("MTTF", grad_mttf(k_common, SCALES)),
                     ("R(MTTF)", grad_R(mttf0, k_common, SCALES)),
                     ("R(2 MTTF)", grad_R(2 * mttf0, k_common, SCALES))]:
        varF = dg @ Sg @ dg
        A = Hm @ Sg @ dg
        gap = A @ np.linalg.solve(HSH, A)
        print(f"  g = {name:10s}: varF = {varF:.4e}, "
              f"first-order reduction = {gap:.3e}, rel = {gap/varF:.2e}")

    print("\nCHECK 2: theoretical LRT noncentrality constant c_D")
    print("  (empirical from divergence sims: 0.50 +/- 0.03 for n >= 1000)")
    for tcv in [0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20]:
        kk = generate_shapes_with_cv(tcv)
        acv = actual_cv(kk)
        d = np.concatenate([kk - K0, np.zeros(m)])
        ncp1 = (Hm @ d) @ np.linalg.solve(HSH, Hm @ d)   # per observation
        print(f"  target CV {tcv:.2f} (actual {acv*100:5.2f}%): "
              f"c_D = ncp/(n CV^2) = {ncp1/acv**2:.3f}")

    print("\nCHECK 3: population KL-projection bias (deterministic)")
    rows = []
    for tcv in [0.0, 0.01, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20, 0.30]:
        kk = generate_shapes_with_cv(tcv)
        acv = actual_cv(kk) if tcv > 0 else 0.0
        B, _ = pseudo_true_bias(kk, SCALES, P_MASK, Q_CENS)
        cB = B / acv ** 2 if acv > 0 else np.nan
        rows.append((tcv, acv, B))
        print(f"  target CV {tcv:.2f} (actual {acv*100:5.2f}%): "
              f"pop. bias = {B*100:+.3f}%   B/CV^2 = {cB:.3f}" if acv > 0 else
              f"  target CV {tcv:.2f} (actual  0.00%): pop. bias = {B*100:+.3f}%")
    # linear-term check: reversed direction at small CV
    for tcv in [0.02, 0.04]:
        kk = generate_shapes_with_cv(tcv)[::-1].copy()   # reversed assignment
        acv = actual_cv(kk)
        B, _ = pseudo_true_bias(kk, SCALES, P_MASK, Q_CENS)
        print(f"  reversed direction, target CV {tcv:.2f}: pop. bias = {B*100:+.3f}%"
              f"   (forward gave {dict((r[0], r[2]) for r in rows)[tcv]*100:+.3f}%)")

    out = "results/consequence/figure/population_bias.csv"
    if os.path.isdir(os.path.dirname(out)):
        with open(out, "w") as fh:
            fh.write("target_cv,actual_cv,pop_bias\n")
            for tcv, acv, B in rows:
                fh.write(f"{tcv},{acv},{B}\n")
        print(f"\npopulation bias curve written to {out}")
