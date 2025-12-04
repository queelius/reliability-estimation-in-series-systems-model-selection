#!/usr/bin/env Rscript
# LRT simulation: Vary number of components (m)
# Assesses how system complexity affects model selection

library(stats)
library(wei.series.md.c1.c2.c3)

# Base parameters for generating systems of different sizes
# Use similar well-designed characteristics: shapes ~1.1-1.3, scales ~800-1000
base_shapes <- c(1.2576, 1.1635, 1.1308, 1.1802, 1.2034, 1.1456, 1.2189, 1.1723, 1.1945, 1.2301)
base_scales <- c(994.37, 908.95, 840.11, 940.13, 923.16, 875.42, 961.28, 889.74, 912.55, 948.63)

# Simulation parameters
csv_file <- "data-lrt-vary-m.csv"
M_values <- c(2, 3, 4, 5, 6, 7, 8)  # number of components
N_values <- c(100, 500, 1000, 5000)  # sample sizes
p <- 0.215  # fixed masking probability
q <- 0.825  # fixed censoring quantile
n_reps <- 500  # replications per condition
max_iter <- 1000L

# Initialize output file
write.table(
  data.frame(m = integer(), n = integer(), p = numeric(), q = numeric(),
             p_value = numeric(), Lambda = numeric(),
             loglik_F = numeric(), loglik_R = numeric(),
             cv_shapes = numeric(), maxmin_ratio = numeric(),
             df_lrt = integer()),
  file = csv_file, sep = ",", row.names = FALSE, col.names = TRUE
)

for (m in M_values) {
  shapes <- base_shapes[1:m]
  scales <- base_scales[1:m]

  # Create theta vector
  theta <- numeric(2 * m)
  for (i in 1:m) {
    theta[2*(i-1) + 1] <- shapes[i]
    theta[2*(i-1) + 2] <- scales[i]
  }
  names(theta) <- paste0(rep(c("shape", "scale"), m), rep(1:m, each = 2))

  # Compute divergence metrics
  cv_shapes <- sd(shapes) / mean(shapes)
  maxmin_ratio <- max(shapes) / min(shapes)

  tau <- qwei_series(p = q, scales = scales, shapes = shapes)

  cat("System with m =", m, "components\n")
  cat("  Shapes:", round(shapes, 3), "\n")
  cat("  Shape CV:", round(cv_shapes, 4), "\n")
  cat("  LRT df:", m - 1, "\n\n")

  for (n in N_values) {
    cat("  Running: m =", m, ", n =", n, "\n")

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

        # LRT (degrees of freedom = m - 1)
        Lambda <- -2 * (sol_R$value - sol_F$value)
        p_value <- pchisq(Lambda, m - 1, lower.tail = FALSE)

        # Write result
        write.table(
          data.frame(m = m, n = n, p = p, q = q, p_value = p_value, Lambda = Lambda,
                     loglik_F = sol_F$value, loglik_R = sol_R$value,
                     cv_shapes = cv_shapes, maxmin_ratio = maxmin_ratio,
                     df_lrt = m - 1),
          file = csv_file, sep = ",", append = TRUE,
          row.names = FALSE, col.names = FALSE)

      }, error = function(e) { })
    }
  }
}

cat("\nSimulation complete. Results saved to:", csv_file, "\n")
