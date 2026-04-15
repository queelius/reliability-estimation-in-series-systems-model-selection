#!/usr/bin/env python3
"""
Analyze LRT results: Effect of shape heterogeneity (CV) on rejection rate.

At CV=0 (perfect homogeneity): rejection rate = Type I error ~ alpha
At CV>0: rejection rate = Power to detect heterogeneity
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
df = pd.read_csv('../data-lrt-divergence.csv')

# Significance level
alpha = 0.05

# Check if AIC/BIC columns are present
has_ic = 'aic_F' in df.columns and 'aic_R' in df.columns

if has_ic:
    df['aic_selects_full'] = df['aic_F'] < df['aic_R']
    df['bic_selects_full'] = df['bic_F'] < df['bic_R']

# Compute rejection rate by (target_cv, n)
agg_dict = dict(
    reject_rate=('p_value', lambda x: (x < alpha).mean()),
    n_reps=('p_value', 'count'),
    mean_lambda=('Lambda', 'mean'),
    sd_lambda=('Lambda', 'std'),
    actual_cv=('actual_cv', 'first'),
    maxmin_ratio=('maxmin_ratio', 'first')
)
if has_ic:
    agg_dict['aic_selects_full_rate'] = ('aic_selects_full', 'mean')
    agg_dict['bic_selects_full_rate'] = ('bic_selects_full', 'mean')

summary = df.groupby(['target_cv', 'n']).agg(**agg_dict).reset_index()

# Standard error for rejection rate (binomial) -- kept for print statements
summary['se_reject'] = np.sqrt(summary['reject_rate'] * (1 - summary['reject_rate']) / summary['n_reps'])

# Wilson confidence intervals
wilson_results = summary.apply(lambda row: wilson_ci(row['reject_rate'], row['n_reps']), axis=1)
summary['ci_low'] = wilson_results.apply(lambda x: x[0])
summary['ci_high'] = wilson_results.apply(lambda x: x[1])

print("LRT Rejection Rate by Shape Heterogeneity (CV)")
print("=" * 70)
print(f"Nominal alpha = {alpha}")
print(f"At CV=0: rejection rate ~ alpha (Type I error)")
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
    yerr_low = np.clip(sub['reject_rate'] - sub['ci_low'], 0, None)
    yerr_high = np.clip(sub['ci_high'] - sub['reject_rate'], 0, None)
    ax1.errorbar(sub['actual_cv'] * 100, sub['reject_rate'],
                 yerr=[yerr_low.values, yerr_high.values],
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
    yerr_low = np.clip(sub['reject_rate'] - sub['ci_low'], 0, None)
    yerr_high = np.clip(sub['ci_high'] - sub['reject_rate'], 0, None)
    ax3.errorbar(sub['actual_cv'] * 100, sub['reject_rate'],
                 yerr=[yerr_low.values, yerr_high.values],
                 marker='o', label=f'n={n}', capsize=3)

ax3.axhline(y=alpha, color='red', linestyle='--', label=f'Nominal alpha={alpha}')
ax3.axhline(y=0.10, color='orange', linestyle=':', alpha=0.5, label='2*alpha')
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
plt.savefig(PAPER_IMAGE / 'lrt_divergence_analysis.pdf', bbox_inches='tight')
print("\nFigure saved to lrt_divergence_analysis.pdf")

# Detailed Type I error analysis at CV=0
print("\n" + "=" * 70)
print("Type I Error Analysis (CV = 0, perfect homogeneity):")
cv0 = summary[summary['target_cv'] == 0]
if not cv0.empty:
    for _, row in cv0.iterrows():
        ci_low = row['ci_low']
        ci_high = row['ci_high']
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

# --- AIC/BIC comparison figure ---
if has_ic:
    ic_summary = df.groupby(['target_cv', 'n']).agg(
        aic_selects_full=('aic_selects_full', 'mean'),
        bic_selects_full=('bic_selects_full', 'mean'),
        reject_rate=('p_value', lambda x: (x < alpha).mean()),
        n_reps=('p_value', 'count')
    ).reset_index()

    # Plot: LRT vs AIC vs BIC for each n
    fig_ic, axes_ic = plt.subplots(1, 2, figsize=(14, 5))

    # Left: All three criteria vs CV for n=1000
    ax = axes_ic[0]
    for n_val in [1000]:
        sub = ic_summary[ic_summary['n'] == n_val]
        ax.plot(sub['target_cv'] * 100, sub['reject_rate'], 'o-', label='LRT rejects H0', linewidth=2)
        ax.plot(sub['target_cv'] * 100, sub['aic_selects_full'], 's--', label='AIC selects full', linewidth=2)
        ax.plot(sub['target_cv'] * 100, sub['bic_selects_full'], '^:', label='BIC selects full', linewidth=2)
    ax.axhline(y=alpha, color='red', linestyle='--', alpha=0.3, label=f'alpha={alpha}')
    ax.set_xlabel('CV of Shapes (%)')
    ax.set_ylabel('Rate')
    ax.set_title(f'Model Selection Comparison (n=1000)')
    ax.legend()
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)

    # Right: Type I error comparison (CV=0)
    ax = axes_ic[1]
    cv0 = ic_summary[ic_summary['target_cv'] == 0]
    if not cv0.empty:
        x = range(len(cv0))
        width = 0.25
        ax.bar([i - width for i in x], cv0['reject_rate'], width, label='LRT')
        ax.bar(x, cv0['aic_selects_full'], width, label='AIC')
        ax.bar([i + width for i in x], cv0['bic_selects_full'], width, label='BIC')
        ax.set_xticks(list(x))
        ax.set_xticklabels([f'n={int(n)}' for n in cv0['n']])
        ax.axhline(y=alpha, color='red', linestyle='--', alpha=0.5)
        ax.set_ylabel('Rate selecting full model / rejecting H0')
        ax.set_title('Type I Error Comparison (CV=0)')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

    fig_ic.tight_layout()
    fig_ic.savefig('lrt_vs_aic_bic_divergence.pdf', bbox_inches='tight')
    fig_ic.savefig(PAPER_IMAGE / 'lrt_vs_aic_bic_divergence.pdf', bbox_inches='tight')
    print("\nAIC/BIC comparison figure saved")

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
