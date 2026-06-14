#!/usr/bin/env python3
"""
Decoupling evidence: the LRT power curve is governed by a single noncentrality
parameter ncp = c_D * n * CV^2 (Le Cam local alternatives). Plotting rejection
rate against n*CV^2 collapses every (n, CV) condition onto one curve, the
noncentral chi-square(df=m-1) power function. This is the empirical heart of
the detection half of the bias-vs-detectability decoupling.

Outputs:
  - decoupling_ncp_collapse.pdf (local + paper/image/)
  - prints the fitted c_D and the CV50 ~ const/sqrt(n) law
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PAPER_IMAGE = SCRIPT_DIR.parents[3] / "paper" / "image"
PAPER_IMAGE.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(SCRIPT_DIR.parent / "data-lrt-divergence.csv")
alpha, m = 0.05, 5
df_df = m - 1
crit = stats.chi2.ppf(1 - alpha, df_df)

df["reject"] = (df["p_value"] < alpha).astype(int)
g = df.groupby(["actual_cv", "n"]).agg(
    reject=("reject", "mean"), N=("reject", "count"),
    mean_lambda=("Lambda", "mean")).reset_index()
g = g[g["actual_cv"] > 0].copy()
g["x"] = g["n"] * g["actual_cv"] ** 2          # collapse variable

# Fit c_D from the noncentrality: ncp_hat = mean(Lambda) - df, regressed on x.
# Restrict to the LOCAL regime (CV <= 27%): beyond it the local-alternative
# approximation ncp ~ c_D n CV^2 breaks down and ncp grows super-quadratically.
g["ncp_hat"] = g["mean_lambda"] - df_df
mask = (g["n"] >= 1000) & (g["actual_cv"] <= 0.275)
c_D = float(np.sum(g.loc[mask, "x"] * g.loc[mask, "ncp_hat"]) /
            np.sum(g.loc[mask, "x"] ** 2))
print(f"Fitted noncentrality constant c_D = {c_D:.3f} "
      f"(n>=1000, CV<=27% local regime)")

# CV50 ~ c / sqrt(n)
print("\nCV at 50% power and CV50*sqrt(n):")
cv50_rows = []
for n in sorted(g["n"].unique()):
    s = g[g["n"] == n].sort_values("actual_cv")
    below, above = s[s.reject < 0.5], s[s.reject >= 0.5]
    if len(below) and len(above):
        x0, y0 = below.iloc[-1][["actual_cv", "reject"]]
        x1, y1 = above.iloc[0][["actual_cv", "reject"]]
        cv50 = x0 + (0.5 - y0) * (x1 - x0) / (y1 - y0)
        cv50_rows.append((n, cv50))
        print(f"  n={int(n):6d}: CV50={cv50*100:5.2f}%  CV50*sqrt(n)={cv50*np.sqrt(n):.3f}")
ns = np.array([r[0] for r in cv50_rows]); cvs = np.array([r[1] for r in cv50_rows])
slope, int2 = np.polyfit(np.log(ns), np.log(cvs), 1)
print(f"  log-log slope of CV50 vs n: {slope:.3f} (Le Cam predicts -0.5)")
const = float(np.mean(cvs * np.sqrt(ns)))
print(f"  CV50 ~ {const:.2f}/sqrt(n)")

# collapse panel restricted to the local regime where ncp ~ c_D n CV^2 holds
gloc = g[g["actual_cv"] <= 0.275]
xx = np.linspace(gloc["x"].min(), gloc["x"].max(), 400)
ncp = c_D * xx
power = stats.ncx2.sf(crit, df_df, ncp)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 4.2))

markers = {100: "o", 500: "s", 1000: "^", 5000: "D", 10000: "v"}
for n in sorted(gloc["n"].unique()):
    s = gloc[gloc["n"] == n]
    axL.scatter(s["x"], s["reject"], s=42, marker=markers.get(n, "o"),
                label=f"n={int(n)}", zorder=3, edgecolor="k", linewidth=0.4)
axL.plot(xx, power, "k-", lw=2,
         label=rf"ncx2$(4,\ {c_D:.2f}\,n\,CV^2)$", zorder=2)
axL.axhline(alpha, color="red", ls="--", alpha=0.5, lw=1)
axL.set_xscale("log")
axL.set_xlabel(r"$n\,\mathrm{CV}_k^2$ (collapse variable)")
axL.set_ylabel("LRT rejection rate")
axL.set_title("(a) Power collapses onto one noncentral-$\\chi^2$ curve")
axL.legend(fontsize=8, loc="lower right")
axL.grid(True, alpha=0.3)
axL.set_ylim(-0.03, 1.05)

# right panel: CV50 vs n with the c/sqrt(n) reference
nn = np.logspace(np.log10(ns.min()), np.log10(ns.max()), 100)
axR.loglog(ns, cvs * 100, "ko", ms=7, label="CV at 50% power")
axR.loglog(nn, const / np.sqrt(nn) * 100, "b-", lw=2,
           label=rf"${const:.1f}/\sqrt{{n}}$")
axR.set_xlabel("sample size $n$")
axR.set_ylabel(r"detectable shape CV$_k$ at 50% power (%)")
axR.set_title(r"(b) Detection threshold falls as $1/\sqrt{n}$")
axR.legend(fontsize=9)
axR.grid(True, which="both", alpha=0.3)

fig.tight_layout()
for dest in [SCRIPT_DIR / "decoupling_ncp_collapse.pdf",
             PAPER_IMAGE / "decoupling_ncp_collapse.pdf"]:
    fig.savefig(dest, bbox_inches="tight")
print(f"\nSaved decoupling_ncp_collapse.pdf to {PAPER_IMAGE}")
