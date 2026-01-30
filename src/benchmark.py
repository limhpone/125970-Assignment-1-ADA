"""
Benchmarking Framework for Interval Scheduling Algorithms
Provides high-precision timing and statistical analysis.
"""

import time
import numpy as np
from typing import Callable, List, Tuple, Dict
from .dataset_generator import IntervalGenerator
from .greedy_algorithms import earliest_finish_time, earliest_start_time, shortest_duration
from .exhaustive_solver import exhaustive_search_optimized


class Timer:
    """High-resolution timer for benchmarking."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Start the timer."""
        self.start_time = time.perf_counter()
    
    def stop(self):
        """Stop the timer and return elapsed time in seconds."""
        self.end_time = time.perf_counter()
        return self.end_time - self.start_time
    
    def elapsed(self):
        """Get elapsed time in seconds."""
        if self.start_time is None:
            return 0
        if self.end_time is None:
            return time.perf_counter() - self.start_time
        return self.end_time - self.start_time


def benchmark_algorithm(
    algorithm: Callable,
    intervals: List[Tuple[int, int]],
    warmup: bool = True
) -> float:
    """
    Benchmark a single algorithm run with high-precision timing.
    
    Args:
        algorithm: Function that takes intervals and returns (count, selected)
        intervals: List of (start, finish) tuples
        warmup: Whether to perform a warmup run
        
    Returns:
        Execution time in seconds
    """
    # Warmup run (excluded from measurement)
    if warmup:
        _ = algorithm(intervals)
    
    # Actual measurement
    timer = Timer()
    timer.start()
    _ = algorithm(intervals)
    elapsed = timer.stop()
    
    return elapsed


def run_trials(
    algorithm: Callable,
    intervals_list: List[List[Tuple[int, int]]],
    warmup: bool = True
) -> Dict[str, float]:
    """
    Run multiple trials and compute statistics.
    
    Args:
        algorithm: Algorithm function
        intervals_list: List of datasets (one per trial)
        warmup: Whether to perform warmup
        
    Returns:
        Dictionary with mean, std, min, max times
    """
    times = []
    
    for intervals in intervals_list:
        elapsed = benchmark_algorithm(algorithm, intervals, warmup)
        times.append(elapsed)
    
    return {
        'mean': np.mean(times),
        'std': np.std(times),
        'min': np.min(times),
        'max': np.max(times),
        'all_times': times
    }


def benchmark_greedy_algorithms(
    n_values: List[int] = None,
    alpha_values: List[float] = [0.1, 1, 5],
    trials: int = 10,
    D: int = 100
) -> Dict:
    """
    Comprehensive benchmark of all greedy algorithms.
    
    Args:
        n_values: List of input sizes
        alpha_values: List of overlap parameters
        trials: Number of trials per configuration
        D: Maximum duration
        
    Returns:
        Dictionary with all benchmark results
    """
    if n_values is None:
        n_values = [2**i for i in range(10, 21)]  # 2^10 to 2^20
    
    results = {}
    generator = IntervalGenerator()
    
    algorithms = {
        'EFT': earliest_finish_time,
        'EST': earliest_start_time,
        'SD': shortest_duration
    }
    
    print("Running greedy benchmarks...")
    print(f"n values: {n_values}")
    print(f"Trials: {trials}\n")
    
    total = len(alpha_values) * len(n_values)
    count = 0
    
    for alpha in alpha_values:
        print(f"\nAlpha = {alpha}")
        results[alpha] = {}
        
        for n in n_values:
            count += 1
            progress = (count / total) * 100
            print(f"  [{count}/{total}] n = {n} ({progress:.1f}%)...", end=' ', flush=True)
            
            # Generate datasets for all trials
            datasets = [
                generator.generate_uniform_dataset(n, alpha, D)
                for _ in range(trials)
            ]
            
            results[alpha][n] = {}
            
            for alg_name, alg_func in algorithms.items():
                stats = run_trials(alg_func, datasets, warmup=True)
                results[alpha][n][alg_name] = stats
            
            print(f"  n = {n}... done ({results[alpha][n]['EFT']['mean']:.6f}s)")
    
    return results


def benchmark_exhaustive_algorithm(
    n_values: List[int] = None,
    alpha_values: List[float] = [0.1, 1, 5],
    trials: int = 10,
    D: int = 100,
    max_n: int = 20
) -> Dict:
    """
    Benchmark exhaustive algorithm (careful with large n!).
    
    Args:
        n_values: List of input sizes (should be small)
        alpha_values: List of overlap parameters
        trials: Number of trials per configuration
        D: Maximum duration
        max_n: Maximum n to attempt (safety limit)
        
    Returns:
        Dictionary with benchmark results
    """
    if n_values is None:
        n_values = list(range(5, max_n + 1, 5))  # 5, 10, 15, 20
    
    results = {}
    generator = IntervalGenerator()
    
    print("Benchmarking exhaustive algorithm...")
    print(f"Input sizes: {n_values}")
    print(f"Alpha values: {alpha_values}")
    print(f"Trials per configuration: {trials}\n")
    
    total = len(alpha_values) * len(n_values)
    count = 0
    
    for alpha in alpha_values:
        print(f"\nAlpha = {alpha}")
        results[alpha] = {}
        
        for n in n_values:
            count += 1
            progress = (count / total) * 100
            if n > max_n:
                print(f"  [{count}/{total}] n = {n} - Skipped (too large)")
                continue
            
            print(f"  [{count}/{total}] n = {n} ({progress:.1f}%)...", end=' ', flush=True)
            
            # Generate datasets
            datasets = [
                generator.generate_uniform_dataset(n, alpha, D)
                for _ in range(trials)
            ]
            
            # Measure time
            stats = run_trials(exhaustive_search_optimized, datasets, warmup=True)
            results[alpha][n] = stats
            
            print(f"done ({stats['mean']:.6f}s)")
            
            # Stop if taking too long
            if stats['mean'] > 10.0:
                print(f"  Stopping (too slow)")
                break
    
    return results


if __name__ == "__main__":
    # Quick benchmark test
    print("=== Quick Benchmark Test ===\n")
    
    # Test greedy algorithms with small inputs
    greedy_results = benchmark_greedy_algorithms(
        n_values=[1024, 2048, 4096],
        alpha_values=[1],
        trials=3
    )
    
    print("\n" + "="*50)
    print("\n=== Exhaustive Algorithm Test ===\n")
    
    # Test exhaustive algorithm with very small inputs
    exhaustive_results = benchmark_exhaustive_algorithm(
        n_values=[5, 10, 15],
        alpha_values=[1],
        trials=3,
        max_n=15
    )
