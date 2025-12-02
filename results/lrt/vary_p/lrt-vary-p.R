#!/usr/bin/env Rscript
# LRT simulation: Vary masking probability (p)
# Assesses how masking affects ability to distinguish full vs reduced model

library(tidyverse)
library(stats)
library(wei.series.md.c1.c2.c3)

# Baseline well-designed system
theta <- c(shape1 = 1.2576, scale1 = 994.3661,
           shape2 = 1.1635, scale2 = 908.9458,
           shape3 = 1.1308, scale3 = 840.1141,
           shape4 = 1.1802, scale4 = 940.1342,
           shape5 = 1.2034, scale5 = 923.1631)

shapes <- theta[seq(1, length(theta), 2)]
scales <- theta[seq(2, length(theta), 2)]
m <- length(shapes)

# Simulation parameters
csv_file <- "data-lrt-vary-p.csv"
P_values <- c(0.05, 0.1, 0.15, 0.215, 0.3, 0.4, 0.5, 0.6, 0.7)  # masking probabilities
N_values <- c(100, 500, 1000, 5000)  # sample sizes
q <- 0.825  # fixed censoring quantile
n_reps <- 500  # replications per condition
max_iter <- 1000L

# Compute divergence metrics for baseline
cv_shapes <- sd(shapes) / mean(shapes)
maxmin_ratio <- max(shapes) / min(shapes)

cat("Baseline system:\n")
cat("  Shape CV:", round(cv_shapes, 4), "\n")
cat("  Max/Min ratio:", round(maxmin_ratio, 4), "\n\n")

# Initialize output file
write.table(
  data.frame(n = integer(), p = numeric(), q = numeric(),
             p_value = numeric(), Lambda = numeric(),
             loglik_F = numeric(), loglik_R = numeric(),
             cv_shapes = numeric(), maxmin_ratio = numeric()),
  file = csv_file, sep = ",", row.names = FALSE, col.names = TRUE
)

for (p in P_values) {
  tau <- qwei_series(p = q, scales = scales, shapes = shapes)

  for (n in N_values) {
    cat("Running: p =", p, ", n =", n, "\n")

    for (rep in 1:n_reps) {
      tryCatch({
        # Generate data
        df <- generate_guo_weibull_table_2_data(
          shapes = shapes, scales = scales, n = n, p = p, tau = tau)

        # Fit full model
        sol_F <- mle_lbfgsb_wei_series_md_c1_c2_c3(
          theta0 = theta, df = df, hessian = FALSE,
          control = list(maxit = max_iter, parscale = theta))

        if (sol_F$convergence != 0) next

        shapes_mle <- sol_F$par[seq(1, length(theta), 2)]
        scales_mle <- sol_F$par[seq(2, length(theta), 2)]
        k_hat <- mean(shapes_mle)

        # Fit reduced model
        loglik_reduced <- function(df, k, scales) {
          theta_r <- rep(NA, length(scales) * 2)
          for (i in 1:length(scales)) {
            theta_r[2*(i-1) + 1] <- k
            theta_r[2*(i-1) + 2] <- scales[i]
          }
          wei.series.md.c1.c2.c3::loglik_wei_series_md_c1_c2_c3(df = df, theta = theta_r)
        }

        sol_R <- stats::optim(
          par = c(k_hat, scales_mle),
          fn = function(theta) loglik_reduced(df = df, k = theta[1], scales = theta[-1]),
          control = list(fnscale = -1, maxit = max_iter))

        # LRT
        Lambda <- -2 * (sol_R$value - sol_F$value)
        p_value <- pchisq(Lambda, m - 1, lower.tail = FALSE)

        # Write result
        write.table(
          data.frame(n = n, p = p, q = q, p_value = p_value, Lambda = Lambda,
                     loglik_F = sol_F$value, loglik_R = sol_R$value,
                     cv_shapes = cv_shapes, maxmin_ratio = maxmin_ratio),
          file = csv_file, sep = ",", append = TRUE,
          row.names = FALSE, col.names = FALSE)

      }, error = function(e) { })
    }
  }
}

cat("\nSimulation complete. Results saved to:", csv_file, "\n")
