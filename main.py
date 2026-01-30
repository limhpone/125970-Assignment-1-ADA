"""
Main Execution Script for Interval Scheduling Assignment
Runs all experiments and generates plots for the report.
"""

import os
import json
import numpy as np
from src.dataset_generator import IntervalGenerator
from src.greedy_algorithms import (
    earliest_finish_time, 
    earliest_start_time, 
    shortest_duration
)
from src.exhaustive_solver import exhaustive_search_optimized
from src.benchmark import (
    benchmark_greedy_algorithms,
    benchmark_exhaustive_algorithm
)
from src.plotting import (
    plot_greedy_runtime_loglog,
    plot_greedy_normalized_runtime,
    plot_exhaustive_runtime,
    plot_exhaustive_normalized_runtime,
    plot_solution_quality
)


def run_greedy_experiments():
    # Run all greedy algorithm tests
    print("\n" + "="*50)
    print("Greedy Algorithms")
    print("="*50)
    
    # Configuration
    n_values = [2**i for i in range(10, 21)]  # 2^10 to 2^20
    alpha_values = [0.1, 1, 5]
    trials = 10
    
    # Run benchmarks
    results = benchmark_greedy_algorithms(
        n_values=n_values,
        alpha_values=alpha_values,
        trials=trials
    )
    
    # Save results
    os.makedirs('results', exist_ok=True)
    with open('results/greedy_results.json', 'w') as f:
        # Convert to serializable format
        serializable = {}
        for alpha in results:
            serializable[str(alpha)] = {}
            for n in results[alpha]:
                serializable[str(alpha)][str(n)] = {}
                for alg in results[alpha][n]:
                    serializable[str(alpha)][str(n)][alg] = {
                        'mean': float(results[alpha][n][alg]['mean']),
                        'std': float(results[alpha][n][alg]['std']),
                        'min': float(results[alpha][n][alg]['min']),
                        'max': float(results[alpha][n][alg]['max'])
                    }
        json.dump(serializable, f, indent=2)
    
    print("Saved greedy results")
    
    # Generate plots
    print("\nGenerating plots...")
    plot_greedy_runtime_loglog(results)
    plot_greedy_normalized_runtime(results)
    print("✓ Greedy plots generated\n")
    
    return results


def run_exhaustive_experiments():
    # Exhaustive search for optimal solutions
    print("\n" + "="*50)
    print("Exhaustive Algorithm")
    print("="*50)
    
    # Configuration (smaller n values!)
    n_values = list(range(5, 26, 5))  # 5, 10, 15, 20, 25 (step=5 per assignment)
    alpha_values = [0.1, 1, 5]
    trials = 10
    
    # Run benchmarks
    results = benchmark_exhaustive_algorithm(
        n_values=n_values,
        alpha_values=alpha_values,
        trials=trials,
        max_n=20
    )
    
    # Save results
    with open('results/exhaustive_results.json', 'w') as f:
        serializable = {}
        for alpha in results:
            serializable[str(alpha)] = {}
            for n in results[alpha]:
                serializable[str(alpha)][str(n)] = {
                    'mean': float(results[alpha][n]['mean']),
                    'std': float(results[alpha][n]['std']),
                    'min': float(results[alpha][n]['min']),
                    'max': float(results[alpha][n]['max'])
                }
        json.dump(serializable, f, indent=2)
    
    print("Saved exhaustive results")
    
    # Generate plots
    plot_exhaustive_runtime(results)
    plot_exhaustive_normalized_runtime(results)
    print("Plots generated\n")
    
    return results


def run_solution_quality_analysis():
    # Compare greedy vs optimal
    print("\n" + "="*50)
    print("Quality Analysis")
    print("="*50)
    
    n_values = list(range(5, 26, 5))  # 5, 10, 15, 20, 25 (step=5 per assignment)
    alpha_values = [0.1, 1, 5]
    trials = 10
    
    generator = IntervalGenerator()
    algorithms = {
        'EFT': earliest_finish_time,
        'EST': earliest_start_time,
        'SD': shortest_duration
    }
    
    quality_results = {}
    
    for alpha in alpha_values:
        print(f"\nAlpha = {alpha}")
        quality_results[alpha] = {}
        
        for n in n_values:
            print(f"  n = {n}...", end=' ', flush=True)
            
            quality_results[alpha][n] = {}
            
            # Run multiple trials
            for trial in range(trials):
                # Generate dataset
                intervals = generator.generate_uniform_dataset(n, alpha, D=100)
                
                # Get optimal solution
                optimal_count, _ = exhaustive_search_optimized(intervals)
                
                # Get greedy solutions
                for alg_name, alg_func in algorithms.items():
                    greedy_count, _ = alg_func(intervals)
                    ratio = greedy_count / optimal_count if optimal_count > 0 else 1.0
                    
                    if alg_name not in quality_results[alpha][n]:
                        quality_results[alpha][n][alg_name] = []
                    quality_results[alpha][n][alg_name].append(ratio)
            
            # Compute mean ratios
            for alg_name in algorithms:
                ratios = quality_results[alpha][n][alg_name]
                quality_results[alpha][n][alg_name] = np.mean(ratios)
            
            print(f"Done (EFT: {quality_results[alpha][n]['EFT']:.3f}, "
                  f"EST: {quality_results[alpha][n]['EST']:.3f}, "
                  f"SD: {quality_results[alpha][n]['SD']:.3f})")
    
    # Save results
    with open('results/quality_results.json', 'w') as f:
        serializable = {}
        for alpha in quality_results:
            serializable[str(alpha)] = {}
            for n in quality_results[alpha]:
                serializable[str(alpha)][str(n)] = {
                    alg: float(quality_results[alpha][n][alg])
                    for alg in quality_results[alpha][n]
                }
        json.dump(serializable, f, indent=2)
    
    print("Saved quality results")
    
    # Generate plots
    plot_solution_quality(quality_results)
    print("Plots generated\n")
    
    return quality_results


def main():
    print("\n" + "="*50)
    print("Interval Scheduling Experiments")
    print("="*50 + "\n")
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    # Run experiments
    try:
        # 1. Greedy algorithms (large inputs)
        greedy_results = run_greedy_experiments()
        
        # 2. Exhaustive algorithm (small inputs)
        exhaustive_results = run_exhaustive_experiments()
        
        # 3. Solution quality comparison
        quality_results = run_solution_quality_analysis()
        
        print("\n" + "="*50)
        print("Done!")
        print("="*50)
        print("\nResults in 'results/' folder")
        print("Check JSON files and PNG plots\n")
        
    except KeyboardInterrupt:
        print("\n\nExperiments interrupted by user.")
    except Exception as e:
        print(f"\n\nError during experiments: {e}")
        raise


if __name__ == "__main__":
    main()
