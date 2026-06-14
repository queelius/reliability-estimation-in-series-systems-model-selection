#!/usr/bin/env python3
"""
Theory-supporting computations for the consequence-analysis section.

(1) Population (n -> infinity) misspecification bias of the common-shape model,
    by deterministic KL projection of the heterogeneous truth onto the reduced
    family under the paper's masking (p=0.215) and censoring (q=0.825). This
    SEPARATES specification bias from the finite-sample estimation bias that
    contaminates the n=100 column of the simulated table, and exhibits the
    O(CV^2) law with no linear term. Overlays the n=5000 simulated bias.
    -> population_bias.pdf, population_bias.csv

(2) MSE-decomposition table at CV=0: full vs reduced MTTF MSE with paired test
    and variance / bias^2 split, extended to n=5000 (where the effect vanishes,
    confirming the zero-first-order-gain proposition).

(3) R(t) relative-bias table from the existing reliability columns.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import integrate, optimize, special
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PAPER_IMAGE = SCRIPT_DIR.parents[2] / "paper" / "image"
PAPER_IMAGE.mkdir(parents=True, exist_ok=True)

m, K0 = 5, 1.18
SCALES = np.array([994.37, 908.95, 840.11, 940.13, 923.16])
P_MASK, Q_CENS = 0.215, 0.825


def gen_shapes(target_cv):
    if target_cv < 1e-4:
        return np.full(m, K0)
    hr = target_cv * K0 * np.sqrt(3)
    return np.linspace(K0 - hr, K0 + hr, m)


def sys_R(t, k, lam):
    t = np.atleast_1d(t)
    return np.exp(-np.sum((t[:, None] / lam) ** k, axis=1))


def sys_mttf(k, lam):
    return integrate.quad(lambda t: float(np.exp(-np.sum((t / lam) ** k))),
                          0, np.inf, limit=300)[0]


def sys_quantile(q, k, lam):
    return optimize.brentq(lambda t: sys_R(t, k, lam)[0] - (1 - q), 1e-6, 1e7)


# ---------- (1) population KL projection, robust ----------------------------
def neg_expected_reduced_loglik(k0, lam0, tau, ngrid=20000):
    """E_truth[ reduced loglik ] as a function of reduced params, masked+cens."""
    t = np.linspace(1e-6, tau, ngrid)
    U0 = t[:, None] / lam0
    R0 = np.exp(-(U0 ** k0).sum(1))
    h0 = (k0 / lam0) * U0 ** (k0 - 1)                 # cause hazards (T, m)
    others = [[l for l in range(m) if l != j] for j in range(m)]
    sub, prob = [], []
    for j in range(m):
        Sj, Pj = [], []
        for code in range(2 ** (m - 1)):
            mask = np.zeros(m, bool); mask[j] = True; nin = 0
            for bi, l in enumerate(others[j]):
                if (code >> bi) & 1:
                    mask[l] = True; nin += 1
            Sj.append(mask); Pj.append(P_MASK ** nin * (1 - P_MASK) ** (m - 1 - nin))
        sub.append(np.array(Sj)); prob.append(np.array(Pj))
    Rtau = float(sys_R(np.array([tau]), k0, lam0)[0])

    def negE(z):                                       # z = [log kappa, log lam_1..m]
        kap = np.exp(z[0]); lamR = np.exp(z[1:])
        UR = t[:, None] / lamR
        hR = (kap / lamR) * UR ** (kap - 1)
        HRsum = (UR ** kap).sum(1)
        val = 0.0
        for j in range(m):
            wj = h0[:, j] * R0
            inner = np.zeros_like(t)
            for mask, pr in zip(sub[j], prob[j]):
                inner += pr * np.log(np.clip(hR[:, mask].sum(1), 1e-300, None))
            val += np.trapezoid(wj * (inner - HRsum), t)
        val += Rtau * (-np.sum((tau / lamR) ** kap))
        return -val
    return negE


def population_bias(target_cv):
    k_true = gen_shapes(target_cv)
    lam = SCALES
    acv = np.std(k_true, ddof=1) / np.mean(k_true) if target_cv > 0 else 0.0
    tau = sys_quantile(Q_CENS, k_true, lam)
    negE = neg_expected_reduced_loglik(k_true, lam, tau)
    best = None
    for kap0 in [k_true.mean(), k_true.min(), k_true.max()]:
        z0 = np.concatenate([[np.log(kap0)], np.log(lam)])
        r = optimize.minimize(negE, z0, method="L-BFGS-B",
                              options={"maxiter": 2000, "ftol": 1e-12})
        if best is None or r.fun < best.fun:
            best = r
    kap = np.exp(best.x[0]); lamR = np.exp(best.x[1:])
    mttfR = special.gamma(1 + 1 / kap) * np.sum(lamR ** (-kap)) ** (-1 / kap)
    mttfT = sys_mttf(k_true, lam)
    return acv, (mttfR - mttfT) / mttfT


cvs_target = [0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.25, 0.30]
rows = []
print("Population (n->inf) misspecification bias (deterministic KL projection):")
for tcv in cvs_target:
    acv, B = population_bias(tcv)
    rows.append((tcv, acv, B))
    cB = B / acv ** 2 if acv > 0 else np.nan
    print(f"  target CV {tcv:.2f}  actual {acv*100:6.3f}%  pop bias {B*100:+7.3f}%"
          f"  B/CV^2 {cB:6.3f}" if acv > 0 else
          f"  target CV {tcv:.2f}  actual  0.000%  pop bias {B*100:+7.3f}%")
pop = pd.DataFrame(rows, columns=["target_cv", "actual_cv", "pop_bias"])
pop.to_csv(SCRIPT_DIR / "population_bias.csv", index=False)

# quadratic coefficient from the reliable regime (actual CV <= 0.20)
fit = pop[(pop.actual_cv > 0) & (pop.actual_cv <= 0.205)]
cB = float(np.sum(fit.actual_cv ** 2 * fit.pop_bias) / np.sum(fit.actual_cv ** 4))
print(f"\nLeading quadratic coefficient c_B = {cB:.3f} (fit over actual CV <= 20%)")

# simulated n=5000 bias overlay
sim = pd.read_csv(SCRIPT_DIR.parent / "data-consequence.csv")
sim["bias"] = (sim.mttf_reduced - sim.mttf_true) / sim.mttf_true
sim5 = sim[sim.n == 5000].groupby("actual_cv")["bias"].mean().reset_index()

fig, ax = plt.subplots(figsize=(6.4, 4.4))
xx = np.linspace(0, 0.205, 100)
ax.plot(xx * 100, cB * xx ** 2 * 100, "b-", lw=2,
        label=rf"population $\approx {cB:.2f}\,\mathrm{{CV}}_k^2$")
preliable = pop[pop.actual_cv <= 0.205]
ax.scatter(preliable.actual_cv * 100, preliable.pop_bias * 100, c="b", s=40,
           zorder=4, label="population (KL projection)", edgecolor="k", linewidth=0.4)
ax.scatter(sim5[sim5.actual_cv <= 0.205].actual_cv * 100,
           sim5[sim5.actual_cv <= 0.205].bias * 100, c="orange", marker="s",
           s=42, zorder=5, label="simulated, $n=5000$", edgecolor="k", linewidth=0.4)
ax.axhspan(-1, 1, color="green", alpha=0.10, label=r"$\pm1\%$ acceptable")
ax.axhline(0, color="gray", lw=0.6)
ax.set_xlabel(r"actual shape CV$_k$ (\%)" if False else "actual shape CV (%)")
ax.set_ylabel("relative MTTF bias of common-shape model (%)")
ax.set_title("Specification bias is $O(\\mathrm{CV}^2)$ with no linear term")
ax.legend(fontsize=8.5, loc="upper left")
ax.grid(True, alpha=0.3)
fig.tight_layout()
for dest in [SCRIPT_DIR / "population_bias.pdf", PAPER_IMAGE / "population_bias.pdf"]:
    fig.savefig(dest, bbox_inches="tight")
print(f"Saved population_bias.pdf to {PAPER_IMAGE}")

# ---------- (2) MSE decomposition at CV=0 -----------------------------------
print("\n" + "=" * 72)
print("MSE decomposition at CV=0 (full vs reduced MTTF), with paired test:")
print(f"{'n':>6} {'RMSE_F':>8} {'RMSE_R':>8} {'paired t':>9} "
      f"{'VarF':>8} {'VarR':>8} {'Bias2F':>7} {'Bias2R':>7}")
mse_rows = []
for n in sorted(sim[sim.target_cv == 0].n.unique()):
    s = sim[(sim.target_cv == 0) & (sim.n == n)]
    seF = (s.mttf_full - s.mttf_true) ** 2
    seR = (s.mttf_reduced - s.mttf_true) ** 2
    d = seF - seR
    t = d.mean() / (d.std(ddof=1) / np.sqrt(len(d)))
    vF, vR = s.mttf_full.var(ddof=1), s.mttf_reduced.var(ddof=1)
    b2F = (s.mttf_full.mean() - s.mttf_true.iloc[0]) ** 2
    b2R = (s.mttf_reduced.mean() - s.mttf_true.iloc[0]) ** 2
    mse_rows.append((n, np.sqrt(seF.mean()), np.sqrt(seR.mean()), t, vF, vR, b2F, b2R))
    print(f"{n:>6} {np.sqrt(seF.mean()):>8.2f} {np.sqrt(seR.mean()):>8.2f} "
          f"{t:>+9.2f} {vF:>8.1f} {vR:>8.1f} {b2F:>7.1f} {b2R:>7.1f}")

# ---------- (3) R(t) relative-bias table ------------------------------------
print("\n" + "=" * 72)
print("R(t) relative bias (%) of common-shape model, n=1000, by actual CV:")
print(f"{'CV%':>6} {'R(MTTF/2)':>10} {'R(MTTF)':>9} {'R(2MTTF)':>9}")
s1000 = sim[sim.n == 1000]
for acv in sorted(s1000.actual_cv.unique()):
    s = s1000[s1000.actual_cv == acv]
    b_half = ((s.R_half_reduced - s.R_half_true) / s.R_half_true).mean() * 100
    b_m = ((s.R_mttf_reduced - s.R_mttf_true) / s.R_mttf_true).mean() * 100
    b_2 = ((s.R_2mttf_reduced - s.R_2mttf_true) / s.R_2mttf_true).mean() * 100
    print(f"{acv*100:>6.1f} {b_half:>+10.2f} {b_m:>+9.2f} {b_2:>+9.2f}")
