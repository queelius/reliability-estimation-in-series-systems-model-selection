library(stats)
library(algebraic.mle)
library(algebraic.dist)
library(md.tools)
library(wei.series.md.c1.c2.c3)

# Source shared vectorized utilities
source("../../sim_utils.R")

set.seed(2024)

theta <- c(shape1 = 1.2576, scale1 = 994.3661,
           shape2 = 1.1635, scale2 = 908.9458,
           shape3 = 1.1308, scale3 = 840.1141,
           shape4 = 1.1802, scale4 = 940.1342,
           shape5 = 1.2034, scale5 = 923.1631)

shapes <- theta[seq(1, length(theta), 2)]
scales <- theta[seq(2, length(theta), 2)]
m <- length(shapes)

csv.file <- "data-lrt-masked.csv"
N <- rep(c(50, 60, 70, 80, 90, 100), 100)
p <- .215
q <- .825
max_iter <- 1000L
tau <- qwei_series(p = q, scales = scales, shapes = shapes)

# Resume logic: read existing data if present
completed_counts <- list()
if (file.exists(csv.file)) {
  existing <- read.csv(csv.file)
  if (nrow(existing) > 0) {
    counts <- table(existing$n)
    for (nm in names(counts)) {
      completed_counts[[nm]] <- as.integer(counts[nm])
    }
    cat("Resuming: found", nrow(existing), "existing rows\n")
    for (nm in names(completed_counts)) {
      cat("  n =", nm, ":", completed_counts[[nm]], "rows\n")
    }
  }
} else {
  write.table(
    data.frame(n = integer(), pmask = numeric(), q = numeric(),
               p.value = numeric(), Lambda = numeric(),
               loglik.F = numeric(), loglik.R = numeric()),
    file = csv.file, sep = ",", row.names = FALSE, col.names = TRUE)
}

n_errors <- 0
n_total <- length(N)
running_counts <- list()

# Batch results by n value for efficient writes
current_n <- NULL
results_batch <- list()
batch_idx <- 0L

flush_batch <- function() {
  if (batch_idx > 0L) {
    write.table(do.call(rbind, results_batch[1:batch_idx]),
                file = csv.file, sep = ",", append = TRUE,
                row.names = FALSE, col.names = FALSE)
  }
  results_batch <<- list()
  batch_idx <<- 0L
}

for (i in seq_along(N)) {
  n <- N[i]
  n_key <- as.character(n)

  # Flush batch when n changes
  if (!is.null(current_n) && n != current_n) {
    flush_batch()
  }
  current_n <- n

  # Track running count for this n value
  if (is.null(running_counts[[n_key]])) running_counts[[n_key]] <- 0L
  running_counts[[n_key]] <- running_counts[[n_key]] + 1L

  # Skip if already completed
  n_done <- if (!is.null(completed_counts[[n_key]])) completed_counts[[n_key]] else 0L
  if (running_counts[[n_key]] <= n_done) next

  # Per-iteration reproducible seed
  set.seed(2024 * 1000 + i)

  tryCatch({
    df <- generate_guo_weibull_table_2_data(
        shapes = shapes, scales = scales, n = n, p = p, tau = tau)

    # Pre-decode data once
    dd <- decode_data(df)

    # Fit full model (vectorized)
    sol <- fit_full_model(theta0 = theta, t = dd$t, delta = dd$delta,
                          C = dd$C, max_iter = max_iter)

    if (sol$convergence != 0) {
        cat("Failed to converge, retrying.\n")
        next
    }
    shapes.mle <- sol$par[seq(1, length(theta), 2)]
    scales.mle <- sol$par[seq(2, length(theta), 2)]
    k.hat <- mean(shapes.mle)

    # Fit reduced model (vectorized + L-BFGS-B with gradient)
    sol.R <- fit_reduced_model(par0 = c(k.hat, scales.mle),
                               t = dd$t, delta = dd$delta, C = dd$C,
                               max_iter = max_iter)

    Lambda <- -2 * (sol.R$value - sol$value)
    p.value <- pchisq(Lambda, m-1, lower.tail = FALSE)

    cat("n =", n, "p-value =", p.value, ", Lambda =", Lambda, ", loglik.F =", sol$value, ", loglik.R =", sol.R$value, "\n")

    # Accumulate result
    batch_idx <- batch_idx + 1L
    results_batch[[batch_idx]] <- data.frame(
      n = n, pmask = p, q = q, p.value = p.value, Lambda = Lambda,
      loglik.F = sol$value, loglik.R = sol.R$value)

  }, error = function(e) {
    n_errors <<- n_errors + 1
    cat("[ERROR]", conditionMessage(e), "\n")
  })
}
# Flush remaining batch
flush_batch()

n_resumed <- sum(unlist(completed_counts))
cat("Completed:", n_total - n_errors, "/", n_total, "successful (", n_errors, "errors,", n_resumed, "resumed)\n")
