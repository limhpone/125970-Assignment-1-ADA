from __future__ import annotations
import argparse, os, time, csv, statistics
import numpy as np

from datasets import generate_uniform_intervals
from greedy import greedy_earliest_finish, greedy_earliest_start, greedy_shortest_duration
from exhaustive import exhaustive_optimal

def _now():
    return time.perf_counter()

def run_greedy_suite(intervals: np.ndarray):
    # Return counts for all three greedy criteria
    return {
        "EFT": greedy_earliest_finish(intervals).count,
        "EST": greedy_earliest_start(intervals).count,
        "SD":  greedy_shortest_duration(intervals).count,
    }

def time_fn(fn, *args, warmup: bool=True, repeat: int=1):
    # High-resolution timer; optional warmup call
    if warmup:
        fn(*args)
    t0 = _now()
    for _ in range(repeat):
        fn(*args)
    t1 = _now()
    return (t1 - t0) / repeat

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def benchmark_greedy(results_dir: str, trials: int, D: int, alphas: list[float], n_pows: list[int], seed: int):
    ensure_dir(results_dir)
    out_csv = os.path.join(results_dir, "greedy_results.csv")

    rng = np.random.default_rng(seed)

    # CSV header
    header = [
        "alpha","D","n","trial",
        "t_EFT","t_EST","t_SD",
        "count_EFT","count_EST","count_SD"
    ]

    total_runs = len(alphas) * len(n_pows) * trials
    run_count = 0

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)

        for alpha in alphas:
            for p in n_pows:
                n = 2 ** p
                print(f"\n[Progress] alpha={alpha}, n=2^{p}={n}")
                # Generate once per trial but EXCLUDE generation time from timing
                for trial in range(1, trials+1):
                    run_count += 1
                    print(f"  Trial {trial}/{trials} (Run {run_count}/{total_runs})...", end=" ", flush=True)
                    intervals, _ = generate_uniform_intervals(n=n, D=D, alpha=alpha, rng=rng)

                    # Warm-up run (excluded): call each algo once on a small slice to "warm" Python internals.
                    _ = run_greedy_suite(intervals[: min(2000, n)])

                    # Time each greedy algorithm (exclude generation time)
                    t_eft = time_fn(greedy_earliest_finish, intervals, warmup=False)
                    t_est = time_fn(greedy_earliest_start,  intervals, warmup=False)
                    t_sd  = time_fn(greedy_shortest_duration, intervals, warmup=False)

                    counts = run_greedy_suite(intervals)

                    w.writerow([
                        alpha, D, n, trial,
                        t_eft, t_est, t_sd,
                        counts["EFT"], counts["EST"], counts["SD"]
                    ])
                    print(f"Done! (EFT: {t_eft:.6f}s, EST: {t_est:.6f}s, SD: {t_sd:.6f}s)")
                f.flush()  # Flush after each n value to save progress

    print(f"[OK] Saved greedy trials to: {out_csv}")

def benchmark_exhaustive(results_dir: str, trials: int, D: int, alphas: list[float], n_list: list[int], seed: int):
    ensure_dir(results_dir)
    out_csv = os.path.join(results_dir, "exhaustive_results.csv")

    rng = np.random.default_rng(seed)

    header = [
        "alpha","D","n","trial",
        "t_exhaustive","opt_count",
        "greedy_EFT_count","greedy_EST_count","greedy_SD_count"
    ]

    total_runs = len(alphas) * len(n_list) * trials
    run_count = 0

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)

        for alpha in alphas:
            for n in n_list:
                print(f"\n[Progress] alpha={alpha}, n={n}")
                for trial in range(1, trials+1):
                    run_count += 1
                    print(f"  Trial {trial}/{trials} (Run {run_count}/{total_runs})...", end=" ", flush=True)
                    intervals, _ = generate_uniform_intervals(n=n, D=D, alpha=alpha, rng=rng)

                    # Warm-up (excluded)
                    _ = exhaustive_optimal(intervals[: min(n, 10)], return_selected=False)

                    # Time exhaustive (exclude generation time)
                    t_opt = time_fn(exhaustive_optimal, intervals, False, warmup=False)

                    opt = exhaustive_optimal(intervals, return_selected=False).count
                    greedy_counts = run_greedy_suite(intervals)

                    w.writerow([
                        alpha, D, n, trial,
                        t_opt, opt,
                        greedy_counts["EFT"], greedy_counts["EST"], greedy_counts["SD"]
                    ])
                    print(f"Done! (Exhaustive: {t_opt:.6f}s, opt_count={opt})")
                f.flush()  # Flush after each n value to save progress

    print(f"[OK] Saved exhaustive trials to: {out_csv}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["greedy","exhaustive"], required=True)
    ap.add_argument("--results_dir", default="results")
    ap.add_argument("--trials", type=int, default=10)
    ap.add_argument("--D", type=int, default=10)
    ap.add_argument("--alphas", type=float, nargs="+", default=[0.1, 1.0, 5.0])
    ap.add_argument("--seed", type=int, default=0)

    # Greedy input sizes: 2^10..2^20
    ap.add_argument("--n_pow_min", type=int, default=10)
    ap.add_argument("--n_pow_max", type=int, default=20)

    # Exhaustive input sizes (you can override)
    ap.add_argument("--exhaustive_n", type=int, nargs="+", default=[5,10,15,20])

    args = ap.parse_args()

    if args.mode == "greedy":
        n_pows = list(range(args.n_pow_min, args.n_pow_max+1))
        benchmark_greedy(
            results_dir=args.results_dir,
            trials=args.trials,
            D=args.D,
            alphas=args.alphas,
            n_pows=n_pows,
            seed=args.seed
        )
    else:
        benchmark_exhaustive(
            results_dir=args.results_dir,
            trials=args.trials,
            D=args.D,
            alphas=args.alphas,
            n_list=args.exhaustive_n,
            seed=args.seed
        )

if __name__ == "__main__":
    main()
