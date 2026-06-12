library(parallel)
library(boot)
library(stats)
library(algebraic.mle)
library(algebraic.dist)
library(md.tools)
library(wei.series.md.c1.c2.c3)

# Source shared vectorized utilities
source("../sim_utils.R")

set.seed(2024)

theta <- c(shape1 = 1.2576, scale1 = 994.3661,
           shape2 = 1.1635, scale2 = 908.9458,
           shape3 = NA,     scale3 = 840.1141,
           shape4 = 1.1802, scale4 = 940.1342,
           shape5 = 1.2034, scale5 = 923.1631)

shapes3 <- rep(c(0.9, 1.0, 1.1308, 1.2, 1.3), 100)
N <- c(100)
P <- c(0.215)
Q <- c(0.825)
R <- 2
B <- 1000
max_iter <- 125L
max_boot_iter <- 125L
total_retries <- 10000L
# Auto-detect cores (leave 2 for OS/other tasks)
n_cores <- max(2L, parallel::detectCores() - 2L)

experiment.name <- "boot-prob-shape3-vary"
csv.out <- paste0(experiment.name, ".csv")

probs3_fn <- list()
probs1_fn <- list()

for (shape3 in shapes3) {
    theta["shape3"] <- shape3
    shapes <- theta[seq(1, length(theta), 2)]
    scales <- theta[seq(2, length(theta), 2)]

    tryCatch({
        probs1_fn[[as.character(shape3)]] <- wei.series.md.c1.c2.c3::wei_series_cause(k = 1L, shape = shapes, scale = scales)
        probs3_fn[[as.character(shape3)]] <- wei.series.md.c1.c2.c3::wei_series_cause(k = 3L, shapes = shapes, scales = scales)
    },
    error = function(e) {
        probs1_fn[[as.character(shape3)]] <<- wei.series.md.c1.c2.c3::wei_series_cause(k = 1L, shapes = shapes, scales = scales,
            mc = TRUE, n = 300000L)
        probs3_fn[[as.character(shape3)]] <<- wei.series.md.c1.c2.c3::wei_series_cause(k = 3L, shapes = shapes, scales = scales,
            mc = TRUE, n = 300000L)
    })
}

# Resume logic: read existing data if present
completed_counts <- list()
if (file.exists(csv.out)) {
  existing <- read.csv(csv.out)
  if (nrow(existing) > 0) {
    counts <- table(existing$shapes1)
    for (nm in names(counts)) {
      completed_counts[[nm]] <- as.integer(counts[nm])
    }
    cat("Resuming: found", nrow(existing), "existing rows across",
        length(completed_counts), "conditions\n")
  }
}

n_errors <- 0
iter_idx <- 0L
running_counts <- list()

