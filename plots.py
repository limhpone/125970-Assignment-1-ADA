from __future__ import annotations
import argparse, os, math
import numpy as np
import matplotlib.pyplot as plt

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def load_csv(path: str):
    import csv
    with open(path, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        rows = list(r)
    return rows

def _group(rows, keys):
    groups = {}
    for row in rows:
        k = tuple(row[key] for key in keys)
        groups.setdefault(k, []).append(row)
    return groups

def plot_greedy(results_dir: str, out_dir: str):
    greedy_path = os.path.join(results_dir, "greedy_results.csv")
    if not os.path.exists(greedy_path):
        print(f"[SKIP] Missing {greedy_path}")
        return

    rows = load_csv(greedy_path)

    # Convert numeric fields
    for r in rows:
        for k in ["alpha","D","n","trial","t_EFT","t_EST","t_SD","count_EFT","count_EST","count_SD"]:
            r[k] = float(r[k]) if k in ["alpha","t_EFT","t_EST","t_SD"] else int(r[k])

    groups = _group(rows, keys=["alpha","D","n"])

    # Aggregate mean and std
    agg = []
    for (alpha, D, n), rs in groups.items():
        t_eft = np.array([x["t_EFT"] for x in rs], dtype=float)
        t_est = np.array([x["t_EST"] for x in rs], dtype=float)
        t_sd  = np.array([x["t_SD"]  for x in rs], dtype=float)
        agg.append({
            "alpha": float(alpha),
            "D": int(D),
            "n": int(n),
            "t_EFT_mean": float(t_eft.mean()),
            "t_EST_mean": float(t_est.mean()),
            "t_SD_mean":  float(t_sd.mean()),
        })

    # Plot per alpha: runtime t(n) vs n (log-log)
    for alpha in sorted(set(a["alpha"] for a in agg)):
        data = sorted([a for a in agg if a["alpha"] == alpha], key=lambda x: x["n"])
        n = np.array([d["n"] for d in data], dtype=float)
        t_eft = np.array([d["t_EFT_mean"] for d in data], dtype=float)
        t_est = np.array([d["t_EST_mean"] for d in data], dtype=float)
        t_sd  = np.array([d["t_SD_mean"]  for d in data], dtype=float)

        plt.figure()
        plt.plot(n, t_eft, marker="o", label="EFT")
        plt.plot(n, t_est, marker="o", label="EST")
        plt.plot(n, t_sd,  marker="o", label="SD")
        plt.xscale("log", base=2)
        plt.yscale("log")
        plt.xlabel("n (number of intervals)")
        plt.ylabel("runtime t(n) (seconds)")
        plt.title(f"Greedy Runtime vs n (log-log), alpha={alpha}")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"greedy_runtime_loglog_alpha_{alpha}.png"), dpi=200)
        plt.close()

        # Normalized runtime: t(n)/(n log2 n)
        denom = n * np.log2(n)
        plt.figure()
        plt.plot(n, t_eft/denom, marker="o", label="EFT")
        plt.plot(n, t_est/denom, marker="o", label="EST")
        plt.plot(n, t_sd/denom,  marker="o", label="SD")
        plt.xscale("log", base=2)
        plt.xlabel("n (number of intervals)")
        plt.ylabel("t(n) / (n log2 n)")
        plt.title(f"Greedy Normalized Runtime, alpha={alpha}")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"greedy_normalized_alpha_{alpha}.png"), dpi=200)
        plt.close()

    print(f"[OK] Greedy plots saved to: {out_dir}")

