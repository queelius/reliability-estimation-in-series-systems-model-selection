#!/usr/bin/env python3
"""
Analyze LRT results: Effect of number of components (m) on type I error rate.
Under H0 (well-designed system with homogeneous shapes), rejection rate should be ~alpha.
LRT degrees of freedom = m - 1.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read data
df = pd.read_csv('../data-lrt-vary-m.csv')

# Significance level
alpha = 0.05

# Compute rejection rate by (m, n)
summary = df.groupby(['m', 'n']).agg(
    reject_rate=('p_value', lambda x: (x < alpha).mean()),
    n_reps=('p_value', 'count'),
    mean_lambda=('Lambda', 'mean'),
    sd_lambda=('Lambda', 'std'),
    df_lrt=('df_lrt', 'first'),
    cv_shapes=('cv_shapes', 'first')
).reset_index()

# Standard error for rejection rate (binomial)
summary['se_reject'] = np.sqrt(summary['reject_rate'] * (1 - summary['reject_rate']) / summary['n_reps'])

# Expected mean of chi-squared is df
summary['expected_lambda'] = summary['df_lrt']

print("LRT Type I Error Rate by Number of Components (m)")
print("=" * 60)
print(f"Nominal alpha = {alpha}")
print(f"Expected rejection rate under H0: {alpha}")
print()
print(summary.to_string(index=False))

# Save summary
summary.to_csv('summary_vary_m.csv', index=False)

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: Rejection rate vs m (lines for each n)
ax1 = axes[0, 0]
for n in sorted(df['n'].unique()):
    sub = summary[summary['n'] == n]
    ax1.errorbar(sub['m'], sub['reject_rate'], yerr=1.96*sub['se_reject'],
                 marker='o', label=f'n={n}', capsize=3)

ax1.axhline(y=alpha, color='red', linestyle='--', label=f'Nominal alpha={alpha}')
ax1.set_xlabel('Number of Components (m)')
ax1.set_ylabel('Rejection Rate')
ax1.set_title('Type I Error Rate vs System Complexity')
ax1.legend(loc='best')
ax1.set_ylim(0, 0.15)
ax1.set_xticks(sorted(df['m'].unique()))
ax1.grid(True, alpha=0.3)

# Plot 2: Heatmap of rejection rates
pivot = summary.pivot(index='m', columns='n', values='reject_rate')
ax2 = axes[0, 1]
sns.heatmap(pivot, annot=True, fmt='.3f', cmap='RdYlGn_r', center=alpha,
            vmin=0, vmax=0.15, ax=ax2, cbar_kws={'label': 'Rejection Rate'})
ax2.set_title('Rejection Rate Heatmap')
ax2.set_xlabel('Sample Size (n)')
ax2.set_ylabel('Number of Components (m)')

# Plot 3: Mean Lambda vs expected (df)
ax3 = axes[1, 0]
for n in sorted(df['n'].unique()):
    sub = summary[summary['n'] == n]
    ax3.scatter(sub['df_lrt'], sub['mean_lambda'], label=f'n={n}', s=60, alpha=0.7)

# Add identity line (expected under H0: mean = df)
ax3.plot([0.5, 7.5], [0.5, 7.5], 'r--', label='Expected (mean = df)')
ax3.set_xlabel('Degrees of Freedom (m - 1)')
ax3.set_ylabel('Mean Lambda')
ax3.set_title('Mean Test Statistic vs Expected')
ax3.legend(loc='best')
ax3.grid(True, alpha=0.3)

# Plot 4: CV of shapes by m
ax4 = axes[1, 1]
cv_by_m = df.groupby('m')['cv_shapes'].first()
ax4.bar(cv_by_m.index, cv_by_m.values, color='steelblue', alpha=0.7)
ax4.set_xlabel('Number of Components (m)')
ax4.set_ylabel('CV of Shape Parameters')
ax4.set_title('Shape Heterogeneity by System Size')
ax4.set_xticks(sorted(df['m'].unique()))
ax4.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('lrt_vary_m_rejection_rate.pdf', bbox_inches='tight')
plt.savefig('/home/spinoza/github/rlang/reliability-estimation-in-series-systems-model-selection/image/lrt_vary_m_rejection_rate.pdf', bbox_inches='tight')
print("\nFigure saved to lrt_vary_m_rejection_rate.pdf")

# Summary table for paper
print("\n" + "=" * 60)
print("LaTeX table:")
print("\\begin{tabular}{ccccc}")
print("\\toprule")
print("$m$ & df & CV & \\multicolumn{2}{c}{Rejection Rate (n)} \\\\")
print("    &    &    & 100 & 5000 \\\\")
print("\\midrule")
for m in sorted(df['m'].unique()):
    sub = summary[summary['m'] == m]
    cv = sub['cv_shapes'].iloc[0]
    df_val = int(sub['df_lrt'].iloc[0])
    r100 = sub[sub['n'] == 100]['reject_rate'].values[0] if 100 in sub['n'].values else np.nan
    r5000 = sub[sub['n'] == 5000]['reject_rate'].values[0] if 5000 in sub['n'].values else np.nan
    print(f"{m} & {df_val} & {cv:.3f} & {r100:.3f} & {r5000:.3f} \\\\")
print("\\bottomrule")
print("\\end{tabular}")

plt.show()
