# Logic Checker Report

**Date**: 2026-02-25
**Paper**: "When Does Model Simplification Matter? Consequence Analysis for Weibull Series Systems"

## Summary

The paper's logical structure is generally sound. The main argument flows correctly: consequence analysis shows when misspecification matters, LRT characterization shows when it can be detected, and the adaptive procedure connects the two. However, there are several issues with specific claims that overstate what the data supports.

## Findings

### CRITICAL: Claim about 30,000 observations has no data support

- **Location**: Abstract (line 40), Section 6 Conclusion (line 473)
- **Quoted text**: "the common-shape model cannot be rejected at shape CV below 5% even with 30,000 observations" (abstract); "Even with sample sizes approaching 30,000" (conclusion)
- **Problem**: The maximum sample size in the simulation data is n=10,000. No simulations were run at n=30,000. At n=10,000 and CV=2.7% (the only data point below 5%), the rejection rate is 26.8%, which is far above the nominal 5%---this IS rejecting the null a substantial fraction of the time. Extrapolating to n=30,000 is unwarranted and likely wrong: at n=10,000, 27% rejection at CV=2.7% would increase well beyond 50% at n=30,000. The claim is not supported by the data and appears to be false.
- **Severity**: Critical
- **Suggestion**: Remove the "30,000" claim entirely. State the finding in terms of what the data shows: "At CV=2.7%, the LRT rejection rate is only 27% even at n=10,000, indicating limited practical power to detect such small departures."

### MAJOR: "Full model has lower MSE across ALL conditions" is contradicted at n=5000, CV=0

- **Location**: Section 3.4 (line 240)
- **Quoted text**: "the full model has lower MSE than the reduced model across all conditions---even when the reduced model is correctly specified (CV = 0)"
- **Problem**: At n=5000 and CV=0, the MSE ratio (full/reduced) is 1.002, meaning the full model has slightly HIGHER MSE. The t-statistic for the difference is 0.24 (p~0.81), so the difference is not statistically significant---but the claim of "across ALL conditions" is technically falsified. The paper itself states the ratio is "1.00" at n=5000, which rounds correctly, but then makes a universal claim that the data does not support.
- **Severity**: Major
- **Suggestion**: Soften to "the full model has comparable or lower MSE across all conditions tested" or "at n <= 1000, the full model consistently has lower MSE."

### MAJOR: CV labeling inconsistency between tables and prose

- **Location**: Section 3.4 (line 244), Section 5.3 (lines 452-458)
- **Quoted text**: "At n = 500 and CV = 10%, the LRT rejection rate is 37% while the MTTF bias is only 0.9%"
- **Problem**: The tables use actual CV values (0, 2.7, 5.5, 8.2, 11.0, 13.7, 20.5, 27.4, 41.1%). The prose refers to "CV = 10%" which corresponds to target_cv = 0.10 but actual_cv = 13.7%. The numbers cited (37% rejection, 0.9% bias) match actual_cv=13.7%, not 10%. This creates a disconnect between the table values and the in-text discussion. A reader looking at Table 5 for "CV = 10%" would find no matching row.
- **Severity**: Major
- **Suggestion**: Use actual CV values consistently throughout both tables and prose. Replace "CV = 10%" with "CV = 14%" (or 13.7%) in the prose to match the tables.

### MINOR: Property 1 closure formula uses non-standard parameterization

- **Location**: Section 2.3 (line 114)
- **Quoted text**: "$\lambda_s = (\sum_{j=1}^{m} \lambda_j^{-k})^{-1/k}$"
- **Problem**: This formula is correct for the parameterization used (where larger lambda = longer life). However, the standard Barlow & Proschan result is typically stated in terms of the cumulative hazard function directly. The formula should be verified against the cited source. The derivation is: system CDF hazard $H(t) = \sum (t/\lambda_j)^k = t^k \sum \lambda_j^{-k} = (t/\lambda_s)^k$ where $\lambda_s^{-k} = \sum \lambda_j^{-k}$, giving $\lambda_s = (\sum \lambda_j^{-k})^{-1/k}$. This is correct.
- **Severity**: Minor (cosmetic)
- **Suggestion**: No change needed; formula is correct.

### MINOR: Uniqueness Remark argument is incomplete

- **Location**: Section 2.3 (lines 117-119)
- **Quoted text**: "This follows from the linear independence of $\{e^{\alpha u} : \alpha \in \mathbb{R}\}$"
- **Problem**: The argument is correct in outline but missing a step. It needs: let u = ln(t), then the system cumulative hazard becomes $\sum_j c_j e^{k_j u}$ where $c_j = \lambda_j^{-k_j}$. For this to equal $c_s e^{k_s u}$, the set $\{k_j\}$ must have cardinality 1 (by linear independence of distinct exponentials over the reals). The phrase "single-parameter restriction" is also ambiguous---it should say "the only constraint that reduces the shape parameters to a single shared parameter."
- **Severity**: Minor
- **Suggestion**: Expand to 2-3 sentences explicitly performing the substitution u = ln(t) and citing the linear independence result.

### MINOR: Censoring factor reported as 2.6x but data shows 2.5x

- **Location**: Section 4.3 (line 342), Section 6 (line 480)
- **Quoted text**: "2.6x from q = 0.50 to q = 1.00"
- **Problem**: The data shows 43.0% / 17.0% = 2.53x, which rounds to 2.5x, not 2.6x. A minor numerical imprecision.
- **Severity**: Minor
- **Suggestion**: Change to "2.5x" or "approximately 2.5x."

### SUGGESTION: Equation (4) could be simplified

- **Location**: Section 2.2 (line 104)
- **Problem**: The log-likelihood writes the failure contribution as $\log(\sum_{j \in C_i} \frac{h_j(t_i)}{h(t_i;\theta)} \cdot f(t_i;\theta))$. This simplifies to $\log R(t_i;\theta) + \log(\sum_{j \in C_i} h_j(t_i))$, since $h_j/h \cdot f = h_j/h \cdot h \cdot R = h_j \cdot R$, and summing gives $R \sum h_j$. The simpler form matches what the code actually computes.
- **Suggestion**: Either simplify the equation or add a remark showing the simplification.

## Logical Chain Assessment

The overall argument is:
1. Common-shape model has Weibull closure (Property 1) -- SOUND
2. Consequence analysis quantifies bias under misspecification -- SOUND (data verified)
3. LRT characterizes detectability -- SOUND (data verified, but prose overstates)
4. Bias-detectability alignment makes adaptive procedure work -- SOUND

The logical chain holds. The issues are in the precision of specific claims, not in the overall structure.

## Confidence: HIGH for all findings
