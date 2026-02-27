# sim_utils.R — Shared vectorized utilities for simulation scripts
#
# Provides drop-in replacements for the package's loglik/score functions
# with two key optimizations:
#   1. Vectorized matrix operations replace O(n) interpreted R loops
#   2. Data (t, delta, C) decoded once and passed directly, avoiding
#      repeated md_decode_matrix() calls inside optim()

# ---------------------------------------------------------------------------
# Pre-decode data from a simulation data frame
# Call once per replication, reuse for all optim evaluations
# ---------------------------------------------------------------------------
decode_data <- function(df, candset = "x", lifetime = "t",
                        right_censoring_indicator = "delta") {
  C <- md.tools::md_decode_matrix(df, candset)
  t_vec <- df[[lifetime]]
  delta <- if (right_censoring_indicator %in% colnames(df)) {
    as.logical(df[[right_censoring_indicator]])
  } else {
    rep(TRUE, nrow(df))
  }
  list(t = t_vec, delta = delta, C = C, n = length(t_vec), m = ncol(C))
}

# ---------------------------------------------------------------------------
# Vectorized log-likelihood for Weibull series system with masked data
#
# Mathematically identical to loglik_wei_series_md_c1_c2_c3 but replaces
# the O(n) R loop with matrix operations:
#   Term 1: -sum_{i,j} (t_i / lambda_j)^k_j
#   Term 2: sum_{uncensored i} log(sum_{j in C_i} h_j(t_i))
#     where h_j(t) = (k_j / lambda_j) * (t / lambda_j)^(k_j - 1)
# ---------------------------------------------------------------------------
loglik_vec <- function(shapes, scales, t, delta, C) {
  n <- length(t)
  m <- length(shapes)

  # t_over_s[i,j] = t[i] / scales[j]  — n x m matrix
  t_over_s <- outer(t, scales, "/")

  # Term 1: survival contribution (all observations, all components)
  # (t_i/lambda_j)^k_j summed over all i,j
  term1 <- -sum(t_over_s ^ rep(shapes, each = n))

  # Term 2: masked hazard contribution (uncensored observations only)
  if (any(delta)) {
    # H[i,j] = (k_j / lambda_j) * (t_i / lambda_j)^(k_j - 1)
    #         = shapes[j] / scales[j] * t_over_s[i,j]^(shapes[j]-1)
    H <- t_over_s ^ rep(shapes - 1, each = n)
    H <- H * rep(shapes / scales, each = n)
    # Zero out non-candidate components
    H <- H * C
    # For uncensored obs: log(sum of hazard over candidate set)
    term2 <- sum(log(rowSums(H[delta, , drop = FALSE])))
  } else {
    term2 <- 0
  }

  term1 + term2
}

