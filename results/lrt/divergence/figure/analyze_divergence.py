#!/usr/bin/env python3
"""
Analyze LRT results: Effect of shape heterogeneity (CV) on rejection rate.

At CV=0 (perfect homogeneity): rejection rate = Type I error ≈ alpha
At CV>0: rejection rate = Power to detect heterogeneity
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read data
df = pd.read_csv('../data-lrt-divergence.csv')

# Significance level
alpha = 0.05

# Compute rejection rate by (target_cv, n)
summary = df.groupby(['target_cv', 'n']).agg(
    reject_rate=('p_value', lambda x: (x < alpha).mean()),
    n_reps=('p_value', 'count'),
    mean_lambda=('Lambda', 'mean'),
    sd_lambda=('Lambda', 'std'),
    actual_cv=('actual_cv', 'first'),
    maxmin_ratio=('maxmin_ratio', 'first')
).reset_index()

# Standard error for rejection rate (binomial)
summary['se_reject'] = np.sqrt(summary['reject_rate'] * (1 - summary['reject_rate']) / summary['n_reps'])

print("LRT Rejection Rate by Shape Heterogeneity (CV)")
print("=" * 70)
print(f"Nominal alpha = {alpha}")
print(f"At CV=0: rejection rate ≈ alpha (Type I error)")
print(f"At CV>0: rejection rate = power to detect heterogeneity")
print()
print(summary.to_string(index=False))

# Save summary
summary.to_csv('summary_divergence.csv', index=False)

# Create figures
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Rejection rate vs actual CV (lines for each n)
ax1 = axes[0, 0]
for n in sorted(df['n'].unique()):
    sub = summary[summary['n'] == n]
    ax1.errorbar(sub['actual_cv'] * 100, sub['reject_rate'], yerr=1.96*sub['se_reject'],
                 marker='o', label=f'n={n}', capsize=3)

ax1.axhline(y=alpha, color='red', linestyle='--', alpha=0.5, label=f'Nominal alpha={alpha}')
ax1.set_xlabel('Coefficient of Variation of Shapes (%)')
ax1.set_ylabel('Rejection Rate')
ax1.set_title('LRT Rejection Rate vs Shape Heterogeneity')
ax1.legend(loc='best')
ax1.set_ylim(0, 1.05)
ax1.grid(True, alpha=0.3)

# Plot 2: Heatmap of rejection rates
pivot = summary.pivot(index='target_cv', columns='n', values='reject_rate')
ax2 = axes[0, 1]
sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn_r', center=0.5,
            vmin=0, vmax=1, ax=ax2, cbar_kws={'label': 'Rejection Rate'})
ax2.set_title('Rejection Rate Heatmap')
ax2.set_xlabel('Sample Size (n)')
ax2.set_ylabel('Target CV')

# Plot 3: Focus on low CV (Type I error region)
ax3 = axes[1, 0]
low_cv = summary[summary['target_cv'] <= 0.04]
for n in sorted(low_cv['n'].unique()):
    sub = low_cv[low_cv['n'] == n]
    ax3.errorbar(sub['actual_cv'] * 100, sub['reject_rate'], yerr=1.96*sub['se_reject'],
                 marker='o', label=f'n={n}', capsize=3)

ax3.axhline(y=alpha, color='red', linestyle='--', label=f'Nominal alpha={alpha}')
ax3.axhline(y=0.10, color='orange', linestyle=':', alpha=0.5, label='2×alpha')
ax3.set_xlabel('Coefficient of Variation of Shapes (%)')
ax3.set_ylabel('Rejection Rate')
ax3.set_title('Type I Error Region (Low CV)')
ax3.legend(loc='best')
ax3.set_ylim(0, 0.20)
ax3.grid(True, alpha=0.3)

# Plot 4: Power curves for different sample sizes
ax4 = axes[1, 1]
for n in sorted(df['n'].unique()):
    sub = summary[summary['n'] == n]
    ax4.plot(sub['actual_cv'] * 100, sub['reject_rate'],
             marker='o', label=f'n={n}', linewidth=2)

ax4.axhline(y=0.80, color='green', linestyle=':', alpha=0.5, label='80% power')
ax4.set_xlabel('Coefficient of Variation of Shapes (%)')
ax4.set_ylabel('Rejection Rate (Power)')
ax4.set_title('Power Curves by Sample Size')
ax4.legend(loc='best')
ax4.set_ylim(0, 1.05)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('lrt_divergence_analysis.pdf', bbox_inches='tight')
plt.savefig('/home/spinoza/github/rlang/reliability-estimation-in-series-systems-model-selection/image/lrt_divergence_analysis.pdf', bbox_inches='tight')
print("\nFigure saved to lrt_divergence_analysis.pdf")

# Detailed Type I error analysis at CV=0
print("\n" + "=" * 70)
print("Type I Error Analysis (CV = 0, perfect homogeneity):")
cv0 = summary[summary['target_cv'] == 0]
if not cv0.empty:
    for _, row in cv0.iterrows():
        ci_low = row['reject_rate'] - 1.96 * row['se_reject']
        ci_high = row['reject_rate'] + 1.96 * row['se_reject']
        contains_alpha = ci_low <= alpha <= ci_high
        status = "OK" if contains_alpha else "SIGNIFICANT"
        print(f"  n={int(row['n']):5d}: {row['reject_rate']:.3f} [{ci_low:.3f}, {ci_high:.3f}] {status}")

# Power analysis: minimum CV to achieve 80% power
print("\n" + "=" * 70)
print("Minimum CV for 80% power by sample size:")
for n in sorted(df['n'].unique()):
    sub = summary[(summary['n'] == n) & (summary['reject_rate'] >= 0.80)]
    if not sub.empty:
        min_cv = sub['actual_cv'].min()
        print(f"  n={n:5d}: CV = {min_cv*100:.1f}%")
    else:
        print(f"  n={n:5d}: 80% power not achieved")

# LaTeX table for paper
print("\n" + "=" * 70)
print("LaTeX table (rejection rates by CV and n):")
print("\\begin{tabular}{cc" + "c" * len(df['n'].unique()) + "}")
print("\\toprule")
print("Target & Actual & \\multicolumn{" + str(len(df['n'].unique())) + "}{c}{Sample Size (n)} \\\\")
ns = sorted(df['n'].unique())
print("CV & CV & " + " & ".join([str(int(n)) for n in ns]) + " \\\\")
print("\\midrule")
for cv in sorted(summary['target_cv'].unique()):
    sub = summary[summary['target_cv'] == cv]
    actual = sub['actual_cv'].iloc[0]
    rates = []
    for n in ns:
        r = sub[sub['n'] == n]['reject_rate'].values
        rates.append(f"{r[0]:.2f}" if len(r) > 0 else "-")
    print(f"{cv:.2f} & {actual:.3f} & " + " & ".join(rates) + " \\\\")
print("\\bottomrule")
print("\\end{tabular}")

plt.show()
