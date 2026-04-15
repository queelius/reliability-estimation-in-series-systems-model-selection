#!/usr/bin/env Rscript
# LRT simulation: Vary censoring quantile (q)
# Assesses how censoring affects ability to distinguish full vs reduced model

library(stats)
library(wei.series.md.c1.c2.c3)

# Source shared vectorized utilities
source("../../sim_utils.R")

set.seed(2024)

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
csv_file <- "data-lrt-vary-q.csv"
Q_values <- c(0.5, 0.6, 0.7, 0.825, 0.9, 0.95, 1.0)  # censoring quantiles (1.0 = no censoring)
N_values <- c(100, 500, 1000, 5000)  # sample sizes
p <- 0.215  # fixed masking probability
n_reps <- 500  # replications per condition
max_iter <- 1000L

# Compute divergence metrics
cv_shapes <- sd(shapes) / mean(shapes)
maxmin_ratio <- max(shapes) / min(shapes)

cat("Baseline system:\n")
cat("  Shape CV:", round(cv_shapes, 4), "\n")
cat("  Max/Min ratio:", round(maxmin_ratio, 4), "\n\n")

# Resume logic: read existing data if present
completed_counts <- list()
if (file.exists(csv_file)) {
  existing <- read.csv(csv_file)
  if (nrow(existing) > 0) {
    counts <- aggregate(p_value ~ n + q, data = existing, FUN = length)
    for (i in 1:nrow(counts)) {
      key <- paste(counts$n[i], counts$q[i], sep = "_")
      completed_counts[[key]] <- counts$p_value[i]
    }
    cat("Resuming: found", nrow(existing), "existing rows across", length(completed_counts), "conditions\n")
  }
} else {
  # Initialize new file with header
  write.table(
    data.frame(n = integer(), p = numeric(), q = numeric(),
               p_value = numeric(), Lambda = numeric(),
               loglik_F = numeric(), loglik_R = numeric(),
               cv_shapes = numeric(), maxmin_ratio = numeric(),
               pct_censored = numeric(),
               aic_F = numeric(), aic_R = numeric(),
               bic_F = numeric(), bic_R = numeric()),
    file = csv_file, sep = ",", row.names = FALSE, col.names = TRUE
  )
}

n_errors <- 0

for (q in Q_values) {
  if (q >= 1.0) {
    tau <- Inf  # no censoring
  } else {
    tau <- qwei_series(p = q, scales = scales, shapes = shapes)
  }

  for (n in N_values) {
    key <- paste(n, q, sep = "_")
    n_done <- if (!is.null(completed_counts[[key]])) completed_counts[[key]] else 0
    if (n_done >= n_reps) {
      cat("  Skipping: q =", q, ", n =", n, "(", n_done, "already done)\n")
      next
    }
    n_remaining <- n_reps - n_done

    # Per-condition reproducible seed
    condition_idx <- which(Q_values == q) * 100 + which(N_values == n)
    set.seed(2024 * 1000 + condition_idx)
    if (n_done > 0) {
      # Advance RNG past already-completed reps
      for (skip in 1:n_done) runif(1)
      cat("  Resuming: q =", q, ", n =", n, "(", n_done, "done,", n_remaining, "remaining)\n")
    } else {
      cat("Running: q =", q, ", n =", n, "\n")
    }

    # Batch results for this condition
    results_batch <- vector("list", n_remaining)
    batch_idx <- 0L

    for (rep in (n_done + 1):n_reps) {
      tryCatch({
        # Generate data
        df <- generate_guo_weibull_table_2_data(
          shapes = shapes, scales = scales, n = n, p = p, tau = tau)

        pct_censored <- 1 - mean(df$delta)

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
          n = n, p = p, q = q, p_value = p_value, Lambda = Lambda,
          loglik_F = sol_F$value, loglik_R = sol_R$value,
          cv_shapes = cv_shapes, maxmin_ratio = maxmin_ratio,
          pct_censored = pct_censored,
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
