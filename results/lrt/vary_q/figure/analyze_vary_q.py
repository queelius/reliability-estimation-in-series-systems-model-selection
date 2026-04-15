#!/usr/bin/env python3
"""
Analyze LRT results: Effect of censoring quantile (q) on type I error rate.
Under H0 (well-designed system with homogeneous shapes), rejection rate should be ~alpha.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --- Path setup ---
SCRIPT_DIR = Path(__file__).resolve().parent
PAPER_IMAGE = SCRIPT_DIR.parents[3] / 'paper' / 'image'
PAPER_IMAGE.mkdir(parents=True, exist_ok=True)


def wilson_ci(p_hat, n, z=1.96):
    """Wilson score confidence interval for a proportion."""
    denom = 1 + z**2 / n
    center = (p_hat + z**2 / (2*n)) / denom
    margin = z * np.sqrt(p_hat * (1 - p_hat) / n + z**2 / (4*n**2)) / denom
    return max(0, center - margin), min(1, center + margin)


# Read data
df = pd.read_csv('../data-lrt-vary-q.csv')

# Significance level
alpha = 0.05

# Check if AIC/BIC columns are present
has_ic = 'aic_F' in df.columns and 'aic_R' in df.columns

if has_ic:
    df['aic_selects_full'] = df['aic_F'] < df['aic_R']
    df['bic_selects_full'] = df['bic_F'] < df['bic_R']

# Compute rejection rate by (q, n)
agg_dict = dict(
    reject_rate=('p_value', lambda x: (x < alpha).mean()),
    n_reps=('p_value', 'count'),
    mean_lambda=('Lambda', 'mean'),
    sd_lambda=('Lambda', 'std'),
    mean_pct_censored=('pct_censored', 'mean')
)
if has_ic:
    agg_dict['aic_selects_full_rate'] = ('aic_selects_full', 'mean')
    agg_dict['bic_selects_full_rate'] = ('bic_selects_full', 'mean')

summary = df.groupby(['q', 'n']).agg(**agg_dict).reset_index()

# Standard error for rejection rate (binomial) -- kept for print statements
summary['se_reject'] = np.sqrt(summary['reject_rate'] * (1 - summary['reject_rate']) / summary['n_reps'])

# Wilson confidence intervals
wilson_results = summary.apply(lambda row: wilson_ci(row['reject_rate'], row['n_reps']), axis=1)
summary['ci_low'] = wilson_results.apply(lambda x: x[0])
summary['ci_high'] = wilson_results.apply(lambda x: x[1])

print("LRT Rejection Rate by Censoring Quantile (q)")
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
    yerr_low = sub['reject_rate'] - sub['ci_low']
    yerr_high = sub['ci_high'] - sub['reject_rate']
    ax1.errorbar(sub['q'], sub['reject_rate'],
                 yerr=[yerr_low.values, yerr_high.values],
                 marker='o', label=f'n={n}', capsize=3)

ax1.axhline(y=alpha, color='red', linestyle='--', label=f'Nominal alpha={alpha}')
ax1.set_xlabel('Censoring Quantile (q)')
ax1.set_ylabel('Rejection Rate')
ax1.set_title('Rejection Rate vs Censoring Level')
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
plt.savefig(PAPER_IMAGE / 'lrt_vary_q_rejection_rate.pdf', bbox_inches='tight')
print("\nFigure saved to lrt_vary_q_rejection_rate.pdf")

# --- AIC/BIC comparison figure ---
if has_ic:
    ic_summary = df.groupby(['q', 'n']).agg(
        aic_selects_full=('aic_selects_full', 'mean'),
        bic_selects_full=('bic_selects_full', 'mean'),
        reject_rate=('p_value', lambda x: (x < alpha).mean()),
        n_reps=('p_value', 'count')
    ).reset_index()

    fig_ic, ax = plt.subplots(figsize=(8, 5))
    for n_val in [500, 5000]:
        sub = ic_summary[ic_summary['n'] == n_val]
        ax.plot(sub['q'], sub['reject_rate'], 'o-', label=f'LRT (n={n_val})', linewidth=2)
        ax.plot(sub['q'], sub['aic_selects_full'], 's--', label=f'AIC (n={n_val})', linewidth=1.5)
        ax.plot(sub['q'], sub['bic_selects_full'], '^:', label=f'BIC (n={n_val})', linewidth=1.5)
    ax.axhline(y=alpha, color='red', linestyle='--', alpha=0.3)
    ax.set_xlabel('Censoring Quantile (q)')
    ax.set_ylabel('Rate')
    ax.set_title('Model Selection: LRT vs AIC vs BIC')
    ax.legend(loc='best')
    ax.set_ylim(0, 0.20)
    ax.grid(True, alpha=0.3)
    fig_ic.tight_layout()
    fig_ic.savefig('lrt_vs_aic_bic_vary_q.pdf', bbox_inches='tight')
    fig_ic.savefig(PAPER_IMAGE / 'lrt_vs_aic_bic_vary_q.pdf', bbox_inches='tight')
    print("\nAIC/BIC comparison figure saved")

# Additional plot: Rejection rate vs actual censoring percentage
fig2, ax = plt.subplots(figsize=(8, 5))
for n in sorted(df['n'].unique()):
    sub = summary[summary['n'] == n]
    ax.scatter(1 - sub['mean_pct_censored'], sub['reject_rate'], label=f'n={n}', s=60)

ax.axhline(y=alpha, color='red', linestyle='--', label=f'Nominal alpha={alpha}')
ax.set_xlabel('Proportion Observed (1 - censoring rate)')
ax.set_ylabel('Rejection Rate')
ax.set_title('Rejection Rate vs Information Content')
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
