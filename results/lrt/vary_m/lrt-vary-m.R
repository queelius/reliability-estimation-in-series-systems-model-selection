#!/usr/bin/env Rscript
# LRT simulation: Vary number of components (m)
# Assesses how system complexity affects model selection

library(stats)
library(wei.series.md.c1.c2.c3)

# Source shared vectorized utilities
source("../../sim_utils.R")

set.seed(2024)

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

# Resume logic: read existing data if present
completed_counts <- list()
if (file.exists(csv_file)) {
  existing <- read.csv(csv_file)
  if (nrow(existing) > 0) {
    counts <- aggregate(p_value ~ m + n, data = existing, FUN = length)
    for (i in 1:nrow(counts)) {
      key <- paste(counts$m[i], counts$n[i], sep = "_")
      completed_counts[[key]] <- counts$p_value[i]
    }
    cat("Resuming: found", nrow(existing), "existing rows across", length(completed_counts), "conditions\n")
  }
} else {
  # Initialize new file with header
  write.table(
    data.frame(m = integer(), n = integer(), p = numeric(), q = numeric(),
               p_value = numeric(), Lambda = numeric(),
               loglik_F = numeric(), loglik_R = numeric(),
               cv_shapes = numeric(), maxmin_ratio = numeric(),
               df_lrt = integer(),
               aic_F = numeric(), aic_R = numeric(),
               bic_F = numeric(), bic_R = numeric()),
    file = csv_file, sep = ",", row.names = FALSE, col.names = TRUE
  )
}

n_errors <- 0

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
    key <- paste(m, n, sep = "_")
    n_done <- if (!is.null(completed_counts[[key]])) completed_counts[[key]] else 0
    if (n_done >= n_reps) {
      cat("  Skipping: m =", m, ", n =", n, "(", n_done, "already done)\n")
      next
    }
    n_remaining <- n_reps - n_done

    # Per-condition reproducible seed
    condition_idx <- which(M_values == m) * 100 + which(N_values == n)
    set.seed(2024 * 1000 + condition_idx)
    if (n_done > 0) {
      # Advance RNG past already-completed reps
      for (skip in 1:n_done) runif(1)
      cat("  Resuming: m =", m, ", n =", n, "(", n_done, "done,", n_remaining, "remaining)\n")
    } else {
      cat("  Running: m =", m, ", n =", n, "\n")
    }

    # Batch results for this condition
    results_batch <- vector("list", n_remaining)
    batch_idx <- 0L

    for (rep in (n_done + 1):n_reps) {
      tryCatch({
        # Generate data
        df <- generate_guo_weibull_table_2_data(
          shapes = shapes, scales = scales, n = n, p = p, tau = tau)

        # Pre-decode data once
        dd <- decode_data(df)

        # Fit full model (vectorized)
        sol_F <- fit_full_model(theta0 = theta, t = dd$t, delta = dd$delta,
                                C = dd$C, max_iter = max_iter)

        if (sol_F$convergence != 0) next

        shapes_mle <- sol_F$par[seq(1, length(theta), 2)]
        scales_mle <- sol_F$par[seq(2, length(theta), 2)]
        k_hat <- mean(shapes_mle)

        # Fit reduced model (vectorized + L-BFGS-B with gradient)
        sol_R <- fit_reduced_model(par0 = c(k_hat, scales_mle),
                                   t = dd$t, delta = dd$delta, C = dd$C,
                                   max_iter = max_iter)

        # LRT (degrees of freedom = m - 1)
        Lambda <- -2 * (sol_R$value - sol_F$value)
        p_value <- pchisq(Lambda, m - 1, lower.tail = FALSE)

        # AIC and BIC
        k_F <- 2 * m        # full model parameters
        k_R <- m + 1         # reduced model parameters
        aic_F <- -2 * sol_F$value + 2 * k_F
        aic_R <- -2 * sol_R$value + 2 * k_R
        bic_F <- -2 * sol_F$value + k_F * log(n)
        bic_R <- -2 * sol_R$value + k_R * log(n)

        # Accumulate result
        batch_idx <- batch_idx + 1L
        results_batch[[batch_idx]] <- data.frame(
          m = m, n = n, p = p, q = q, p_value = p_value, Lambda = Lambda,
          loglik_F = sol_F$value, loglik_R = sol_R$value,
          cv_shapes = cv_shapes, maxmin_ratio = maxmin_ratio,
          df_lrt = m - 1,
          aic_F = aic_F, aic_R = aic_R,
          bic_F = bic_F, bic_R = bic_R)

      }, error = function(e) {
        n_errors <<- n_errors + 1
        cat("[ERROR rep", rep, "]", conditionMessage(e), "\n")
      })
    }

    # Write batch for this condition
    if (batch_idx > 0) {
      write.table(do.call(rbind, results_batch[1:batch_idx]),
                  file = csv_file, sep = ",", append = TRUE,
                  row.names = FALSE, col.names = FALSE)
    }

    n_new <- batch_idx
    if (n_done > 0) {
      cat("  Completed:", n_new, "/", n_remaining, "new successful (", n_errors, "errors,", n_done, "resumed)\n")
    } else {
      cat("  Completed:", n_new, "/", n_reps, "successful (", n_errors, "errors)\n")
    }
    n_errors <- 0
  }
}

cat("\nSimulation complete. Results saved to:", csv_file, "\n")