def plot_exhaustive(results_dir: str, out_dir: str):
    ex_path = os.path.join(results_dir, "exhaustive_results.csv")
    if not os.path.exists(ex_path):
        print(f"[SKIP] Missing {ex_path}")
        return

    rows = load_csv(ex_path)
    for r in rows:
        for k in ["alpha","D","n","trial","t_exhaustive","opt_count","greedy_EFT_count","greedy_EST_count","greedy_SD_count"]:
            r[k] = float(r[k]) if k in ["alpha","t_exhaustive"] else int(r[k])

    groups = _group(rows, keys=["alpha","D","n"])
    agg = []
    for (alpha, D, n), rs in groups.items():
        t = np.array([x["t_exhaustive"] for x in rs], dtype=float)
        agg.append({
            "alpha": float(alpha),
            "D": int(D),
            "n": int(n),
            "t_mean": float(t.mean()),
        })

    for alpha in sorted(set(a["alpha"] for a in agg)):
        data = sorted([a for a in agg if a["alpha"] == alpha], key=lambda x: x["n"])
        n = np.array([d["n"] for d in data], dtype=float)
        t = np.array([d["t_mean"] for d in data], dtype=float)

        # Runtime vs n
        plt.figure()
        plt.plot(n, t, marker="o")
        plt.xlabel("n (number of intervals)")
        plt.ylabel("runtime t(n) (seconds)")
        plt.title(f"Exhaustive Runtime vs n, alpha={alpha}")
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"exhaustive_runtime_alpha_{alpha}.png"), dpi=200)
        plt.close()

        # Normalized: t(n)/(n 2^n)
        denom = n * (2.0 ** n)
        plt.figure()
        plt.plot(n, t/denom, marker="o")
        plt.xlabel("n (number of intervals)")
        plt.ylabel("t(n) / (n 2^n)")
        plt.title(f"Exhaustive Normalized Runtime, alpha={alpha}")
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"exhaustive_normalized_alpha_{alpha}.png"), dpi=200)
        plt.close()

    print(f"[OK] Exhaustive plots saved to: {out_dir}")

