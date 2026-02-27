#!/usr/bin/env python3
"""
Bias-variance decomposition of MTTF MSE for full vs reduced models.

Key finding: the full model has LOWER MTTF variance than the reduced model
even when the reduced model is correctly specified (CV=0). The constraint
k_1 = ... = k_m forces all shape estimation error into one degree of freedom,
amplifying its propagation through the nonlinear MTTF integral.

Produces a 2-panel figure:
  (a) Variance comparison: full vs reduced MTTF variance by CV and n
  (b) MSE decomposition: stacked bias^2 + variance for each model
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# --- Path setup ---
SCRIPT_DIR = Path(__file__).resolve().parent
PAPER_IMAGE = SCRIPT_DIR.parents[2] / 'paper' / 'image'
PAPER_IMAGE.mkdir(parents=True, exist_ok=True)

# Read data
df = pd.read_csv('../data-consequence.csv')
print(f"Loaded {len(df)} rows")
print(f"CV values: {sorted(df['target_cv'].unique())}")
print(f"Sample sizes: {sorted(df['n'].unique())}")

# --- Compute bias-variance decomposition ---
def bv_decomposition(df):
    """Compute bias, variance, and MSE for each (target_cv, n) condition."""
    rows = []
    for (tcv, n), g in df.groupby(['target_cv', 'n']):
        mttf_true = g['mttf_true'].iloc[0]
        actual_cv = g['actual_cv'].iloc[0]

        for model, col in [('full', 'mttf_full'), ('reduced', 'mttf_reduced')]:
            estimates = g[col].values
            mean_est = np.mean(estimates)
            bias = mean_est - mttf_true
            variance = np.mean((estimates - mean_est) ** 2)
            mse = np.mean((estimates - mttf_true) ** 2)
            # Sanity check: MSE ≈ bias^2 + variance
            mse_check = bias**2 + variance

            rows.append({
                'target_cv': tcv,
                'actual_cv': actual_cv,
                'n': n,
                'model': model,
                'mttf_true': mttf_true,
                'mean_est': mean_est,
                'bias': bias,
                'bias_sq': bias**2,
                'variance': variance,
                'mse': mse,
                'mse_check': mse_check,
                'bias_frac': bias**2 / mse if mse > 0 else 0,
                'var_frac': variance / mse if mse > 0 else 0,
                'n_reps': len(g),
            })

    return pd.DataFrame(rows)


bv = bv_decomposition(df)

# Print key findings
print("\n" + "=" * 70)
print("BIAS-VARIANCE DECOMPOSITION")
print("=" * 70)
for n in sorted(bv['n'].unique()):
    print(f"\nn = {n}:")
    sub = bv[bv['n'] == n]
    for tcv in sorted(sub['target_cv'].unique()):
        full = sub[(sub['target_cv'] == tcv) & (sub['model'] == 'full')].iloc[0]
        red = sub[(sub['target_cv'] == tcv) & (sub['model'] == 'reduced')].iloc[0]
        print(f"  CV={full['actual_cv']*100:5.1f}%: "
              f"Var(full)={full['variance']:.1f} Var(red)={red['variance']:.1f} "
              f"Bias²(full)={full['bias_sq']:.1f} Bias²(red)={red['bias_sq']:.1f} "
              f"MSE(full)={full['mse']:.1f} MSE(red)={red['mse']:.1f}")

# Save summary
bv.to_csv('summary_mse_decomposition.csv', index=False)
print("\nSummary saved to summary_mse_decomposition.csv")

# =========================================================================
# Figure: 2-panel bias-variance decomposition
# =========================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

sample_sizes = sorted(bv['n'].unique())
colors_n = plt.cm.viridis(np.linspace(0.2, 0.8, len(sample_sizes)))

# --- Panel (a): Variance comparison ---
for i, n in enumerate(sample_sizes):
    sub_full = bv[(bv['n'] == n) & (bv['model'] == 'full')].sort_values('actual_cv')
    sub_red = bv[(bv['n'] == n) & (bv['model'] == 'reduced')].sort_values('actual_cv')

    ax1.plot(sub_full['actual_cv'] * 100, sub_full['variance'],
             's--', color=colors_n[i], alpha=0.7, markersize=4,
             label=f'Full (n={n})')
    ax1.plot(sub_red['actual_cv'] * 100, sub_red['variance'],
             'o-', color=colors_n[i], markersize=4,
             label=f'Reduced (n={n})')

ax1.set_xlabel('Shape CV (%)', fontsize=11)
ax1.set_ylabel('MTTF Estimator Variance', fontsize=11)
ax1.set_title('(a) Variance: Full vs Reduced Model', fontsize=12)
ax1.legend(fontsize=7, loc='upper left', ncol=2)
ax1.grid(True, alpha=0.3)

# --- Panel (b): MSE decomposition (stacked bars) ---
# Focus on n=100 and n=500 for readability
focus_ns = [100, 500]
cvs = sorted(bv['actual_cv'].unique())
n_cvs = len(cvs)
bar_width = 0.35
x_base = np.arange(n_cvs)

color_bias = {'full': '#2166ac', 'reduced': '#b2182b'}
color_var = {'full': '#92c5de', 'reduced': '#f4a582'}

for idx, n_focus in enumerate(focus_ns):
    offset = idx * (2 * n_cvs + 2)  # spacing between n groups

    for m_idx, model in enumerate(['full', 'reduced']):
        sub = bv[(bv['n'] == n_focus) & (bv['model'] == model)].sort_values('actual_cv')
        x = x_base + m_idx * bar_width + offset

        # Stacked: variance on bottom, bias^2 on top
        bars_var = ax2.bar(x, sub['variance'].values, bar_width,
                           color=color_var[model],
                           label=f'{model.capitalize()} variance' if idx == 0 else '')
        bars_bias = ax2.bar(x, sub['bias_sq'].values, bar_width,
                            bottom=sub['variance'].values,
                            color=color_bias[model],
                            label=f'{model.capitalize()} bias²' if idx == 0 else '')

    # x-tick labels for this group
    mid_x = x_base + bar_width / 2 + offset
    for j, cv in enumerate(cvs):
        ax2.text(mid_x[j], -15, f'{cv*100:.0f}%', ha='center', fontsize=6,
                 rotation=45)

    # Group label
    ax2.text(mid_x[n_cvs // 2], ax2.get_ylim()[1] * 0.95 if idx == 0 else -45,
             f'n={n_focus}', ha='center', fontsize=10, fontweight='bold')

ax2.set_ylabel('MSE = Variance + Bias²', fontsize=11)
ax2.set_title('(b) MSE Decomposition by Shape CV', fontsize=12)
ax2.set_xticks([])
ax2.set_xlabel('Shape CV (%)', fontsize=11)
ax2.legend(fontsize=8, loc='upper left')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()

# Save
fig.savefig('mse_decomposition.pdf', bbox_inches='tight')
fig.savefig(PAPER_IMAGE / 'mse_decomposition.pdf', bbox_inches='tight')
print("\nFigure saved to mse_decomposition.pdf and paper/image/mse_decomposition.pdf")

plt.close()
