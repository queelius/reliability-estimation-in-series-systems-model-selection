#!/usr/bin/env python3
"""
Analyze LRT results: Effect of masking probability (p) on type I error rate.
Under H0 (well-designed system with homogeneous shapes), rejection rate should be ~alpha.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read data
df = pd.read_csv('../data-lrt-vary-p.csv')

# Significance level
alpha = 0.05

# Compute rejection rate by (p, n)
summary = df.groupby(['p', 'n']).agg(
    reject_rate=('p_value', lambda x: (x < alpha).mean()),
    n_reps=('p_value', 'count'),
    mean_lambda=('Lambda', 'mean'),
    sd_lambda=('Lambda', 'std')
).reset_index()

# Standard error for rejection rate (binomial)
summary['se_reject'] = np.sqrt(summary['reject_rate'] * (1 - summary['reject_rate']) / summary['n_reps'])

print("LRT Type I Error Rate by Masking Probability (p)")
print("=" * 60)
print(f"Nominal alpha = {alpha}")
print(f"Expected rejection rate under H0: {alpha}")
print()
print(summary.to_string(index=False))

# Save summary
summary.to_csv('summary_vary_p.csv', index=False)

# Create figure: Rejection rate vs p, faceted by n
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Rejection rate vs p (lines for each n)
ax1 = axes[0]
for n in sorted(df['n'].unique()):
    sub = summary[summary['n'] == n]
    ax1.errorbar(sub['p'], sub['reject_rate'], yerr=1.96*sub['se_reject'],
                 marker='o', label=f'n={n}', capsize=3)

ax1.axhline(y=alpha, color='red', linestyle='--', label=f'Nominal alpha={alpha}')
ax1.set_xlabel('Masking Probability (p)')
ax1.set_ylabel('Rejection Rate')
ax1.set_title('Type I Error Rate vs Masking Probability')
ax1.legend(loc='best')
ax1.set_ylim(0, 0.15)
ax1.grid(True, alpha=0.3)

# Plot 2: Heatmap of rejection rates
pivot = summary.pivot(index='p', columns='n', values='reject_rate')
ax2 = axes[1]
sns.heatmap(pivot, annot=True, fmt='.3f', cmap='RdYlGn_r', center=alpha,
            vmin=0, vmax=0.15, ax=ax2, cbar_kws={'label': 'Rejection Rate'})
ax2.set_title('Rejection Rate Heatmap')
ax2.set_xlabel('Sample Size (n)')
ax2.set_ylabel('Masking Probability (p)')

plt.tight_layout()
plt.savefig('lrt_vary_p_rejection_rate.pdf', bbox_inches='tight')
plt.savefig('/home/spinoza/github/rlang/reliability-estimation-in-series-systems-model-selection/image/lrt_vary_p_rejection_rate.pdf', bbox_inches='tight')
print("\nFigure saved to lrt_vary_p_rejection_rate.pdf")

# Additional analysis: Check if rejection rate is statistically different from alpha
print("\n" + "=" * 60)
print("Statistical test: Is rejection rate significantly different from alpha?")
print("(95% CI for rejection rate)")
print()
for _, row in summary.iterrows():
    ci_low = row['reject_rate'] - 1.96 * row['se_reject']
    ci_high = row['reject_rate'] + 1.96 * row['se_reject']
    contains_alpha = ci_low <= alpha <= ci_high
    status = "OK" if contains_alpha else "SIGNIFICANT"
    print(f"p={row['p']:.3f}, n={int(row['n']):5d}: {row['reject_rate']:.3f} [{ci_low:.3f}, {ci_high:.3f}] {status}")

plt.show()
