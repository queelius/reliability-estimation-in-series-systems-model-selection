#!/usr/bin/env Rscript
# LRT simulation: Controlled divergence from homogeneity
# Systematically varies shape parameter heterogeneity using CV as the metric

library(stats)
library(wei.series.md.c1.c2.c3)

# Function to generate shapes with target CV
generate_shapes_with_cv <- function(m, mean_k, target_cv) {
  # Generate shapes uniformly spread around mean to achieve target CV
  # CV = sd/mean, so sd = CV * mean
  target_sd <- target_cv * mean_k

  if (target_cv < 0.001) {
    # Essentially homogeneous
    return(rep(mean_k, m))
  }

  # Generate evenly spaced values symmetric around mean
  # For uniform spread: sd = range / sqrt(12) for uniform
  # We'll use a simpler approach: linear spread
  half_range <- target_sd * sqrt(3)  # for uniform distribution
  shapes <- seq(mean_k - half_range, mean_k + half_range, length.out = m)

  # Ensure all positive
  if (any(shapes <= 0)) {
    shapes <- shapes - min(shapes) + 0.1
    # Rescale to target mean
    shapes <- shapes * mean_k / mean(shapes)
  }

  return(shapes)
}

# Simulation parameters
csv_file <- "data-lrt-divergence.csv"
m <- 5  # 5-component system
mean_k <- 1.18  # mean shape parameter (similar to baseline)
CV_values <- c(0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20, 0.30, 0.50)  # target CVs
N_values <- c(100, 500, 1000, 5000, 10000)  # sample sizes

# Fixed scale parameters (same as baseline)
scales <- c(994.37, 908.95, 840.11, 940.13, 923.16)

p <- 0.215  # fixed masking probability
q <- 0.825  # fixed censoring quantile
n_reps <- 500  # replications per condition
max_iter <- 1000L

# Initialize output file
write.table(
  data.frame(n = integer(), target_cv = numeric(), actual_cv = numeric(),
             maxmin_ratio = numeric(), p = numeric(), q = numeric(),
             p_value = numeric(), Lambda = numeric(),
             loglik_F = numeric(), loglik_R = numeric()),
  file = csv_file, sep = ",", row.names = FALSE, col.names = TRUE
)

for (target_cv in CV_values) {
  shapes <- generate_shapes_with_cv(m, mean_k, target_cv)
  actual_cv <- sd(shapes) / mean(shapes)
  maxmin_ratio <- max(shapes) / min(shapes)

  # Create theta vector
  theta <- numeric(2 * m)
  for (i in 1:m) {
    theta[2*(i-1) + 1] <- shapes[i]
    theta[2*(i-1) + 2] <- scales[i]
  }
  names(theta) <- paste0(rep(c("shape", "scale"), m), rep(1:m, each = 2))

  tau <- qwei_series(p = q, scales = scales, shapes = shapes)

  cat("Target CV:", target_cv, "\n")
  cat("  Shapes:", round(shapes, 4), "\n")
  cat("  Actual CV:", round(actual_cv, 4), "\n")
  cat("  Max/Min:", round(maxmin_ratio, 4), "\n\n")

  for (n in N_values) {
    cat("  Running: CV =", round(target_cv, 2), ", n =", n, "\n")

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
          theta_r <- numeric(length(scales) * 2)
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
          data.frame(n = n, target_cv = target_cv, actual_cv = actual_cv,
                     maxmin_ratio = maxmin_ratio, p = p, q = q,
                     p_value = p_value, Lambda = Lambda,
                     loglik_F = sol_F$value, loglik_R = sol_R$value),
          file = csv_file, sep = ",", append = TRUE,
          row.names = FALSE, col.names = FALSE)

      }, error = function(e) { })
    }
  }
}

cat("\nSimulation complete. Results saved to:", csv_file, "\n")
