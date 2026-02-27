#!/usr/bin/env Rscript
# Consequence analysis: How wrong are predictions when the reduced model is misspecified?
#
# For each (CV, n) condition:
#   1. Generate data from full model (heterogeneous shapes)
#   2. Fit both full and reduced models
#   3. Compute system MTTF, R(t), and component failure probs under each
#   4. Compare to ground truth
#
# This answers: "when the reduced model is wrong, does it matter for predictions?"

library(stats)
library(wei.series.md.c1.c2.c3)

source("../sim_utils.R")

set.seed(2024)

# ---------------------------------------------------------------------------
# Reliability metric functions
# ---------------------------------------------------------------------------

# System MTTF via numerical integration of the reliability function
# MTTF = integral_0^infty R(t) dt = integral_0^infty exp{-sum_j (t/lambda_j)^k_j} dt
system_mttf <- function(shapes, scales, upper = 1e5) {
  R_sys <- function(t) {
    exp(-sum((t / scales)^shapes))
  }
  integrate(Vectorize(R_sys), lower = 0, upper = upper,
            rel.tol = 1e-8, subdivisions = 1000L)$value
}

# System reliability at time t
system_reliability <- function(t, shapes, scales) {
  exp(-sum((t / scales)^shapes))
}

# Component failure probability P_j = Pr{K = j}
# P_j = integral_0^infty h_j(t) * R(t) dt
component_failure_prob <- function(j, shapes, scales, upper = 1e5) {
  integrand <- function(t) {
    k_j <- shapes[j]
    lam_j <- scales[j]
    h_j <- (k_j / lam_j) * (t / lam_j)^(k_j - 1)
    R <- exp(-sum((t / scales)^shapes))
    h_j * R
  }
  integrate(Vectorize(integrand), lower = 0, upper = upper,
            rel.tol = 1e-8, subdivisions = 1000L)$value
}

# All component failure probabilities
all_failure_probs <- function(shapes, scales, upper = 1e5) {
  m <- length(shapes)
  sapply(1:m, function(j) component_failure_prob(j, shapes, scales, upper))
}

# ---------------------------------------------------------------------------
# Shape generation (same as divergence study)
# ---------------------------------------------------------------------------
generate_shapes_with_cv <- function(m, mean_k, target_cv) {
  target_sd <- target_cv * mean_k
  if (target_cv < 0.001) return(rep(mean_k, m))
  half_range <- target_sd * sqrt(3)
  shapes <- seq(mean_k - half_range, mean_k + half_range, length.out = m)
  if (any(shapes <= 0)) {
    shapes <- shapes - min(shapes) + 0.1
    shapes <- shapes * mean_k / mean(shapes)
  }
  shapes
}

# ---------------------------------------------------------------------------
# Simulation parameters
# ---------------------------------------------------------------------------
csv_file <- "data-consequence.csv"
m <- 5
mean_k <- 1.18
CV_values <- c(0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20, 0.30)
N_values <- c(100, 500, 1000, 5000)
scales <- c(994.37, 908.95, 840.11, 940.13, 923.16)
p_mask <- 0.215
q_cens <- 0.825
n_reps <- 500
max_iter <- 1000L

# Resume logic
completed_counts <- list()
if (file.exists(csv_file)) {
  existing <- read.csv(csv_file)
  if (nrow(existing) > 0) {
    counts <- aggregate(mttf_true ~ n + target_cv, data = existing, FUN = length)
    for (i in 1:nrow(counts)) {
      key <- paste(counts$n[i], counts$target_cv[i], sep = "_")
      completed_counts[[key]] <- counts$mttf_true[i]
    }
    cat("Resuming: found", nrow(existing), "existing rows\n")
  }
} else {
  header <- data.frame(
    n = integer(), target_cv = numeric(), actual_cv = numeric(),
    # Ground truth
    mttf_true = numeric(),
    R_half_true = numeric(), R_mttf_true = numeric(), R_2mttf_true = numeric(),
    # Full model estimates
    mttf_full = numeric(),
    R_half_full = numeric(), R_mttf_full = numeric(), R_2mttf_full = numeric(),
    # Reduced model estimates
    mttf_reduced = numeric(),
    R_half_reduced = numeric(), R_mttf_reduced = numeric(), R_2mttf_reduced = numeric(),
    # Log-likelihoods
    loglik_F = numeric(), loglik_R = numeric(),
    # LRT
    Lambda = numeric(), p_value = numeric(),
    # Convergence
    conv_F = integer(), conv_R = integer()
  )
  write.table(header, file = csv_file, sep = ",", row.names = FALSE, col.names = TRUE)
}

n_errors <- 0