# ---------------------------------------------------------------------------
# Vectorized score (gradient) for full model
#
# Returns gradient in interleaved format: (dk1, dlambda1, dk2, dlambda2, ...)
# Mathematically identical to score_wei_series_md_c1_c2_c3
# ---------------------------------------------------------------------------
score_vec <- function(shapes, scales, t, delta, C) {
  n <- length(t)
  m <- length(shapes)

  t_over_s <- outer(t, scales, "/")          # n x m
  log_t_over_s <- log(t_over_s)              # n x m
  t_over_s_k <- t_over_s ^ rep(shapes, each = n)  # (t/lambda)^k

  # --- Reliability/survival term gradients (all observations) ---
  # d/dk_j of -sum_i (t_i/lambda_j)^k_j = -sum_i (t_i/lambda_j)^k_j * log(t_i/lambda_j)
  rt_shape <- -t_over_s_k * log_t_over_s    # n x m
  # d/dlambda_j of -sum_i (t_i/lambda_j)^k_j = sum_i k_j/lambda_j * (t_i/lambda_j)^k_j
  rt_scale <- t_over_s_k * rep(shapes / scales, each = n)  # n x m

  shape_scores <- colSums(rt_shape)
  scale_scores <- colSums(rt_scale)

  # --- Masking term gradients (uncensored observations only) ---
  if (any(delta)) {
    idx <- which(delta)
    t_s_unc <- t_over_s[idx, , drop = FALSE]       # n_unc x m
    C_unc <- C[idx, , drop = FALSE]                 # n_unc x m
    t_unc <- t[idx]                                  # n_unc

    # Hazard h_j(t_i) = k_j/lambda_j * (t_i/lambda_j)^(k_j-1)
    H <- t_s_unc ^ rep(shapes - 1, each = length(idx))
    H <- H * rep(shapes / scales, each = length(idx))
    H_masked <- H * C_unc                           # zero out non-candidates
    denom <- rowSums(H_masked)                       # n_unc

    # d/dk_j: numerator = (1/t_i) * (t_i/lambda_j)^k_j * (1 + k_j * log(t_i/lambda_j))
    log_t_s_unc <- log(t_s_unc)
    t_s_k_unc <- t_s_unc ^ rep(shapes, each = length(idx))
    numer_shape <- (1 / t_unc) * t_s_k_unc *
                   (1 + rep(shapes, each = length(idx)) * log_t_s_unc)
    numer_shape <- numer_shape * C_unc
    mask_shape <- numer_shape / denom                # n_unc x m

    # d/dlambda_j: numerator = (k_j/lambda_j)^2 * (t_i/lambda_j)^(k_j-1)
    numer_scale <- rep((shapes / scales)^2, each = length(idx)) *
                   t_s_unc ^ rep(shapes - 1, each = length(idx))
    numer_scale <- numer_scale * C_unc
    mask_scale <- numer_scale / denom                # n_unc x m

    shape_scores <- shape_scores + colSums(mask_shape)
    scale_scores <- scale_scores - colSums(mask_scale)
  }

  # Interleave into theta-format gradient
  grad <- numeric(2 * m)
  grad[seq(1, 2 * m, 2)] <- shape_scores
  grad[seq(2, 2 * m, 2)] <- scale_scores
  grad
}

# ---------------------------------------------------------------------------
# Vectorized log-likelihood wrapper accepting theta in interleaved format
# (for use as optim fn)
# ---------------------------------------------------------------------------
loglik_vec_theta <- function(theta, t, delta, C) {
  m <- length(theta) %/% 2
  shapes <- theta[seq(1, 2 * m, 2)]
  scales <- theta[seq(2, 2 * m, 2)]
  loglik_vec(shapes, scales, t, delta, C)
}

# ---------------------------------------------------------------------------
# Vectorized score wrapper accepting theta in interleaved format
# (for use as optim gr)
# ---------------------------------------------------------------------------
score_vec_theta <- function(theta, t, delta, C) {
  m <- length(theta) %/% 2
  shapes <- theta[seq(1, 2 * m, 2)]
  scales <- theta[seq(2, 2 * m, 2)]
  score_vec(shapes, scales, t, delta, C)
}

# ---------------------------------------------------------------------------
# Vectorized log-likelihood for the REDUCED model (common shape k)
# Parameters: par = c(k, lambda_1, ..., lambda_m)
# ---------------------------------------------------------------------------
loglik_reduced_vec <- function(par, t, delta, C) {
  k <- par[1]
  scales <- par[-1]
  m <- length(scales)
  shapes <- rep(k, m)
  loglik_vec(shapes, scales, t, delta, C)
}

# ---------------------------------------------------------------------------
# Vectorized gradient for the REDUCED model (common shape k)
#
# The full-model gradient gives d/dk_j for each j. Under the constraint
# k_1 = ... = k_m = k, the chain rule gives: d/dk = sum_j d/dk_j
# Scale gradients are unchanged.
# ---------------------------------------------------------------------------
score_reduced_vec <- function(par, t, delta, C) {
  k <- par[1]
  scales <- par[-1]
  m <- length(scales)
  shapes <- rep(k, m)

  full_grad <- score_vec(shapes, scales, t, delta, C)

  # d/dk = sum of all shape gradients (chain rule for shared parameter)
  shape_grads <- full_grad[seq(1, 2 * m, 2)]
  scale_grads <- full_grad[seq(2, 2 * m, 2)]

  c(sum(shape_grads), scale_grads)
}

