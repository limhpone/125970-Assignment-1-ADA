# Interval Scheduling — Empirical Runtime & Optimality Study

**Aye Khin Khin Hpone-Yolanda Lim (st125970)**

This project matches the assignment spec:
- 3 greedy algorithms: EFT, EST, SD (each O(n log n))
- 1 exhaustive optimal solver for small n (subset enumeration)
- Controlled synthetic datasets using T = α · n · D with α in {0.1, 1, 5}
- Benchmarking with >=10 trials, warm-up, high-resolution timer
- Big-O validation plots (raw + normalized)

## Quick start
1) Install deps:
```bash
pip install -r requirements.txt
```

2) Run greedy benchmarks (default: n = 2^10..2^20, trials=10, regimes α = 0.1,1,5):
```bash
python benchmark.py --mode greedy
```

3) Run exhaustive benchmarks (default: n = 5,10,15,... up to n_max you set):
```bash
python benchmark.py --mode exhaustive --exhaustive_n 5 10 15 20
```

4) Generate plots from saved results:
```bash
python plots.py --results_dir results
```

Outputs:
- `results/*.csv` (trial summaries)
- `results/plots/*.png` (required plots)
- Use `report_template.md` for your report write-up.

## Notes
- Timing excludes dataset generation time (as required).
- Greedy algorithms return the number of selected intervals and (optionally) the chosen set.
- Exhaustive solver is intended only for small n; it is exponential.
