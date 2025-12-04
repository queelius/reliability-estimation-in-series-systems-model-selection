#!/usr/bin/env Rscript
# Compute divergence metrics (CV and max/min ratio) for existing LRT results
# Maps shape3 values to divergence from homogeneity

# Baseline shape parameters (excluding shape3)
other_shapes <- c(1.2576, 1.1635, 1.1802, 1.2034)

# shape3 values from the simulation
shapes3 <- c(0.25, 0.5, 0.75, 1, 1.1308, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3.0)

# Function to compute divergence metrics
compute_metrics <- function(shape3) {
  shapes <- c(other_shapes[1:2], shape3, other_shapes[3:4])
  cv <- sd(shapes) / mean(shapes)
  maxmin <- max(shapes) / min(shapes)
  list(cv = cv, maxmin = maxmin, mean_shape = mean(shapes))
}

# Create table
results <- data.frame(
  shape3 = shapes3,
  cv = sapply(shapes3, function(k) compute_metrics(k)$cv),
  maxmin_ratio = sapply(shapes3, function(k) compute_metrics(k)$maxmin),
  mean_shape = sapply(shapes3, function(k) compute_metrics(k)$mean_shape)
)

# Display results
cat("Divergence Metrics for Varying shape3\n")
cat("======================================\n\n")
cat("Baseline shapes: k1=1.2576, k2=1.1635, k4=1.1802, k5=1.2034\n")
cat("Well-designed baseline k3=1.1308\n\n")

print(results, digits = 4, row.names = FALSE)

# Save to CSV
write.csv(results, "divergence_metrics_by_shape3.csv", row.names = FALSE)

cat("\n\nInterpretation:\n")
cat("- CV (Coefficient of Variation): sd(shapes)/mean(shapes)\n")
cat("- Values near 0 indicate homogeneous shapes\n")
cat("- Max/Min ratio: max(shape)/min(shape)\n")
cat("- Values near 1 indicate homogeneous shapes\n")

# Also create LaTeX table for paper
cat("\n\nLaTeX table:\n")
cat("\\begin{tabular}{cccc}\n")
cat("\\toprule\n")
cat("$k_3$ & CV & Max/Min & Mean $k$ \\\\\n")
cat("\\midrule\n")
for (i in 1:nrow(results)) {
  cat(sprintf("%.4f & %.3f & %.2f & %.3f \\\\\n",
              results$shape3[i], results$cv[i], results$maxmin_ratio[i], results$mean_shape[i]))
}
cat("\\bottomrule\n")
cat("\\end{tabular}\n")
