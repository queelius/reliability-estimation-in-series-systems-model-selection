#!/usr/bin/env python3
"""
Analyze adaptive model selection results.

Compares four strategies:
  1. Always-full:    always use full model estimates
  2. Always-reduced: always use reduced model estimates
  3. Adaptive-LRT:   fit full -> LRT -> decide
  4. Adaptive-CV:    fit full -> estimate CV -> decide

Key question: Does the adaptive procedure achieve near-oracle RMSE
by selecting the right model for each dataset?
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
df = pd.read_csv('../data-adaptive.csv')
print(f"Loaded {len(df)} rows")
print(f"CV values: {sorted(df['target_cv'].unique())}")
print(f"Sample sizes: {sorted(df['n'].unique())}")

# --- Compute summary statistics ---
groups = df.groupby(['target_cv', 'n'])

# Selection rates
sel = groups.agg(
    n_reps=('mttf_true', 'count'),
    mttf_true=('mttf_true', 'first'),
    actual_cv=('actual_cv', 'first'),
    lrt_selects_reduced=('selected_model_lrt', lambda x: (x == 'reduced').mean()),
    cv_selects_reduced=('selected_model_cv', lambda x: (x == 'reduced').mean()),
    mean_cv_hat=('cv_hat', 'mean'),
    sd_cv_hat=('cv_hat', 'std'),
).reset_index()

# MSE for each strategy
mse = groups.apply(lambda g: pd.Series({
    'mse_full': ((g['mttf_full'] - g['mttf_true'])**2).mean(),
    'mse_red': ((g['mttf_reduced'] - g['mttf_true'])**2).mean(),
    'mse_lrt': ((g['mttf_adaptive_lrt'] - g['mttf_true'])**2).mean(),
    'mse_cv': ((g['mttf_adaptive_cv'] - g['mttf_true'])**2).mean(),
})).reset_index()

summary = sel.merge(mse, on=['target_cv', 'n'])
summary['rmse_full'] = np.sqrt(summary['mse_full'])
summary['rmse_red'] = np.sqrt(summary['mse_red'])
summary['rmse_lrt'] = np.sqrt(summary['mse_lrt'])
summary['rmse_cv'] = np.sqrt(summary['mse_cv'])

# Relative RMSE (normalized by full model)
summary['rel_rmse_red'] = summary['rmse_red'] / summary['rmse_full']
summary['rel_rmse_lrt'] = summary['rmse_lrt'] / summary['rmse_full']
summary['rel_rmse_cv'] = summary['rmse_cv'] / summary['rmse_full']

# Bias
bias = groups.agg(
    bias_full=('mttf_full', lambda x: (x - x.name[1]).mean() if False else 0),
    bias_red=('mttf_reduced', lambda x: 0),
    bias_lrt=('mttf_adaptive_lrt', lambda x: 0),
).reset_index()
# Recompute properly
for strategy in ['full', 'reduced', 'adaptive_lrt', 'adaptive_cv']:
    col = f'mttf_{strategy}'
    bias_col = f'bias_{strategy}'
    summary[bias_col] = groups.apply(
        lambda g: (g[col] - g['mttf_true']).mean()
    ).reset_index(drop=True) if False else 0

# Proper bias computation
bias_data = []
for (cv, n), g in df.groupby(['target_cv', 'n']):
    true = g['mttf_true'].iloc[0]
    bias_data.append({
        'target_cv': cv, 'n': n,
        'bias_full': (g['mttf_full'] - true).mean(),
        'bias_red': (g['mttf_reduced'] - true).mean(),
        'bias_lrt': (g['mttf_adaptive_lrt'] - true).mean(),
        'bias_cv': (g['mttf_adaptive_cv'] - true).mean(),
    })
bias_df = pd.DataFrame(bias_data)
summary = summary.merge(bias_df, on=['target_cv', 'n'])

# RMSE as % of true MTTF
summary['rmse_full_pct'] = 100 * summary['rmse_full'] / summary['mttf_true']
summary['rmse_red_pct'] = 100 * summary['rmse_red'] / summary['mttf_true']
summary['rmse_lrt_pct'] = 100 * summary['rmse_lrt'] / summary['mttf_true']

print("\nSummary:")
print(summary[['target_cv', 'n', 'lrt_selects_reduced', 'rmse_full', 'rmse_red',
               'rmse_lrt', 'rmse_cv']].to_string(index=False))
summary.to_csv('summary_adaptive.csv', index=False)

# =========================================================================
# Figure 1: Main adaptive selection analysis (2x2 panel)
# =========================================================================
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

sample_sizes = sorted(df['n'].unique())
colors_n = {'100': 'tab:blue', '500': 'tab:orange', '1000': 'tab:green'}

# --- Panel (a): Selection rate ---
ax = axes[0, 0]
for n in sample_sizes:
    sub = summary[summary['n'] == n]
    ax.plot(sub['actual_cv'] * 100, sub['lrt_selects_reduced'],
            'o-', label=f'n={n}', markersize=5, linewidth=2)
ax.axhline(y=0.95, color='gray', linestyle=':', alpha=0.5, label='95% (1-alpha)')
ax.set_xlabel('Shape CV (%)')
ax.set_ylabel('Fraction Selecting Reduced Model')
ax.set_title('(a) LRT-Based Model Selection Rate')
ax.legend(fontsize=9)
ax.set_ylim(-0.05, 1.05)
ax.grid(True, alpha=0.3)

# --- Panel (b): RMSE comparison for n=500 ---
ax = axes[0, 1]
n_focus = 500
sub = summary[summary['n'] == n_focus]
ax.plot(sub['actual_cv'] * 100, sub['rmse_full'],
        's--', color='tab:blue', label='Always Full', linewidth=2, markersize=5)
ax.plot(sub['actual_cv'] * 100, sub['rmse_red'],
        'o--', color='tab:red', label='Always Reduced', linewidth=2, markersize=5)
ax.plot(sub['actual_cv'] * 100, sub['rmse_lrt'],
        'D-', color='tab:green', label='Adaptive (LRT)', linewidth=2.5, markersize=6)
ax.set_xlabel('Shape CV (%)')
ax.set_ylabel('RMSE (MTTF)')
ax.set_title(f'(b) RMSE Comparison (n={n_focus})')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# --- Panel (c): RMSE comparison for n=100 ---
ax = axes[1, 0]
n_focus = 100
sub = summary[summary['n'] == n_focus]
ax.plot(sub['actual_cv'] * 100, sub['rmse_full'],
        's--', color='tab:blue', label='Always Full', linewidth=2, markersize=5)
ax.plot(sub['actual_cv'] * 100, sub['rmse_red'],
        'o--', color='tab:red', label='Always Reduced', linewidth=2, markersize=5)
ax.plot(sub['actual_cv'] * 100, sub['rmse_lrt'],
        'D-', color='tab:green', label='Adaptive (LRT)', linewidth=2.5, markersize=6)
ax.set_xlabel('Shape CV (%)')
ax.set_ylabel('RMSE (MTTF)')
ax.set_title(f'(c) RMSE Comparison (n={n_focus})')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# --- Panel (d): Relative RMSE vs always-full ---
ax = axes[1, 1]
for n in sample_sizes:
    sub = summary[summary['n'] == n]
    ax.plot(sub['actual_cv'] * 100, sub['rel_rmse_lrt'],
            'o-', label=f'Adaptive/Full (n={n})', markersize=5, linewidth=2)
ax.axhline(y=1.0, color='black', linestyle='--', alpha=0.3, label='Equal to Full')
ax.set_xlabel('Shape CV (%)')
ax.set_ylabel('RMSE(Adaptive) / RMSE(Full)')
ax.set_title('(d) Adaptive RMSE Relative to Full Model')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

plt.tight_layout()
fig.savefig('adaptive_selection.pdf', bbox_inches='tight')
fig.savefig(PAPER_IMAGE / 'adaptive_selection.pdf', bbox_inches='tight')
print("\nMain figure saved")

# =========================================================================
# Figure 2: Focused plot for paper (single panel, n=500)
# =========================================================================
fig2, ax = plt.subplots(1, 1, figsize=(7, 5))

n_focus = 500
sub = summary[summary['n'] == n_focus]

ax.plot(sub['actual_cv'] * 100, sub['rmse_full_pct'],
        's--', color='tab:blue', label='Always Full', linewidth=2, markersize=6)
ax.plot(sub['actual_cv'] * 100, sub['rmse_red_pct'],
        'o--', color='tab:red', label='Always Reduced', linewidth=2, markersize=6)
ax.plot(sub['actual_cv'] * 100, sub['rmse_lrt_pct'],
        'D-', color='tab:green', label='Adaptive (LRT)', linewidth=2.5, markersize=7)

# Shade regions
ax.axvspan(0, 5, alpha=0.05, color='green', label='CV < 5% (reduced safe)')
ax.axvspan(5, 10, alpha=0.05, color='yellow')

ax.set_xlabel('Coefficient of Variation of Shape Parameters (%)', fontsize=11)
ax.set_ylabel('RMSE (% of true MTTF)', fontsize=11)
ax.set_title(f'Adaptive Model Selection Performance (n={n_focus})', fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

fig2.tight_layout()
fig2.savefig('adaptive_focused.pdf', bbox_inches='tight')
fig2.savefig(PAPER_IMAGE / 'adaptive_focused.pdf', bbox_inches='tight')
print("Focused figure saved")

# =========================================================================
# Print key findings
# =========================================================================
print("\n" + "=" * 70)
print("KEY FINDINGS:")
print("=" * 70)

# Type I error of adaptive procedure (CV=0)
print("\nType I error (model selection at CV=0):")
cv0 = summary[summary['target_cv'] == 0]
for _, row in cv0.iterrows():
    print(f"  n={int(row['n']):5d}: LRT selects full {1-row['lrt_selects_reduced']:.1%} "
          f"(should be ~{0.05:.0%})")

# Adaptive RMSE improvement
print("\nAdaptive vs Always-Full (RMSE ratio, <1 means adaptive better):")
for n in sample_sizes:
    sub = summary[summary['n'] == n]
    print(f"\n  n={n}:")
    for _, row in sub.iterrows():
        cv_pct = row['actual_cv'] * 100
        print(f"    CV={cv_pct:5.1f}%: adaptive/full = {row['rel_rmse_lrt']:.3f}, "
              f"reduced/full = {row['rel_rmse_red']:.3f}")

# When does adaptive match full?
print("\nAdaptive achieves < 2% RMSE overhead vs full model:")
for n in sample_sizes:
    sub = summary[(summary['n'] == n) & (summary['rel_rmse_lrt'] < 1.02)]
    if not sub.empty:
        max_cv = sub['actual_cv'].max()
        print(f"  n={n:5d}: up to CV = {max_cv*100:.1f}%")

# LaTeX table
print("\n" + "=" * 70)
print("LaTeX table:")
print("\\begin{tabular}{cccccc}")
print("\\toprule")
print("CV (\\%) & $n$ & \\multicolumn{3}{c}{RMSE (\\% of true MTTF)} & Sel.~Reduced \\\\")
print("& & Full & Reduced & Adaptive & (\\%) \\\\")
print("\\midrule")
for cv in sorted(summary['target_cv'].unique()):
    for i, n in enumerate(sample_sizes):
        row = summary[(summary['target_cv'] == cv) & (summary['n'] == n)]
        if row.empty:
            continue
        r = row.iloc[0]
        cv_str = f"{r['actual_cv']*100:.1f}" if i == 0 else ""
        print(f"{cv_str} & {n} & {r['rmse_full_pct']:.1f} & {r['rmse_red_pct']:.1f} "
              f"& {r['rmse_lrt_pct']:.1f} & {r['lrt_selects_reduced']*100:.0f} \\\\")
    if cv != sorted(summary['target_cv'].unique())[-1]:
        print("\\addlinespace")
print("\\bottomrule")
print("\\end{tabular}")

plt.show()
