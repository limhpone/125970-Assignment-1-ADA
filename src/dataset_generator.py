# Dataset generator for interval scheduling
# Creates random intervals with different overlap levels

import numpy as np
from typing import List, Tuple


class IntervalGenerator:
    # Generate datasets for testing
    
    def __init__(self, seed: int = None):
        """
        Initialize the generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        if seed is not None:
            np.random.seed(seed)
    
    def generate_uniform_dataset(
        self, 
        n: int, 
        alpha: float, 
        D: int = 100
    ) -> List[Tuple[int, int]]:
        """
        Generate a uniform random dataset of intervals.
        
        Formula:
            T = α · n · D
            s_i ~ Uniform[0, T]
            d_i ~ Uniform[1, D]
            f_i = s_i + d_i
        
        Args:
            n: Number of intervals
            alpha: Overlap control parameter (0.1=high, 1=medium, 5=low overlap)
            D: Maximum duration
            
        Returns:
            List of (start, finish) tuples
        """
        T = alpha * n * D
        
        # Generate start times uniformly in [0, T]
        start_times = np.random.uniform(0, T, n)
        
        # Generate durations uniformly in [1, D]
        durations = np.random.uniform(1, D, n)
        
        # Calculate finish times
        finish_times = start_times + durations
        
        # Create intervals as list of tuples
        intervals = [(int(s), int(f)) for s, f in zip(start_times, finish_times)]
        
        return intervals
    
    def get_overlap_statistics(self, intervals: List[Tuple[int, int]]) -> dict:
        """
        Calculate overlap statistics for a dataset.
        
        Args:
            intervals: List of (start, finish) tuples
            
        Returns:
            Dictionary with overlap statistics
        """
        n = len(intervals)
        overlap_count = 0
        
        for i in range(n):
            for j in range(i + 1, n):
                s1, f1 = intervals[i]
                s2, f2 = intervals[j]
                # Check if intervals overlap
                if not (f1 <= s2 or f2 <= s1):
                    overlap_count += 1
        
        max_possible_overlaps = n * (n - 1) // 2
        overlap_density = overlap_count / max_possible_overlaps if max_possible_overlaps > 0 else 0
        
        return {
            'total_intervals': n,
            'overlapping_pairs': overlap_count,
            'overlap_density': overlap_density
        }


def generate_all_datasets(
    alpha_values: List[float] = [0.1, 1, 5],
    n_values: List[int] = None,
    D: int = 100,
    trials: int = 10
) -> dict:
    """
    Generate multiple datasets for all experimental configurations.
    
    Args:
        alpha_values: List of overlap parameters
        n_values: List of interval counts
        D: Maximum duration
        trials: Number of trials per configuration
        
    Returns:
        Dictionary mapping (alpha, n, trial) to dataset
    """
    if n_values is None:
        n_values = [2**i for i in range(10, 21)]  # 2^10 to 2^20
    
    datasets = {}
    generator = IntervalGenerator()
    
    for alpha in alpha_values:
        for n in n_values:
            for trial in range(trials):
                intervals = generator.generate_uniform_dataset(n, alpha, D)
                datasets[(alpha, n, trial)] = intervals
    
    return datasets


if __name__ == "__main__":
    # Example usage
    generator = IntervalGenerator(seed=42)
    
    # Generate sample datasets
    print("Generating sample datasets...\n")
    
    for alpha in [0.1, 1, 5]:
        intervals = generator.generate_uniform_dataset(n=100, alpha=alpha, D=100)
        stats = generator.get_overlap_statistics(intervals)
        
        print(f"Alpha = {alpha} ({['High', 'Medium', 'Low'][[0.1, 1, 5].index(alpha)]} overlap):")
        print(f"  Intervals: {stats['total_intervals']}")
        print(f"  Overlapping pairs: {stats['overlapping_pairs']}")
        print(f"  Overlap density: {stats['overlap_density']:.4f}")
        print()
