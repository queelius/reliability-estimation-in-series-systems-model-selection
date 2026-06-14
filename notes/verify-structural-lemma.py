"""Validate the STRUCTURE behind the zero-first-order-gain proposition, not
just the end result. Works in the (k, eta) parameterization, eta_l = lam_l^-k.

The proof rests on a 2D subspace closure. With blocks ordered (eta, k):
   grad g = (c_eta * 1, c_k * eta)   -- the gradient lives in P = span{(1,0),(0,eta)}
  and the Fisher information I maps U = span{(eta,0),(0,1)} into P:
    (P1) I_eta,eta @ eta  proportional to  1
    (P2) I_k,eta   @ eta  proportional to  eta
    (P3) I_eta,k   @ 1    proportional to  1
    (P4) I_k,k     @ 1    proportional to  eta
If (P1)-(P4) hold then I: U -> P is onto (2x2, generically invertible), so
I^{-1} grad g lies in U, whose k-block is proportional to 1, i.e. constant
across components: exactly the reduced model's tangent space. Zero gain.

This script checks grad-g structure and (P1)-(P4) for COMPLETE data (where
the hand proof gives them in closed form) and for MASKED + CENSORED data
(where we only have the conjecture). Proportionality residual reported as
the relative deviation from the best rank-1 (proportional) fit.
"""
import numpy as np
from scipy import integrate

rng = np.random.default_rng(20260614)

m = 5
K0 = 1.18
SCALES = np.array([994.37, 908.95, 840.11, 940.13, 923.16])
ETA = SCALES ** (-K0)                      # eta_l = lam_l^-k at common shape
P_MASK, Q_CENS = 0.215, 0.825


def system_reliability(t, k, lam):
    t = np.atleast_1d(t)
    return np.exp(-np.sum((t[:, None] / lam) ** k, axis=1))


def system_mttf(k, lam):
    return integrate.quad(lambda t: np.exp(-np.sum((t / lam) ** k)), 0, np.inf,
                          limit=300)[0]


def system_quantile(q, k, lam):
    from scipy.optimize import brentq
    return brentq(lambda t: system_reliability(t, k, lam)[0] - (1 - q), 1e-6, 1e7)


def prop_residual(Mv, ref):
    """Relative deviation of vector Mv from being proportional to ref."""
    ref = ref / np.linalg.norm(ref)
    proj = (Mv @ ref) * ref
    return np.linalg.norm(Mv - proj) / (np.linalg.norm(Mv) + 1e-300)


# ----- gradients in (eta, k) coordinates via finite differences -------------
def system_mttf_eta(eta, k_vec):
    lam = eta ** (-1.0 / k_vec)
    return system_mttf(k_vec, lam)


def system_R_eta(t, eta, k_vec):
    lam = eta ** (-1.0 / k_vec)
    return system_reliability(t, k_vec, lam)[0]


def grad_eta_k(func, eps=1e-6):
    """grad of func(eta, k_vec) at (ETA, K0*1), returns (d/d eta [m], d/d k [m])."""
    eta0 = ETA.copy(); k0 = np.full(m, K0)
    g_eta = np.zeros(m); g_k = np.zeros(m)
    for l in range(m):
        e = eta0.copy(); h = eps * eta0[l]
        e[l] += h; fp = func(e, k0); e[l] -= 2 * h; fm = func(e, k0)
        g_eta[l] = (fp - fm) / (2 * h)
        kk = k0.copy(); hk = eps
        kk[l] += hk; fp = func(eta0, kk); kk[l] -= 2 * hk; fm = func(eta0, kk)
        g_k[l] = (fp - fm) / (2 * hk)
    return g_eta, g_k


