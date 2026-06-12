#!/usr/bin/env Rscript
# Adaptive model selection procedure simulation
#
# Compares four strategies:
#   1. Always-full:    always use full model estimates
#   2. Always-reduced: always use reduced model estimates
#   3. Adaptive:       fit full -> estimate CV -> decide
#   4. Oracle:         knows true CV, picks optimally
#
# Metrics: MSE of system MTTF, bias, model selection accuracy

library(stats)
library(wei.series.md.c1.c2.c3)

source("../sim_utils.R")

set.seed(2024)

# ---------------------------------------------------------------------------
# Reliability metric functions
# ---------------------------------------------------------------------------
system_mttf <- function(shapes, scales, upper = 1e5) {
  R_sys <- function(t) exp(-sum((t / scales)^shapes))
  integrate(Vectorize(R_sys), lower = 0, upper = upper,
            rel.tol = 1e-8, subdivisions = 1000L)$value
}

# ---------------------------------------------------------------------------
# Shape generation
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
csv_file <- "data-adaptive.csv"
m <- 5
mean_k <- 1.18
CV_values <- c(0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20)
N_values <- c(100, 500, 1000)
scales <- c(994.37, 908.95, 840.11, 940.13, 923.16)
p_mask <- 0.215
q_cens <- 0.825
n_reps <- 500
max_iter <- 1000L

# Adaptive threshold: CV_hat below which we select the reduced model.
# Calibrated so that under H0 (true CV = 0), the procedure selects the
# full model at approximately alpha = 0.05 rate.
# This is set per sample size; we'll calibrate it from the LRT:
# select reduced if LRT p-value > alpha.
# For the adaptive-CV variant, we use a threshold on estimated CV.
# We test both approaches.
alpha <- 0.05

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
    mttf_true = numeric(),
    # Full model
    mttf_full = numeric(),
    # Reduced model
    mttf_reduced = numeric(),
    # Adaptive (LRT-based): use reduced if p > alpha, else full
    mttf_adaptive_lrt = numeric(),
    selected_model_lrt = character(),  # "full" or "reduced"
    # Adaptive (CV-based): use reduced if CV_hat < threshold
    cv_hat = numeric(),
    mttf_adaptive_cv = numeric(),
    selected_model_cv = character(),
    # LRT statistics
    Lambda = numeric(), p_value = numeric(),
    loglik_F = numeric(), loglik_R = numeric(),
    # Convergence
    conv_F = integer()
  )
  write.table(header, file = csv_file, sep = ",", row.names = FALSE, col.names = TRUE)
}

n_errors <- 0

# CV threshold for the CV-based adaptive procedure
# We'll use 0.10 as a starting point (to be calibrated from results)
cv_threshold <- 0.10

for (target_cv in CV_values) {
  shapes <- generate_shapes_with_cv(m, mean_k, target_cv)
  actual_cv <- sd(shapes) / mean(shapes)

  mttf_true <- system_mttf(shapes, scales)

  theta <- numeric(2 * m)
  for (i in 1:m) {
    theta[2*(i-1) + 1] <- shapes[i]
    theta[2*(i-1) + 2] <- scales[i]
  }
  names(theta) <- paste0(rep(c("shape", "scale"), m), rep(1:m, each = 2))

  tau <- qwei_series(p = q_cens, scales = scales, shapes = shapes)

  cat("CV:", round(target_cv, 3), " | True MTTF:", round(mttf_true, 1), "\n")

  for (n in N_values) {
    key <- paste(n, target_cv, sep = "_")
    n_done <- if (!is.null(completed_counts[[key]])) completed_counts[[key]] else 0
    if (n_done >= n_reps) {
      cat("  Skip: n =", n, "\n")
      next
    }
    n_remaining <- n_reps - n_done

    condition_idx <- which(CV_values == target_cv) * 100 + which(N_values == n)
    set.seed(2024 * 3000 + condition_idx)
    if (n_done > 0) for (skip in 1:n_done) runif(1)

    cat("  n =", n, ": running", n_remaining, "reps\n")

    results_batch <- vector("list", n_remaining)
    batch_idx <- 0L

    for (rep in (n_done + 1):n_reps) {
      tryCatch({
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

        # MTTF under each model
        mttf_full <- system_mttf(shapes_F, scales_F)
        mttf_reduced <- system_mttf(rep(k_R, m), scales_R)

        # LRT
        Lambda <- -2 * (sol_R$value - sol_F$value)
        p_val <- pchisq(Lambda, m - 1, lower.tail = FALSE)

        # Adaptive LRT: use reduced if p > alpha
        if (p_val > alpha) {
          mttf_adaptive_lrt <- mttf_reduced
          selected_lrt <- "reduced"
        } else {
          mttf_adaptive_lrt <- mttf_full
          selected_lrt <- "full"
        }

        # Adaptive CV: use reduced if estimated CV < threshold
        cv_hat <- sd(shapes_F) / mean(shapes_F)
        if (cv_hat < cv_threshold) {
          mttf_adaptive_cv <- mttf_reduced
          selected_cv <- "reduced"
        } else {
          mttf_adaptive_cv <- mttf_full
          selected_cv <- "full"
        }

        batch_idx <- batch_idx + 1L
        results_batch[[batch_idx]] <- data.frame(
          n = n, target_cv = target_cv, actual_cv = actual_cv,
          mttf_true = mttf_true,
          mttf_full = mttf_full,
          mttf_reduced = mttf_reduced,
          mttf_adaptive_lrt = mttf_adaptive_lrt,
          selected_model_lrt = selected_lrt,
          cv_hat = cv_hat,
          mttf_adaptive_cv = mttf_adaptive_cv,
          selected_model_cv = selected_cv,
          Lambda = Lambda, p_value = p_val,
          loglik_F = sol_F$value, loglik_R = sol_R$value,
          conv_F = sol_F$convergence
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

cat("\nAdaptive selection study complete. Results saved to:", csv_file, "\n")
