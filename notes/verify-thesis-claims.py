"""Verify the three load-bearing thesis claims against simulation data.

Claim 1: Reduced-model MTTF bias is ~O(CV^2) and sample-size independent.
Claim 2: MSE counterexample -- full model has lower MTTF MSE than reduced
         at CV=0 for n <= 1000 (paired MC significance test).
Claim 3: LRT detection threshold scales as 1/sqrt(n) (power collapses on n*CV^2).
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------- load
cons = pd.read_csv("results/consequence/data-consequence.csv")
div = pd.read_csv("results/lrt/divergence/data-lrt-divergence.csv")

print("=" * 78)
print("DATA HYGIENE: rows per condition (500 planned) and conv_R distribution")
print("=" * 78)
cnt = cons.groupby(["n", "target_cv"]).size().unstack("n")
print("consequence rows per (target_cv, n):")
print(cnt.to_string())
print("\nconv_R values:", cons.conv_R.value_counts().to_dict())
print("conv_F values:", cons.conv_F.value_counts().to_dict())

# ---------------------------------------------------------------- claim 1
print()
print("=" * 78)
print("CLAIM 1: bias ~ O(CV^2), independent of n")
print("=" * 78)
cons["bias_red"] = (cons.mttf_reduced - cons.mttf_true) / cons.mttf_true
g = cons.groupby(["actual_cv", "n"])["bias_red"].agg(["mean", "sem", "size"])
tab = (g["mean"] * 100).unstack("n").round(2)
print("Mean relative bias (%) of reduced-model MTTF by actual CV (rows) and n (cols):")
print(tab.to_string())

# Power-law fit log|bias| ~ a + b log(CV) over CV in [0.05, 0.30], per n
print("\nPower-law exponent fit (bias ~ CV^b), CV range 5%-42%:")
for n in sorted(cons.n.unique()):
    sub = g.xs(n, level="n").reset_index()
    sub = sub[(sub.actual_cv >= 0.05) & (sub["mean"] > 0)]
    b, a = np.polyfit(np.log(sub.actual_cv), np.log(sub["mean"]), 1)
    print(f"  n={n:5d}: exponent b = {b:.2f}")

# n-independence: bias range across n at each CV
print("\nSample-size independence check (bias % at n=100 vs n=5000):")
for cv in sorted(cons.actual_cv.unique()):
    sub = g.xs(cv, level="actual_cv")
    b100 = sub.loc[100, "mean"] * 100 if 100 in sub.index else np.nan
    b5000 = sub.loc[5000, "mean"] * 100 if 5000 in sub.index else np.nan
    print(f"  CV={cv*100:5.1f}%:  n=100: {b100:+.2f}%   n=5000: {b5000:+.2f}%")

# ---------------------------------------------------------------- claim 2
print()
print("=" * 78)
print("CLAIM 2: MSE counterexample at CV=0 (paired test, per replication)")
print("=" * 78)
print("d_i = SqErr(full_i) - SqErr(reduced_i); mean(d)<0 => full has LOWER MSE")
for cv0 in [0.0]:
    sub = cons[cons.target_cv == cv0]
    for n in sorted(sub.n.unique()):
        s = sub[sub.n == n]
        se_f = (s.mttf_full - s.mttf_true) ** 2
        se_r = (s.mttf_reduced - s.mttf_true) ** 2
        d = se_f - se_r
        md, sd = d.mean(), d.std(ddof=1) / np.sqrt(len(d))
        t = md / sd
        rmse_f = np.sqrt(se_f.mean())
        rmse_r = np.sqrt(se_r.mean())
        # variance and bias-squared decomposition
        var_f = s.mttf_full.var(ddof=1); var_r = s.mttf_reduced.var(ddof=1)
        b2_f = (s.mttf_full.mean() - s.mttf_true.iloc[0]) ** 2
        b2_r = (s.mttf_reduced.mean() - s.mttf_true.iloc[0]) ** 2
        print(f"  n={n:5d} (N={len(s):3d}): RMSE_F={rmse_f:6.2f} RMSE_R={rmse_r:6.2f}  "
              f"mean(d)={md:+8.1f} (t={t:+5.2f})  "
              f"VarF={var_f:7.1f} VarR={var_r:7.1f}  Bias2F={b2_f:5.1f} Bias2R={b2_r:5.1f}")

# correlation between full/reduced shape ests at CV=0 to understand mechanism
print("\nSame comparison from adaptive data (independent dataset, CV=0):")
adap = pd.read_csv("results/adaptive/data-adaptive.csv")
sub = adap[adap.target_cv == 0.0]
for n in sorted(sub.n.unique()):
    s = sub[sub.n == n]
    se_f = (s.mttf_full - s.mttf_true) ** 2
    se_r = (s.mttf_reduced - s.mttf_true) ** 2
    d = se_f - se_r
    t = d.mean() / (d.std(ddof=1) / np.sqrt(len(d)))
    print(f"  n={n:5d} (N={len(s):3d}): RMSE_F={np.sqrt(se_f.mean()):6.2f} "
          f"RMSE_R={np.sqrt(se_r.mean()):6.2f}  t={t:+5.2f}")

# ---------------------------------------------------------------- claim 3
print()
print("=" * 78)
print("CLAIM 3: detection threshold ~ 1/sqrt(n)  (power collapses on n*CV^2)")
print("=" * 78)
div["reject"] = (div.p_value < 0.05).astype(int)
pw = div.groupby(["actual_cv", "n"])["reject"].agg(["mean", "size"])
print("Rejection rate by actual CV and n:")
print((pw["mean"].unstack("n")).round(3).to_string())

# CV at 50% power per n (linear interp on log CV)
print("\nInterpolated CV at 50% power, compared with c/sqrt(n):")
rows = []
for n in sorted(div.n.unique()):
    s = pw.xs(n, level="n")["mean"].sort_index()
    s = s[s.index > 0]
    below = s[s < 0.5]
    above = s[s >= 0.5]
    if len(below) and len(above):
        cv_lo, p_lo = below.index[-1], below.iloc[-1]
        cv_hi, p_hi = above.index[0], above.iloc[0]
        cv50 = cv_lo + (0.5 - p_lo) * (cv_hi - cv_lo) / (p_hi - p_lo)
        rows.append((n, cv50))
        print(f"  n={n:5d}: CV50 ~ {cv50*100:5.2f}%   CV50*sqrt(n) = {cv50*np.sqrt(n):.3f}")
if len(rows) >= 2:
    ns = np.array([r[0] for r in rows]); cv50s = np.array([r[1] for r in rows])
    slope, _ = np.polyfit(np.log(ns), np.log(cv50s), 1)
    print(f"  log-log slope of CV50 vs n: {slope:.3f}  (Le Cam predicts -0.5)")

# noncentrality collapse: mean Lambda - (m-1) should be ~ n * c * CV^2
print("\nNoncentrality check: (mean(Lambda) - df) / (n * CV^2) should be ~constant:")
lam = div.groupby(["actual_cv", "n"])["Lambda"].mean()
m_df = 4  # m-1 with m=5
for (cv, n), L in lam.items():
    if cv > 0:
        c = (L - m_df) / (n * cv ** 2)
        if n in (100, 1000, 10000):
            print(f"  CV={cv*100:5.1f}% n={n:6d}: mean(Lambda)={L:7.2f}  c_hat={c:6.3f}")