# ----- Fisher information in (eta, k), by MC score outer products -----------
def fim_eta_k(masked, N=3_000_000, batch=300_000):
    k = np.full(m, K0); eta = ETA
    lam = eta ** (-1.0 / k)
    tau = system_quantile(Q_CENS, k, lam) if masked else np.inf
    S = np.zeros((2 * m, 2 * m)); done = 0
    while done < N:
        n = min(batch, N - done)
        X = lam * rng.weibull(k, size=(n, m))
        Tsys = X.min(1); J = X.argmin(1)
        if masked:
            delta = Tsys <= tau
            T = np.where(delta, Tsys, tau)
            C = rng.random((n, m)) < P_MASK
            C[np.arange(n), J] = True
            C[~delta] = False
        else:
            delta = np.ones(n, bool); T = Tsys
            C = np.zeros((n, m), bool); C[np.arange(n), J] = True
        tk = T[:, None] ** k                       # t^{k_l}, common k
        lnt = np.log(T)[:, None]
        # -- eta scores: -t^{k_l} + (failure) 1{l in C} h_l / sum_{C} h
        d_eta = -tk
        d_k = -eta * tk * lnt                       # from -sum eta_l t^{k_l}
        if masked or True:
            h = eta * k * T[:, None] ** (k - 1)     # hazards h_l (n,m)
            hC = np.where(C, h, 0.0).sum(1)         # sum over candidate set
            hC = np.where(delta, hC, 1.0)
            add_eta = np.where(C, k * T[:, None] ** (k - 1), 0.0) / hC[:, None]
            # d/dk_l of log sum_{C} eta_l k_l t^{k_l-1}:
            #   numerator term for l in C: eta_l t^{k_l-1}(1 + k_l ln t)
            add_k = np.where(C, eta * T[:, None] ** (k - 1) * (1 + k * lnt), 0.0) / hC[:, None]
            d_eta = d_eta + np.where(delta[:, None], add_eta, 0.0)
            d_k = d_k + np.where(delta[:, None], add_k, 0.0)
        sc = np.concatenate([d_eta, d_k], axis=1)
        S += sc.T @ sc; done += n
    return S / N


def analyze(masked):
    label = "MASKED + CENSORED" if masked else "COMPLETE DATA"
    print(f"\n{'='*72}\n{label}\n{'='*72}")
    I = fim_eta_k(masked)
    Iee = I[:m, :m]; Iek = I[:m, m:]; Ike = I[m:, :m]; Ikk = I[m:, m:]
    one = np.ones(m)
    print("Structural proportionalities (relative residual; ~0 means holds):")
    print(f"  (P1) I_ee @ eta  ~ 1   : {prop_residual(Iee @ ETA, one):.2e}")
    print(f"  (P2) I_ke @ eta  ~ eta : {prop_residual(Ike @ ETA, ETA):.2e}")
    print(f"  (P3) I_ek @ 1    ~ 1   : {prop_residual(Iek @ one, one):.2e}")
    print(f"  (P4) I_kk @ 1    ~ eta : {prop_residual(Ikk @ one, ETA):.2e}")
    mttf0 = system_mttf(np.full(m, K0), SCALES)
    for name, fn in [("MTTF", lambda e, kk: system_mttf_eta(e, kk)),
                     ("R(MTTF)", lambda e, kk: system_R_eta(mttf0, e, kk))]:
        g_eta, g_k = grad_eta_k(fn)
        print(f"  grad {name}: eta-block ~ 1 resid {prop_residual(g_eta, one):.2e}, "
              f"k-block ~ eta resid {prop_residual(g_k, ETA):.2e}")
        dg = np.concatenate([g_eta, g_k])
        Sg = np.linalg.inv(I)
        # constraint A: contrasts on k-block
        A = np.zeros((m - 1, 2 * m))
        for r in range(m - 1):
            A[r, m + r] = 1.0; A[r, m + r + 1] = -1.0
        varF = dg @ Sg @ dg
        Av = A @ Sg @ dg
        gain = Av @ np.linalg.solve(A @ Sg @ A.T, Av)
        # also: is k-block of Sg@dg constant?
        v = Sg @ dg
        kblock_resid = prop_residual(v[m:], one)
        print(f"           var_F={varF:.4e}  gain={gain:.3e}  rel={gain/varF:.2e}"
              f"  (k-block of I^-1 grad const? resid {kblock_resid:.2e})")


if __name__ == "__main__":
    print(f"Common-shape point k={K0}, scales=baseline, eta=lam^-k")
    analyze(masked=False)
    analyze(masked=True)
