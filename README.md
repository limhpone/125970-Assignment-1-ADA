# Interval Scheduling Assignment

## Project Structure

```
├── src/
│   ├── dataset_generator.py    # Generate synthetic interval datasets
│   ├── greedy_algorithms.py    # EFT, EST, SD implementations
│   ├── exhaustive_solver.py    # Optimal solution finder
│   ├── benchmark.py            # Runtime measurement framework
│   └── plotting.py             # Visualization utilities
├── main.py                     # Main execution script
├── requirements.txt            # Python dependencies
└── results/                    # Output directory for plots and data
```

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run experiments:
   ```bash
   python main.py
   ```
python main.py

python run_experiments.py

# Activate environment
.\.venv\Scripts\Activate.ps1

# Run full experiment (~45 min)
python main.py

## Algorithms Implemented

- **Greedy Algorithms**: EFT, EST, SD (O(n log n))
- **Exhaustive Algorithm**: Optimal solver (O(n·2^n))

## Experimental Protocol

- 3 overlap regimes: α = 0.1, 1, 5
- 10+ trials per configuration
- Big-O validation plots
- Solution quality analysis