options(digits = 5, scipen = 999)
for (shape3 in shapes3) {
    iter_idx <- iter_idx + 1L
    s3_key <- as.character(shape3)

    # Track running count for this condition
    if (is.null(running_counts[[s3_key]])) running_counts[[s3_key]] <- 0L
    running_counts[[s3_key]] <- running_counts[[s3_key]] + 1L

    # Skip if this iteration's worth of rows already exists
    n_done_rows <- if (!is.null(completed_counts[[s3_key]])) completed_counts[[s3_key]] else 0L
    n_done_iters <- n_done_rows %/% R  # each iteration writes R rows
    if (running_counts[[s3_key]] <= n_done_iters) {
      next
    }

    # Per-iteration reproducible seed
    set.seed(2024 * 1000 + iter_idx)

    for (n in N) {
        for (p in P) {
            for (q in Q) {

                theta["shape3"] <- shape3
                shapes <- theta[seq(1, length(theta), 2)]
                scales <- theta[seq(2, length(theta), 2)]

                tau <- wei.series.md.c1.c2.c3::qwei_series(p = q, scales = scales, shapes = shapes)
                shapes.mle <- matrix(NA, nrow = R, ncol = length(theta) / 2)
                scales.mle <- matrix(NA, nrow = R, ncol = length(theta) / 2)

                shapes.lower <- matrix(NA, nrow = R, ncol = length(theta) / 2)
                shapes.upper <- matrix(NA, nrow = R, ncol = length(theta) / 2)
                scales.lower <- matrix(NA, nrow = R, ncol = length(theta) / 2)
                scales.upper <- matrix(NA, nrow = R, ncol = length(theta) / 2)

                cat("[starting] scenario(shapes: ", shapes, ", scales: ", scales, ", n: ", n, ", p: ", p, ", q: ", q, ")\n")
                iter <- 0L
                repeat {
                    retry <- FALSE
                    tryCatch({
                        repeat {
                            df <- wei.series.md.c1.c2.c3::generate_guo_weibull_table_2_data(
                                shapes = shapes, scales = scales, n = n, p = p, tau = tau)

                            # Pre-decode data for initial MLE fit
                            dd <- decode_data(df)
                            sol <- fit_full_model(theta0 = theta, t = dd$t,
                                                  delta = dd$delta, C = dd$C,
                                                  max_iter = max_iter)
                            if (sol$convergence == 0) {
                                break
                            }
                            cat("[", iter, "] MLE did not converge, retrying...\n")
                        }

                        # Bootstrap MLE solver using vectorized fitting
                        mle_solver <- function(df, i) {
                            dd_b <- decode_data(df[i, ])
                            solb <- fit_full_model(theta0 = sol$par, t = dd_b$t,
                                                   delta = dd_b$delta, C = dd_b$C,
                                                   max_iter = max_boot_iter)
                            solb$par
                        }

                        sol.boot <- boot::boot(df, mle_solver,
                            R = B, parallel = "multicore", ncpus = n_cores)
                    },
                    error = function(e) {
                        cat("[error] ", conditionMessage(e), "\n")
                        n_errors <<- n_errors + 1
                        cat("[retrying scenario n = ", n, ", p = ", p, ", q = ", q, "]")
                    })
                    if (retry) {
                        next
                    }
                    iter <- iter + 1L
                    shapes.mle[iter,] <- sol$par[seq(1, length(theta), 2)]
                    scales.mle[iter,] <- sol$par[seq(2, length(theta), 2)]

                    tryCatch({
                        sb <- mle_boot(sol.boot)
                        ci <- confint(sb, type = "bca", level = 0.95)
                        shapes.ci <- ci[seq(1, length(theta), 2), ]
                        scales.ci <- ci[seq(2, length(theta), 2), ]
                        shapes.lower[iter, ] <- shapes.ci[, 1]
                        shapes.upper[iter, ] <- shapes.ci[, 2]
                        scales.lower[iter, ] <- scales.ci[, 1]
                        scales.upper[iter, ] <- scales.ci[, 2]
                    }, error = function(e) {
                        cat("[bootstrap error: ", conditionMessage(e), "]\n")
                    })

                    if (iter %% 1 == 0) {
                        cat("[iteration ", iter, "] shape mles: ", shapes.mle[iter,], ", scale mles = ", scales.mle[iter, ], "\n")

                    }
                    if (iter == R) {
                        break
                    }
                }

                df <- data.frame(
                    n = rep(n, R),
                    p = rep(p, R),
                    q = rep(q, R),
                    prob3 = rep(probs3_fn[[as.character(shape3)]], R),
                    mttf3 = rep(wei.series.md.c1.c2.c3::wei_mttf(shape = shapes[3], scale = scales[3]), R),
                    prob1 = rep(probs1_fn[[as.character(shape3)]], R),
                    mttf1 = rep(wei.series.md.c1.c2.c3::wei_mttf(shape = shapes[1], scale = scales[1]), R),
                    mttf = rep(wei.series.md.c1.c2.c3::wei_series_mttf(shapes = shapes, scales = scales), R),
                    tau = rep(tau, R),
                    shapes1 = rep(shape3, R),
                    shape.mles = shapes.mle,
                    scale.mles = scales.mle,
                    shapes.lower = shapes.lower,
                    shapes.upper = shapes.upper,
                    scales.lower = scales.lower,
                    scales.upper = scales.upper)

                write.table(df, file = csv.out, sep = ",", row.names = FALSE,
                    col.names = !file.exists(csv.out), append = TRUE)
            }
        }
    }
}
cat("Completed with", n_errors, "errors\n")
