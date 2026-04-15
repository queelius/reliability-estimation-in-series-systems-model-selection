#!/usr/bin/env Rscript
# LRT simulation: Controlled divergence from homogeneity
# Systematically varies shape parameter heterogeneity using CV as the metric

library(stats)
library(wei.series.md.c1.c2.c3)

# Source shared vectorized utilities
source("../../sim_utils.R")

set.seed(2024)

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

# Resume logic: read existing data if present
completed_counts <- list()
if (file.exists(csv_file)) {
  existing <- read.csv(csv_file)
  if (nrow(existing) > 0) {
    counts <- aggregate(p_value ~ n + target_cv, data = existing, FUN = length)
    for (i in 1:nrow(counts)) {
      key <- paste(counts$n[i], counts$target_cv[i], sep = "_")
      completed_counts[[key]] <- counts$p_value[i]
    }
    cat("Resuming: found", nrow(existing), "existing rows across", length(completed_counts), "conditions\n")
  }
} else {
  # Initialize new file with header
  write.table(
    data.frame(n = integer(), target_cv = numeric(), actual_cv = numeric(),
               maxmin_ratio = numeric(), p = numeric(), q = numeric(),
               p_value = numeric(), Lambda = numeric(),
               loglik_F = numeric(), loglik_R = numeric(),
               aic_F = numeric(), aic_R = numeric(),
               bic_F = numeric(), bic_R = numeric()),
    file = csv_file, sep = ",", row.names = FALSE, col.names = TRUE
  )
}

n_errors <- 0

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
    key <- paste(n, target_cv, sep = "_")
    n_done <- if (!is.null(completed_counts[[key]])) completed_counts[[key]] else 0
    if (n_done >= n_reps) {
      cat("  Skipping: CV =", round(target_cv, 2), ", n =", n, "(", n_done, "already done)\n")
      next
    }
    n_remaining <- n_reps - n_done

    # Per-condition reproducible seed
    condition_idx <- which(CV_values == target_cv) * 100 + which(N_values == n)
    set.seed(2024 * 1000 + condition_idx)
    if (n_done > 0) {
      # Advance RNG past already-completed reps
      for (skip in 1:n_done) runif(1)
      cat("  Resuming: CV =", round(target_cv, 2), ", n =", n, "(", n_done, "done,", n_remaining, "remaining)\n")
    } else {
      cat("  Running: CV =", round(target_cv, 2), ", n =", n, "\n")
    }

    # Batch results for this condition
    results_batch <- vector("list", n_remaining)
    batch_idx <- 0L

    for (rep in (n_done + 1):n_reps) {
      tryCatch({
        # Generate data
        df <- generate_guo_weibull_table_2_data(
          shapes = shapes, scales = scales, n = n, p = p, tau = tau)

        # Pre-decode data once (avoids repeated md_decode_matrix calls)
        dd <- decode_data(df)

        # Fit full model (vectorized loglik + analytical gradient)
        sol_F <- fit_full_model(theta0 = theta, t = dd$t, delta = dd$delta,
                                C = dd$C, max_iter = max_iter)

        if (sol_F$convergence != 0) next

        shapes_mle <- sol_F$par[seq(1, length(theta), 2)]
        scales_mle <- sol_F$par[seq(2, length(theta), 2)]
        k_hat <- mean(shapes_mle)

        # Fit reduced model (vectorized loglik + analytical gradient + L-BFGS-B)
        sol_R <- fit_reduced_model(par0 = c(k_hat, scales_mle),
                                   t = dd$t, delta = dd$delta, C = dd$C,
                                   max_iter = max_iter)

        # LRT
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
          n = n, target_cv = target_cv, actual_cv = actual_cv,
          maxmin_ratio = maxmin_ratio, p = p, q = q,
          p_value = p_value, Lambda = Lambda,
          loglik_F = sol_F$value, loglik_R = sol_R$value,
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