def plot_approximation_ratios(results_dir: str, out_dir: str):
    """Plot greedy approximation ratios (greedy_count / optimal_count) across different alpha values."""
    ex_path = os.path.join(results_dir, "exhaustive_results.csv")
    if not os.path.exists(ex_path):
        print(f"[SKIP] Missing {ex_path} for approximation ratio analysis")
        return

    rows = load_csv(ex_path)
    for r in rows:
        for k in ["alpha","D","n","trial","t_exhaustive","opt_count","greedy_EFT_count","greedy_EST_count","greedy_SD_count"]:
            r[k] = float(r[k]) if k in ["alpha","t_exhaustive"] else int(r[k])

    # Group by (alpha, D, n) and compute mean approximation ratios
    groups = _group(rows, keys=["alpha","D","n"])
    agg = []
    for (alpha, D, n), rs in groups.items():
        opt_counts = np.array([x["opt_count"] for x in rs], dtype=float)
        eft_counts = np.array([x["greedy_EFT_count"] for x in rs], dtype=float)
        est_counts = np.array([x["greedy_EST_count"] for x in rs], dtype=float)
        sd_counts = np.array([x["greedy_SD_count"] for x in rs], dtype=float)
        
        # Compute ratios (avoid division by zero)
        eft_ratios = np.where(opt_counts > 0, eft_counts / opt_counts, 1.0)
        est_ratios = np.where(opt_counts > 0, est_counts / opt_counts, 1.0)
        sd_ratios = np.where(opt_counts > 0, sd_counts / opt_counts, 1.0)
        
        agg.append({
            "alpha": float(alpha),
            "D": int(D),
            "n": int(n),
            "eft_ratio_mean": float(eft_ratios.mean()),
            "est_ratio_mean": float(est_ratios.mean()),
            "sd_ratio_mean": float(sd_ratios.mean()),
            "eft_ratio_std": float(eft_ratios.std()),
            "est_ratio_std": float(est_ratios.std()),
            "sd_ratio_std": float(sd_ratios.std()),
        })

    # Plot approximation ratios for each n value: ratio vs alpha
    n_values = sorted(set(a["n"] for a in agg))
    for n in n_values:
        data = sorted([a for a in agg if a["n"] == n], key=lambda x: x["alpha"])
        if len(data) == 0:
            continue
            
        alphas = np.array([d["alpha"] for d in data], dtype=float)
        eft_ratio = np.array([d["eft_ratio_mean"] for d in data], dtype=float)
        est_ratio = np.array([d["est_ratio_mean"] for d in data], dtype=float)
        sd_ratio = np.array([d["sd_ratio_mean"] for d in data], dtype=float)
        eft_ratio_std = np.array([d["eft_ratio_std"] for d in data], dtype=float)
        est_ratio_std = np.array([d["est_ratio_std"] for d in data], dtype=float)
        sd_ratio_std = np.array([d["sd_ratio_std"] for d in data], dtype=float)

        plt.figure(figsize=(8, 6))
        plt.errorbar(alphas, eft_ratio, yerr=eft_ratio_std, label="EFT", capsize=5, linewidth=2, alpha=0.8)
        plt.errorbar(alphas, est_ratio, yerr=est_ratio_std, label="EST", capsize=5, linewidth=2, alpha=0.8)
        plt.errorbar(alphas, sd_ratio, yerr=sd_ratio_std, label="SD", capsize=5, linewidth=2, alpha=0.8)
        plt.axhline(y=1.0, color='gray', linestyle='--', linewidth=1, label='Optimal (ratio=1.0)')
        plt.xlabel("α (overlap density parameter)", fontsize=12)
        plt.ylabel("Approximation Ratio (greedy / optimal)", fontsize=12)
        plt.title(f"Greedy Approximation Ratios vs α (n={n})", fontsize=14)
        plt.ylim(0.5, 1.05)  # Focus on the relevant range
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"approximation_ratios_n_{n}.png"), dpi=200)
        plt.close()

    # Also create a heatmap-style plot showing how ratios vary with both n and alpha
    # For each algorithm, create a separate heatmap
    for algo_name, ratio_key, std_key in [("EFT", "eft_ratio_mean", "eft_ratio_std"),
                                            ("EST", "est_ratio_mean", "est_ratio_std"),
                                            ("SD", "sd_ratio_mean", "sd_ratio_std")]:
        # Create matrix: rows=n, cols=alpha
        alphas_sorted = sorted(set(a["alpha"] for a in agg))
        n_sorted = sorted(set(a["n"] for a in agg))
        
        matrix = np.zeros((len(n_sorted), len(alphas_sorted)))
        for i, n in enumerate(n_sorted):
            for j, alpha in enumerate(alphas_sorted):
                matches = [a for a in agg if a["n"] == n and a["alpha"] == alpha]
                if matches:
                    matrix[i, j] = matches[0][ratio_key]
                else:
                    matrix[i, j] = np.nan
        
        plt.figure(figsize=(8, 6))
        im = plt.imshow(matrix, aspect='auto', cmap='RdYlGn', vmin=0.5, vmax=1.0, interpolation='nearest')
        plt.colorbar(im, label='Approximation Ratio')
        plt.xticks(range(len(alphas_sorted)), [f"{a:.1f}" for a in alphas_sorted])
        plt.yticks(range(len(n_sorted)), [str(n) for n in n_sorted])
        plt.xlabel("α (overlap density)", fontsize=12)
        plt.ylabel("n (number of intervals)", fontsize=12)
        plt.title(f"{algo_name} Approximation Ratio Heatmap", fontsize=14)
        
        # Add text annotations
        for i in range(len(n_sorted)):
            for j in range(len(alphas_sorted)):
                if not np.isnan(matrix[i, j]):
                    text = plt.text(j, i, f"{matrix[i, j]:.3f}",
                                   ha="center", va="center", color="black", fontsize=9)
        
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"approximation_heatmap_{algo_name}.png"), dpi=200)
        plt.close()

    print(f"[OK] Approximation ratio plots saved to: {out_dir}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results_dir", default="results")
    ap.add_argument("--out_dir", default=None)
    args = ap.parse_args()

    out_dir = args.out_dir or os.path.join(args.results_dir, "plots")
    ensure_dir(out_dir)

    plot_greedy(args.results_dir, out_dir)
    plot_exhaustive(args.results_dir, out_dir)
    plot_approximation_ratios(args.results_dir, out_dir)

if __name__ == "__main__":
    main()
