#!/usr/bin/env python3
"""
Analyze LRT results: Effect of censoring quantile (q) on type I error rate.
Under H0 (well-designed system with homogeneous shapes), rejection rate should be ~alpha.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read data
df = pd.read_csv('../data-lrt-vary-q.csv')

# Significance level
alpha = 0.05

# Compute rejection rate by (q, n)
summary = df.groupby(['q', 'n']).agg(
    reject_rate=('p_value', lambda x: (x < alpha).mean()),
    n_reps=('p_value', 'count'),
    mean_lambda=('Lambda', 'mean'),
    sd_lambda=('Lambda', 'std'),
    mean_pct_censored=('pct_censored', 'mean')
).reset_index()

# Standard error for rejection rate (binomial)
summary['se_reject'] = np.sqrt(summary['reject_rate'] * (1 - summary['reject_rate']) / summary['n_reps'])

print("LRT Type I Error Rate by Censoring Quantile (q)")
print("=" * 60)
print(f"Nominal alpha = {alpha}")
print(f"Expected rejection rate under H0: {alpha}")
print()
print(summary.to_string(index=False))

# Save summary
summary.to_csv('summary_vary_q.csv', index=False)

# Create figure: Rejection rate vs q
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Rejection rate vs q (lines for each n)
ax1 = axes[0]
for n in sorted(df['n'].unique()):
    sub = summary[summary['n'] == n]
    ax1.errorbar(sub['q'], sub['reject_rate'], yerr=1.96*sub['se_reject'],
                 marker='o', label=f'n={n}', capsize=3)

ax1.axhline(y=alpha, color='red', linestyle='--', label=f'Nominal alpha={alpha}')
ax1.set_xlabel('Censoring Quantile (q)')
ax1.set_ylabel('Rejection Rate')
ax1.set_title('Type I Error Rate vs Censoring Level')
ax1.legend(loc='best')
ax1.set_ylim(0, 0.15)
ax1.grid(True, alpha=0.3)

# Plot 2: Heatmap of rejection rates
pivot = summary.pivot(index='q', columns='n', values='reject_rate')
ax2 = axes[1]
sns.heatmap(pivot, annot=True, fmt='.3f', cmap='RdYlGn_r', center=alpha,
            vmin=0, vmax=0.15, ax=ax2, cbar_kws={'label': 'Rejection Rate'})
ax2.set_title('Rejection Rate Heatmap')
ax2.set_xlabel('Sample Size (n)')
ax2.set_ylabel('Censoring Quantile (q)')

plt.tight_layout()
plt.savefig('lrt_vary_q_rejection_rate.pdf', bbox_inches='tight')
plt.savefig('/home/spinoza/github/rlang/reliability-estimation-in-series-systems-model-selection/image/lrt_vary_q_rejection_rate.pdf', bbox_inches='tight')
print("\nFigure saved to lrt_vary_q_rejection_rate.pdf")

# Additional plot: Rejection rate vs actual censoring percentage
fig2, ax = plt.subplots(figsize=(8, 5))
for n in sorted(df['n'].unique()):
    sub = summary[summary['n'] == n]
    ax.scatter(1 - sub['mean_pct_censored'], sub['reject_rate'], label=f'n={n}', s=60)

ax.axhline(y=alpha, color='red', linestyle='--', label=f'Nominal alpha={alpha}')
ax.set_xlabel('Proportion Observed (1 - censoring rate)')
ax.set_ylabel('Rejection Rate')
ax.set_title('Type I Error Rate vs Information Content')
ax.legend(loc='best')
ax.set_ylim(0, 0.15)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('lrt_vary_q_vs_censoring.pdf', bbox_inches='tight')

print("\n" + "=" * 60)
print("Censoring summary:")
cens_summary = summary.groupby('q')['mean_pct_censored'].mean()
for q, pct in cens_summary.items():
    print(f"  q={q}: mean censoring = {pct:.1%}")

plt.show()
