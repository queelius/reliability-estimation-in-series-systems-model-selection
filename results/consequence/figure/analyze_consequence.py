#!/usr/bin/env python3
"""
Analyze consequence analysis results: How much does MTTF estimation degrade
when the reduced (common-shape) model is incorrectly applied to systems
with heterogeneous shapes?

Key outputs:
  1. MTTF bias curves: full vs reduced model, by CV and sample size
  2. RMSE comparison showing crossover behavior
  3. R(t) bias analysis at mission-critical time points
  4. Summary CSV and LaTeX table
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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

# --- Compute summary statistics ---
def compute_summaries(df):
    """Compute bias, RMSE, and relative efficiency by (target_cv, n)."""
    groups = df.groupby(['target_cv', 'n'])

    # Mean MTTF estimates
    means = groups.agg(
        mttf_true=('mttf_true', 'first'),
        actual_cv=('actual_cv', 'first'),
        mttf_full_mean=('mttf_full', 'mean'),
        mttf_red_mean=('mttf_reduced', 'mean'),
        n_reps=('mttf_true', 'count'),
    ).reset_index()

    # Bias (%)
    means['bias_full_pct'] = 100 * (means['mttf_full_mean'] - means['mttf_true']) / means['mttf_true']
    means['bias_red_pct'] = 100 * (means['mttf_red_mean'] - means['mttf_true']) / means['mttf_true']

    # MSE and RMSE
    mse = groups.apply(lambda g: pd.Series({
        'mse_full': ((g['mttf_full'] - g['mttf_true'])**2).mean(),
        'mse_red': ((g['mttf_reduced'] - g['mttf_true'])**2).mean(),
    })).reset_index()

    means = means.merge(mse, on=['target_cv', 'n'])
    means['rmse_full'] = np.sqrt(means['mse_full'])
    means['rmse_red'] = np.sqrt(means['mse_red'])

    # Relative efficiency: MSE_full / MSE_reduced (>1 means reduced better)
    means['rel_eff'] = means['mse_full'] / means['mse_red']

    # MTTF error as % of true MTTF
    means['rmse_full_pct'] = 100 * means['rmse_full'] / means['mttf_true']
    means['rmse_red_pct'] = 100 * means['rmse_red'] / means['mttf_true']

    # R(t) bias at system MTTF
    R_means = groups.agg(
        R_mttf_true=('R_mttf_true', 'first'),
        R_mttf_full=('R_mttf_full', 'mean'),
        R_mttf_red=('R_mttf_reduced', 'mean'),
    ).reset_index()
    R_means['R_bias_full_pct'] = 100 * (R_means['R_mttf_full'] - R_means['R_mttf_true']) / R_means['R_mttf_true']
    R_means['R_bias_red_pct'] = 100 * (R_means['R_mttf_red'] - R_means['R_mttf_true']) / R_means['R_mttf_true']

    means = means.merge(R_means[['target_cv', 'n', 'R_bias_full_pct', 'R_bias_red_pct']],
                        on=['target_cv', 'n'])

    # LRT rejection rate
    lrt = groups.agg(
        reject_rate=('p_value', lambda x: (x < 0.05).mean()),
    ).reset_index()
    means = means.merge(lrt, on=['target_cv', 'n'])

    return means


summary = compute_summaries(df)
print("\n" + "=" * 70)
print("Summary statistics:")
print(summary.to_string(index=False))
summary.to_csv('summary_consequence.csv', index=False)

# =========================================================================
# Figure 1: Main consequence analysis (1x3 panel)
# =========================================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

sample_sizes = sorted(df['n'].unique())
colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(sample_sizes)))

# --- Panel (a): MTTF bias ---
ax = axes[0]
for i, n in enumerate(sample_sizes):
    sub = summary[summary['n'] == n]
    ax.plot(sub['actual_cv'] * 100, sub['bias_red_pct'],
            'o-', color=colors[i], label=f'Reduced (n={n})', markersize=4)
    ax.plot(sub['actual_cv'] * 100, sub['bias_full_pct'],
            's--', color=colors[i], alpha=0.4, markersize=3)
ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
ax.axhline(y=1, color='red', linestyle=':', alpha=0.3, label='1% bias')
ax.axhline(y=-1, color='red', linestyle=':', alpha=0.3)
ax.set_xlabel('Shape CV (%)')
ax.set_ylabel('MTTF Bias (%)')
ax.set_title('(a) MTTF Estimation Bias')
ax.legend(fontsize=7, loc='upper left')
ax.grid(True, alpha=0.3)

# --- Panel (b): RMSE comparison ---
ax = axes[1]
for i, n in enumerate(sample_sizes):
    sub = summary[summary['n'] == n]
    ax.plot(sub['actual_cv'] * 100, sub['rmse_red_pct'],
            'o-', color=colors[i], label=f'Reduced (n={n})', markersize=4)
    ax.plot(sub['actual_cv'] * 100, sub['rmse_full_pct'],
            's--', color=colors[i], alpha=0.5, markersize=3)
# Mark where they diverge
ax.set_xlabel('Shape CV (%)')
ax.set_ylabel('RMSE (% of true MTTF)')
ax.set_title('(b) RMSE: Full (dashed) vs Reduced (solid)')
ax.legend(fontsize=7, loc='upper left')
ax.grid(True, alpha=0.3)

# --- Panel (c): Relative efficiency ---
ax = axes[2]
for i, n in enumerate(sample_sizes):
    sub = summary[summary['n'] == n]
    ax.plot(sub['actual_cv'] * 100, sub['rel_eff'],
            'o-', color=colors[i], label=f'n={n}', markersize=5, linewidth=2)
ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='Equal MSE')
ax.set_xlabel('Shape CV (%)')
ax.set_ylabel('MSE(Full) / MSE(Reduced)')
ax.set_title('(c) Relative Efficiency')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 1.2)

plt.tight_layout()
fig.savefig('consequence_analysis.pdf', bbox_inches='tight')
fig.savefig(PAPER_IMAGE / 'consequence_analysis.pdf', bbox_inches='tight')
print("\nMain figure saved to consequence_analysis.pdf")

# =========================================================================
# Figure 2: Focused consequence plot for the paper (single panel)
# =========================================================================
fig2, ax = plt.subplots(1, 1, figsize=(7, 5))

# Plot MTTF bias of reduced model vs CV, with rejection rate on secondary axis
ax2 = ax.twinx()

n_focus = 500  # Focus on moderate sample size
sub = summary[summary['n'] == n_focus]

# Left axis: bias
l1 = ax.plot(sub['actual_cv'] * 100, sub['bias_red_pct'],
             'o-', color='tab:blue', linewidth=2, markersize=6,
             label='MTTF bias (reduced model)')
ax.fill_between(sub['actual_cv'] * 100, -1, 1, alpha=0.1, color='green',
                label='Acceptable bias (< 1%)')
ax.axhline(y=0, color='black', linestyle='-', alpha=0.2)

# Right axis: rejection rate
l2 = ax2.plot(sub['actual_cv'] * 100, sub['reject_rate'],
              's--', color='tab:red', linewidth=2, markersize=6,
              label='LRT rejection rate')
ax2.axhline(y=0.05, color='tab:red', linestyle=':', alpha=0.3)

ax.set_xlabel('Coefficient of Variation of Shape Parameters (%)', fontsize=11)
ax.set_ylabel('MTTF Bias of Reduced Model (%)', color='tab:blue', fontsize=11)
ax2.set_ylabel('LRT Rejection Rate', color='tab:red', fontsize=11)

ax.tick_params(axis='y', labelcolor='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:red')
ax2.set_ylim(0, 1.05)

# Combined legend
lines = l1 + l2
labels = [l.get_label() for l in lines]
ax.legend(lines, labels, loc='upper left', fontsize=9)

ax.set_title(f'Consequence of Model Misspecification (n={n_focus})', fontsize=12)
ax.grid(True, alpha=0.3)

fig2.tight_layout()
fig2.savefig('consequence_focused.pdf', bbox_inches='tight')
fig2.savefig(PAPER_IMAGE / 'consequence_focused.pdf', bbox_inches='tight')
print("Focused figure saved to consequence_focused.pdf")

# =========================================================================
# Print key findings for the paper
# =========================================================================
print("\n" + "=" * 70)
print("KEY FINDINGS FOR PAPER:")
print("=" * 70)

for n in sample_sizes:
    sub = summary[summary['n'] == n]
    print(f"\nn = {n}:")
    for _, row in sub.iterrows():
        cv_pct = row['actual_cv'] * 100
        print(f"  CV={cv_pct:5.1f}%: bias_red={row['bias_red_pct']:+6.2f}%, "
              f"rmse_full={row['rmse_full']:.1f}, rmse_red={row['rmse_red']:.1f}, "
              f"rel_eff={row['rel_eff']:.3f}, reject={row['reject_rate']:.3f}")

# Crossover point: where does reduced model become worse than full?
print("\n" + "=" * 70)
print("MTTF bias exceeds 1% threshold:")
for n in sample_sizes:
    sub = summary[(summary['n'] == n) & (abs(summary['bias_red_pct']) > 1.0)]
    if not sub.empty:
        min_cv = sub['actual_cv'].min()
        print(f"  n={n:5d}: first exceeds at CV = {min_cv*100:.1f}%")
    else:
        print(f"  n={n:5d}: never exceeds 1% bias")

print("\n" + "=" * 70)
print("LaTeX table (MTTF consequence by CV):")
print("\\begin{tabular}{c" + "cc" * len(sample_sizes) + "}")
print("\\toprule")
print("& \\multicolumn{" + str(2*len(sample_sizes)) + "}{c}{Sample Size} \\\\")
ns_header = " & ".join([f"\\multicolumn{{2}}{{c}}{{$n={n}$}}" for n in sample_sizes])
print(f"CV (\\%) & {ns_header} \\\\")
sub_header = " & ".join(["Bias (\\%) & RMSE"] * len(sample_sizes))
print(f"& {sub_header} \\\\")
print("\\midrule")
for cv in sorted(summary['target_cv'].unique()):
    vals = []
    for n in sample_sizes:
        row = summary[(summary['target_cv'] == cv) & (summary['n'] == n)]
        if not row.empty:
            vals.append(f"{row['bias_red_pct'].values[0]:+.1f} & {row['rmse_red'].values[0]:.1f}")
        else:
            vals.append("-- & --")
    actual = summary[summary['target_cv'] == cv]['actual_cv'].iloc[0]
    print(f"{actual*100:.1f} & " + " & ".join(vals) + " \\\\")
print("\\bottomrule")
print("\\end{tabular}")

plt.show()
