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
           shape3 = NA,     scale3 = 840.1141,
           shape4 = 1.1802, scale4 = 940.1342,
           shape5 = 1.2034, scale5 = 923.1631)

csv.file <- "data-lrt-masked-reduced-3.csv"
shapes3 <- c(0.25, 0.5, .75, 1, 1.1308, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3.0)
N <- rep(1000, 1000)
p <- .215
q <- .825
max_iter <- 1000L

# Resume logic: read existing data if present
completed_counts <- list()
if (file.exists(csv.file)) {
  existing <- read.csv(csv.file)
  if (nrow(existing) > 0) {
    counts <- table(existing$shape3)
    for (nm in names(counts)) {
      completed_counts[[nm]] <- as.integer(counts[nm])
    }
    cat("Resuming: found", nrow(existing), "existing rows\n")
    for (nm in names(completed_counts)) {
      cat("  shape3 =", nm, ":", completed_counts[[nm]], "rows\n")
    }
  }
} else {
  write.table(
    data.frame(n = integer(), pmask = numeric(), q = numeric(),
               shape3 = numeric(), p.value = numeric(), Lambda = numeric(),
               loglik.F = numeric(), loglik.R = numeric()),
    file = csv.file, sep = ",", row.names = FALSE, col.names = TRUE)
}

n_errors <- 0
n_total <- length(N) * length(shapes3)
iter_idx <- 0L
running_counts <- list()

# Batch results by shape3 for efficient writes
current_s3 <- NULL
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

for (n in N) {
for (shape3 in shapes3) {
    iter_idx <- iter_idx + 1L
    s3_key <- as.character(shape3)

    # Flush batch when shape3 changes
    if (!is.null(current_s3) && shape3 != current_s3) {
      flush_batch()
    }
    current_s3 <- shape3

    # Track running count for this shape3 value
    if (is.null(running_counts[[s3_key]])) running_counts[[s3_key]] <- 0L
    running_counts[[s3_key]] <- running_counts[[s3_key]] + 1L

    # Skip if already completed
    n_done <- if (!is.null(completed_counts[[s3_key]])) completed_counts[[s3_key]] else 0L
    if (running_counts[[s3_key]] <= n_done) next

    # Per-iteration reproducible seed
    set.seed(2024 * 1000 + iter_idx)
    theta['shape3'] <- shape3
    shapes <- theta[seq(1, length(theta), 2)]
    scales <- theta[seq(2, length(theta), 2)]
    m <- length(shapes)
    tau <- qwei_series(p = q, scales = scales, shapes = shapes)

    df <- generate_guo_weibull_table_2_data(
        shapes = shapes, scales = scales, n = n, p = p, tau = tau)
    tryCatch({
        # Pre-decode data once
        dd <- decode_data(df)

        # Fit full model (vectorized)
        sol <- fit_full_model(theta0 = theta, t = dd$t, delta = dd$delta,
                              C = dd$C, max_iter = max_iter)

        shapes.mle <- sol$par[seq(1, length(theta), 2)]
        scales.mle <- sol$par[seq(2, length(theta), 2)]
        k.hat <- mean(shapes.mle)

        # Fit reduced model (vectorized + L-BFGS-B with gradient)
        sol.R <- fit_reduced_model(par0 = c(k.hat, scales.mle),
                                   t = dd$t, delta = dd$delta, C = dd$C,
                                   max_iter = max_iter)

        Lambda <- -2 * (sol.R$value - sol$value)
        p.value <- pchisq(Lambda, m-1, lower.tail = FALSE)

        cat("n =", n, ", shape3 =", shape3,  ", p-value =", p.value, ", Lambda =", Lambda, ", loglik.F =", sol$value, ", loglik.R =", sol.R$value, "\n")

        # Accumulate result
        batch_idx <- batch_idx + 1L
        results_batch[[batch_idx]] <- data.frame(
          n = n, pmask = p, q = q, shape3 = shape3, p.value = p.value, Lambda = Lambda,
          loglik.F = sol$value, loglik.R = sol.R$value)

    }, error = function(e) {
      n_errors <<- n_errors + 1
      cat("[ERROR n=", n, "shape3=", shape3, "]", conditionMessage(e), "\n")
    })
}
}
# Flush remaining batch
flush_batch()

n_resumed <- sum(unlist(completed_counts))
cat("Completed:", n_total - n_errors, "/", n_total, "successful (", n_errors, "errors,", n_resumed, "resumed)\n")