for (target_cv in CV_values) {
  shapes <- generate_shapes_with_cv(m, mean_k, target_cv)
  actual_cv <- sd(shapes) / mean(shapes)

  # Ground truth metrics
  mttf_true <- system_mttf(shapes, scales)
  t_half <- mttf_true / 2
  t_mttf <- mttf_true
  t_2mttf <- mttf_true * 2

  R_half_true <- system_reliability(t_half, shapes, scales)
  R_mttf_true <- system_reliability(t_mttf, shapes, scales)
  R_2mttf_true <- system_reliability(t_2mttf, shapes, scales)

  # Create theta vector
  theta <- numeric(2 * m)
  for (i in 1:m) {
    theta[2*(i-1) + 1] <- shapes[i]
    theta[2*(i-1) + 2] <- scales[i]
  }
  names(theta) <- paste0(rep(c("shape", "scale"), m), rep(1:m, each = 2))

  tau <- qwei_series(p = q_cens, scales = scales, shapes = shapes)

  cat("CV:", round(target_cv, 3), " | True MTTF:", round(mttf_true, 1), "\n")
  cat("  Shapes:", round(shapes, 4), "\n")

  for (n in N_values) {
    key <- paste(n, target_cv, sep = "_")
    n_done <- if (!is.null(completed_counts[[key]])) completed_counts[[key]] else 0
    if (n_done >= n_reps) {
      cat("  Skip: n =", n, "(", n_done, "done)\n")
      next
    }
    n_remaining <- n_reps - n_done

    condition_idx <- which(CV_values == target_cv) * 100 + which(N_values == n)
    set.seed(2024 * 2000 + condition_idx)
    if (n_done > 0) for (skip in 1:n_done) runif(1)

    cat("  n =", n, ": running", n_remaining, "reps\n")

    results_batch <- vector("list", n_remaining)
    batch_idx <- 0L

    for (rep in (n_done + 1):n_reps) {
      tryCatch({
        # Generate data
        df <- generate_guo_weibull_table_2_data(
          shapes = shapes, scales = scales, n = n, p = p_mask, tau = tau)
        dd <- decode_data(df)

        # Fit full model
        sol_F <- fit_full_model(theta0 = theta, t = dd$t, delta = dd$delta,
                                C = dd$C, max_iter = max_iter)
        if (sol_F$convergence != 0) next

        shapes_F <- sol_F$par[seq(1, 2*m, 2)]
        scales_F <- sol_F$par[seq(2, 2*m, 2)]

        # Fit reduced model
        k_hat <- mean(shapes_F)
        sol_R <- fit_reduced_model(par0 = c(k_hat, scales_F),
                                   t = dd$t, delta = dd$delta, C = dd$C,
                                   max_iter = max_iter)

        k_R <- sol_R$par[1]
        scales_R <- sol_R$par[-1]

        # Prediction metrics: full model
        mttf_full <- system_mttf(shapes_F, scales_F)
        R_half_full <- system_reliability(t_half, shapes_F, scales_F)
        R_mttf_full <- system_reliability(t_mttf, shapes_F, scales_F)
        R_2mttf_full <- system_reliability(t_2mttf, shapes_F, scales_F)

        # Prediction metrics: reduced model
        shapes_R <- rep(k_R, m)
        mttf_reduced <- system_mttf(shapes_R, scales_R)
        R_half_reduced <- system_reliability(t_half, shapes_R, scales_R)
        R_mttf_reduced <- system_reliability(t_mttf, shapes_R, scales_R)
        R_2mttf_reduced <- system_reliability(t_2mttf, shapes_R, scales_R)

        # LRT
        Lambda <- -2 * (sol_R$value - sol_F$value)
        # Guard against numerical Lambda < 0 (optimization failure indicator)
        if (Lambda < 0) {
          cat("[WARN] Negative Lambda at rep", rep, "- skipping\n")
          next
        }
        p_val <- pchisq(Lambda, m - 1, lower.tail = FALSE)

        batch_idx <- batch_idx + 1L
        results_batch[[batch_idx]] <- data.frame(
          n = n, target_cv = target_cv, actual_cv = actual_cv,
          mttf_true = mttf_true,
          R_half_true = R_half_true, R_mttf_true = R_mttf_true, R_2mttf_true = R_2mttf_true,
          mttf_full = mttf_full,
          R_half_full = R_half_full, R_mttf_full = R_mttf_full, R_2mttf_full = R_2mttf_full,
          mttf_reduced = mttf_reduced,
          R_half_reduced = R_half_reduced, R_mttf_reduced = R_mttf_reduced, R_2mttf_reduced = R_2mttf_reduced,
          loglik_F = sol_F$value, loglik_R = sol_R$value,
          Lambda = Lambda, p_value = p_val,
          conv_F = sol_F$convergence, conv_R = sol_R$convergence
        )
      }, error = function(e) {
        n_errors <<- n_errors + 1
        cat("[ERROR rep", rep, "]", conditionMessage(e), "\n")
      })
    }

    if (batch_idx > 0) {
      write.table(do.call(rbind, results_batch[1:batch_idx]),
                  file = csv_file, sep = ",", append = TRUE,
                  row.names = FALSE, col.names = FALSE)
    }
    cat("  Done:", batch_idx, "/", n_remaining, " (", n_errors, "errors)\n")
    n_errors <- 0
  }
}

cat("\nConsequence analysis complete. Results saved to:", csv_file, "\n")