# ---------------------------------------------------------------------------
# Vectorized log-likelihood for REDUCED MODEL 2 (common shape AND common scale)
# Parameters: par = c(k, lambda)
# ---------------------------------------------------------------------------
loglik_reduced2_vec <- function(par, t, delta, C) {
  k <- par[1]
  lambda <- par[2]
  m <- ncol(C)
  shapes <- rep(k, m)
  scales <- rep(lambda, m)
  loglik_vec(shapes, scales, t, delta, C)
}

# ---------------------------------------------------------------------------
# Vectorized gradient for REDUCED MODEL 2 (common shape AND common scale)
# d/dk = sum_j d/dk_j, d/dlambda = sum_j d/dlambda_j
# ---------------------------------------------------------------------------
score_reduced2_vec <- function(par, t, delta, C) {
  k <- par[1]
  lambda <- par[2]
  m <- ncol(C)
  shapes <- rep(k, m)
  scales <- rep(lambda, m)

  full_grad <- score_vec(shapes, scales, t, delta, C)

  shape_grads <- full_grad[seq(1, 2 * m, 2)]
  scale_grads <- full_grad[seq(2, 2 * m, 2)]

  c(sum(shape_grads), sum(scale_grads))
}

# ---------------------------------------------------------------------------
# Fit full model (pre-decoded data, vectorized loglik+gradient, L-BFGS-B)
# Returns same structure as optim() result
# ---------------------------------------------------------------------------
fit_full_model <- function(theta0, t, delta, C, max_iter = 1000L) {
  stats::optim(
    par = theta0,
    fn = loglik_vec_theta,
    gr = score_vec_theta,
    t = t, delta = delta, C = C,
    method = "L-BFGS-B",
    lower = rep(0.001, length(theta0)),
    control = list(fnscale = -1, maxit = max_iter, parscale = theta0)
  )
}

# ---------------------------------------------------------------------------
# Fit reduced model (common shape)
#
# Strategy: L-BFGS-B with gradient for speed, then Nelder-Mead from the
# L-BFGS-B solution to escape local optima (the common-shape likelihood
# surface is multimodal). Returns the better of the two fits.
#
# par0 = c(k_hat, scales_mle)
# Returns same structure as optim() result
# ---------------------------------------------------------------------------
fit_reduced_model <- function(par0, t, delta, C, max_iter = 1000L) {
  # Fast L-BFGS-B with analytical gradient
  sol_lb <- stats::optim(
    par = par0,
    fn = loglik_reduced_vec,
    gr = score_reduced_vec,
    t = t, delta = delta, C = C,
    method = "L-BFGS-B",
    lower = rep(0.001, length(par0)),
    control = list(fnscale = -1, maxit = max_iter)
  )

  # Nelder-Mead from L-BFGS-B solution (escapes local optima)
  sol_nm <- stats::optim(
    par = sol_lb$par,
    fn = loglik_reduced_vec,
    t = t, delta = delta, C = C,
    control = list(fnscale = -1, maxit = max_iter)
  )

  # Return whichever found the higher log-likelihood
  best <- if (sol_nm$value > sol_lb$value) sol_nm else sol_lb
  # Propagate convergence: 0 only if both stages converged
  best$convergence <- max(sol_lb$convergence, sol_nm$convergence)
  best
}

# ---------------------------------------------------------------------------
# Fit reduced model 2 (common shape AND common scale, L-BFGS-B)
# par0 = c(k_hat, scale_hat)
# ---------------------------------------------------------------------------
fit_reduced2_model <- function(par0, t, delta, C, max_iter = 1000L) {
  stats::optim(
    par = par0,
    fn = loglik_reduced2_vec,
    gr = score_reduced2_vec,
    t = t, delta = delta, C = C,
    method = "L-BFGS-B",
    lower = rep(0.001, length(par0)),
    control = list(fnscale = -1, maxit = max_iter)
  )
}
