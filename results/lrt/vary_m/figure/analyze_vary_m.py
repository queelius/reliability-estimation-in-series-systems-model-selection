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
df = pd.read_csv('../data-lrt-vary-m.csv')

# Significance level
alpha = 0.05

# Check if AIC/BIC columns are present
has_ic = 'aic_F' in df.columns and 'aic_R' in df.columns

if has_ic:
    df['aic_selects_full'] = df['aic_F'] < df['aic_R']
    df['bic_selects_full'] = df['bic_F'] < df['bic_R']

# Compute rejection rate by (m, n)
agg_dict = dict(
    reject_rate=('p_value', lambda x: (x < alpha).mean()),
    n_reps=('p_value', 'count'),
    mean_lambda=('Lambda', 'mean'),
    sd_lambda=('Lambda', 'std'),
    df_lrt=('df_lrt', 'first'),
    cv_shapes=('cv_shapes', 'first')
)
if has_ic:
    agg_dict['aic_selects_full_rate'] = ('aic_selects_full', 'mean')
    agg_dict['bic_selects_full_rate'] = ('bic_selects_full', 'mean')

summary = df.groupby(['m', 'n']).agg(**agg_dict).reset_index()

# Standard error for rejection rate (binomial) -- kept for print statements
summary['se_reject'] = np.sqrt(summary['reject_rate'] * (1 - summary['reject_rate']) / summary['n_reps'])

# Expected mean of chi-squared is df
summary['expected_lambda'] = summary['df_lrt']

# Wilson confidence intervals
wilson_results = summary.apply(lambda row: wilson_ci(row['reject_rate'], row['n_reps']), axis=1)
summary['ci_low'] = wilson_results.apply(lambda x: x[0])
summary['ci_high'] = wilson_results.apply(lambda x: x[1])

print("LRT Rejection Rate by Number of Components (m)")
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
    yerr_low = sub['reject_rate'] - sub['ci_low']
    yerr_high = sub['ci_high'] - sub['reject_rate']
    ax1.errorbar(sub['m'], sub['reject_rate'],
                 yerr=[yerr_low.values, yerr_high.values],
                 marker='o', label=f'n={n}', capsize=3)

ax1.axhline(y=alpha, color='red', linestyle='--', label=f'Nominal alpha={alpha}')
ax1.set_xlabel('Number of Components (m)')
ax1.set_ylabel('Rejection Rate')
ax1.set_title('Rejection Rate vs System Complexity')
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
plt.savefig(PAPER_IMAGE / 'lrt_vary_m_rejection_rate.pdf', bbox_inches='tight')
print("\nFigure saved to lrt_vary_m_rejection_rate.pdf")

# --- AIC/BIC comparison figure ---
if has_ic:
    ic_summary = df.groupby(['m', 'n']).agg(
        aic_selects_full=('aic_selects_full', 'mean'),
        bic_selects_full=('bic_selects_full', 'mean'),
        reject_rate=('p_value', lambda x: (x < alpha).mean()),
        n_reps=('p_value', 'count')
    ).reset_index()

    fig_ic, ax = plt.subplots(figsize=(8, 5))
    for n_val in [500, 5000]:
        sub = ic_summary[ic_summary['n'] == n_val]
        ax.plot(sub['m'], sub['reject_rate'], 'o-', label=f'LRT (n={n_val})', linewidth=2)
        ax.plot(sub['m'], sub['aic_selects_full'], 's--', label=f'AIC (n={n_val})', linewidth=1.5)
        ax.plot(sub['m'], sub['bic_selects_full'], '^:', label=f'BIC (n={n_val})', linewidth=1.5)
    ax.axhline(y=alpha, color='red', linestyle='--', alpha=0.3)
    ax.set_xlabel('Number of Components (m)')
    ax.set_ylabel('Rate')
    ax.set_title('Model Selection: LRT vs AIC vs BIC')
    ax.legend(loc='best')
    ax.set_ylim(0, 0.20)
    ax.set_xticks(sorted(df['m'].unique()))
    ax.grid(True, alpha=0.3)
    fig_ic.tight_layout()
    fig_ic.savefig('lrt_vs_aic_bic_vary_m.pdf', bbox_inches='tight')
    fig_ic.savefig(PAPER_IMAGE / 'lrt_vs_aic_bic_vary_m.pdf', bbox_inches='tight')
    print("\nAIC/BIC comparison figure saved")

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
