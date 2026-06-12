"""Check: at a common-shape point, does the constrained-MLE projection reduce
the asymptotic variance of system MTTF?  Var_R(g) = Var_F(g) - correction,
correction = (H S dg)' (H S H')^{-1} (H S dg),  S = I^{-1}.
We approximate the FIM with the COMPLETE-DATA (no masking/censoring) series
likelihood via Monte Carlo score outer products -- enough to test the
symmetry mechanism (exact-equality under equal scales, near-equality under
baseline scales).
"""
import numpy as np
from scipy import integrate

rng = np.random.default_rng(7)
m = 5

def system_mttf(k, lam):
    f = lambda t: np.exp(-np.sum((t / lam) ** k))
    val, _ = integrate.quad(f, 0, np.inf, limit=200)
    return val

def grad_mttf(k, lam, eps=1e-6):
    g = np.zeros(2 * m)
    th0 = np.concatenate([k, lam])
    base = system_mttf(k, lam)
    for i in range(2 * m):
        th = th0.copy(); th[i] += eps
        g[i] = (system_mttf(th[:m], th[m:]) - base) / eps
    return g

def score(t, j, k, lam):
    """Score of one series observation (t, failed component j), complete data.
    loglik = log h_j(t) - sum_l (t/lam_l)^k_l
    """
    s = np.zeros(2 * m)
    for l in range(m):
        u = t / lam[l]
        # d/dk_l of -(u)^k_l
        s[l] += -(u ** k[l]) * np.log(u)
        # d/dlam_l of -(u)^k_l  = k_l u^k_l / lam_l
        s[m + l] += k[l] * (u ** k[l]) / lam[l]
    # log h_j = log k_j - k_j log lam_j + (k_j-1) log t
    u = t / lam[j]
    s[j] += 1 / k[j] + np.log(u)
    s[m + j] += -k[j] / lam[j]
    return s

def fim(k, lam, N=400_000):
    """MC estimate of complete-data FIM via score outer product."""
    # simulate series failures
    T = np.min(lam * rng.weibull(k, size=(N, m)) ** (1.0), axis=1)  # careful below
    # numpy weibull: scale 1, shape a -> X = W^(1) ; lifetime = lam * W where W~weibull(k)
    X = lam * rng.weibull(k, size=(N, m))
    T = X.min(axis=1); J = X.argmin(axis=1)
    S = np.zeros((2 * m, 2 * m))
    for t, j in zip(T, J):
        sc = score(t, j, k, lam)
        S += np.outer(sc, sc)
    return S / N

def variance_gap(k, lam):
    I = fim(np.asarray(k, float), np.asarray(lam, float))
    Sg = np.linalg.inv(I)
    dg = grad_mttf(np.asarray(k, float), np.asarray(lam, float))
    # constraints: k_1 - k_j = 0, j=2..m  -> H (m-1) x 2m
    H = np.zeros((m - 1, 2 * m))
    for r in range(m - 1):
        H[r, 0] = 1; H[r, r + 1] = -1
    varF = dg @ Sg @ dg
    A = H @ Sg @ dg
    corr = A @ np.linalg.solve(H @ Sg @ H.T, A)
    return varF, corr, corr / varF

k0 = 1.18
print("Case 1: equal scales (exchangeable), k=1.18, lam=900 x5")
vF, c, rel = variance_gap([k0]*m, [900.0]*m)
print(f"  varF(MTTF)={vF:.3f}  first-order reduction from constraint={c:.5f}  rel={rel:.2e}")

print("Case 2: baseline scales (994,909,840,940,923), common k=1.18")
vF, c, rel = variance_gap([k0]*m, [994.37, 908.95, 840.11, 940.13, 923.16])
print(f"  varF(MTTF)={vF:.3f}  first-order reduction from constraint={c:.5f}  rel={rel:.2e}")

print("Case 3: very unequal scales (1500,1200,900,600,300), common k=1.18")
vF, c, rel = variance_gap([k0]*m, [1500.0, 1200.0, 900.0, 600.0, 300.0])
print(f"  varF(MTTF)={vF:.3f}  first-order reduction from constraint={c:.5f}  rel={rel:.2e}")
