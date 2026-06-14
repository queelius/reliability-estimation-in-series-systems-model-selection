#!/usr/bin/env python3
"""
Pretest model selection: extend the LRT-pretest comparison to AIC- and
BIC-pretest selectors, computed post-hoc from the adaptive simulation's
log-likelihood columns (no new simulation). For nested models differing by
m-1 = 4 parameters, the selection rules in terms of Lambda = -2(llR - llF) are:
  LRT  : pick reduced if Lambda < chi2_{4,0.95} = 9.488
  AIC  : pick reduced if Lambda < 2*(df) = 8
  BIC  : pick reduced if Lambda < df*log(n) = 4 log n
The MTTF estimate then comes from the selected model. We report RMSE (% of true
MTTF) and overhead vs always-full, exposing the pretest-estimator risk hump.
"""
import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
df = pd.read_csv(SCRIPT_DIR.parent / "data-adaptive.csv")
m = 5
dfree = m - 1
crit = stats.chi2.ppf(0.95, dfree)

# recompute Lambda from loglik columns where present, else use the column
df["Lambda_rec"] = -2 * (df.loglik_R - df.loglik_F)
df["Lambda_use"] = df["Lambda"].where(df["Lambda"].notna(), df["Lambda_rec"])

def selected_mttf(row, rule):
    L = row["Lambda_use"]
    if rule == "lrt":
        thr = crit
    elif rule == "aic":
        thr = 2 * dfree
    elif rule == "bic":
        thr = dfree * np.log(row["n"])
    use_reduced = L < thr
    return row["mttf_reduced"] if use_reduced else row["mttf_full"]

for rule in ["aic", "bic"]:
    df[f"mttf_{rule}"] = df.apply(lambda r: selected_mttf(r, rule), axis=1)
    df[f"sel_red_{rule}"] = (df["Lambda_use"] <
                             (2 * dfree if rule == "aic" else dfree * np.log(df["n"])))

def rmse_pct(est, row_true):
    return np.sqrt(((est - row_true) ** 2).mean()) / row_true.mean() * 100

print("Pretest selectors: RMSE (% true MTTF) and reduced-selection rate")
print(f"{'CV':>5} {'n':>5} | {'Full':>5} {'Red':>5} {'LRT':>5} {'AIC':>5} {'BIC':>5} "
      f"| {'selR_LRT':>8} {'selR_AIC':>8} {'selR_BIC':>8}")
out = []
for (tcv, n), s in df.groupby(["target_cv", "n"]):
    tr = s["mttf_true"]
    rF = rmse_pct(s.mttf_full, tr); rR = rmse_pct(s.mttf_reduced, tr)
    rL = rmse_pct(s.mttf_adaptive_lrt, tr)
    rA = rmse_pct(s.mttf_aic, tr); rB = rmse_pct(s.mttf_bic, tr)
    selL = (s["Lambda_use"] < crit).mean()
    selA = s["sel_red_aic"].mean(); selB = s["sel_red_bic"].mean()
    out.append((tcv, n, rF, rR, rL, rA, rB, selL, selA, selB))
    print(f"{tcv:>5.2f} {int(n):>5} | {rF:>5.1f} {rR:>5.1f} {rL:>5.1f} {rA:>5.1f} "
          f"{rB:>5.1f} | {selL:>8.2f} {selA:>8.2f} {selB:>8.2f}")

res = pd.DataFrame(out, columns=["target_cv", "n", "rmse_full", "rmse_reduced",
                                 "rmse_lrt", "rmse_aic", "rmse_bic",
                                 "selred_lrt", "selred_aic", "selred_bic"])
res.to_csv(SCRIPT_DIR / "summary_aic_bic_adaptive.csv", index=False)

# pretest risk hump: worst overhead vs always-full at each n
print("\nWorst pretest overhead vs always-full (max over CV), by selector and n:")
for n in sorted(res.n.unique()):
    s = res[res.n == n]
    for col, name in [("rmse_lrt", "LRT"), ("rmse_aic", "AIC"), ("rmse_bic", "BIC")]:
        ov = ((s[col] - s.rmse_full) / s.rmse_full * 100)
        print(f"  n={int(n):5d} {name}: worst overhead {ov.max():+5.1f}% "
              f"at CV={s.loc[ov.idxmax(),'target_cv']:.2f}")
print(f"\nSaved summary_aic_bic_adaptive.csv to {SCRIPT_DIR}")
