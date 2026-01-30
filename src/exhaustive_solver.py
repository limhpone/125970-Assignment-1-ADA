# Exhaustive search to find optimal solution
# Warning: Very slow for large n!

from typing import List, Tuple
from itertools import combinations


def is_compatible_set(intervals: List[Tuple[int, int]]) -> bool:
    """
    Check if a set of intervals are mutually compatible (non-overlapping).
    
    Args:
        intervals: List of (start, finish) tuples
        
    Returns:
        True if all intervals are pairwise compatible
    """
    n = len(intervals)
    
    for i in range(n):
        for j in range(i + 1, n):
            s1, f1 = intervals[i]
            s2, f2 = intervals[j]
            
            # Intervals overlap if NOT (f1 <= s2 or f2 <= s1)
            if not (f1 <= s2 or f2 <= s1):
                return False
    
    return True


def exhaustive_search(intervals: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Exhaustive search algorithm using subset enumeration.
    Finds the maximum-size compatible subset.
    
    Algorithm:
    1. Enumerate all 2^n subsets
    2. Check each subset for compatibility
    3. Keep track of the largest compatible subset
    
    Args:
        intervals: List of (start, finish) tuples
        
    Returns:
        Tuple of (count, selected_intervals)
    """
    if not intervals:
        return 0, []
    
    n = len(intervals)
    max_count = 0
    best_subset = []
    
    # Try all possible subset sizes from largest to smallest
    # This allows early termination once we find a feasible solution
    for size in range(n, 0, -1):
        if size <= max_count:
            # Already found a larger solution
            break
        
        # Generate all subsets of this size
        for subset_indices in combinations(range(n), size):
            subset = [intervals[i] for i in subset_indices]
            
            if is_compatible_set(subset):
                if len(subset) > max_count:
                    max_count = len(subset)
                    best_subset = subset
                    # For this size, we found a solution, move to next size
                    break
    
    return max_count, best_subset


def exhaustive_search_optimized(intervals: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Optimized exhaustive search with compatibility precomputation.
    
    Optimization:
    - Precompute compatibility matrix
    - Still O(n·2^n) worst case, but faster in practice
    
    Args:
        intervals: List of (start, finish) tuples
        
    Returns:
        Tuple of (count, selected_intervals)
    """
    if not intervals:
        return 0, []
    
    n = len(intervals)
    
    # Precompute compatibility matrix (O(n^2))
    compatible = [[True] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            s1, f1 = intervals[i]
            s2, f2 = intervals[j]
            if not (f1 <= s2 or f2 <= s1):
                compatible[i][j] = False
                compatible[j][i] = False
    
    max_count = 0
    best_subset = []
    
    # Try all possible subset sizes from largest to smallest
    for size in range(n, 0, -1):
        if size <= max_count:
            break
        
        for subset_indices in combinations(range(n), size):
            # Check compatibility using precomputed matrix
            is_valid = True
            for i in range(len(subset_indices)):
                for j in range(i + 1, len(subset_indices)):
                    if not compatible[subset_indices[i]][subset_indices[j]]:
                        is_valid = False
                        break
                if not is_valid:
                    break
            
            if is_valid:
                subset = [intervals[idx] for idx in subset_indices]
                if len(subset) > max_count:
                    max_count = len(subset)
                    best_subset = subset
                    break
    
    return max_count, best_subset


if __name__ == "__main__":
    # Example usage
    test_intervals = [
        (1, 4),
        (3, 5),
        (0, 6),
        (5, 7),
        (3, 9),
        (5, 9),
        (6, 10),
        (8, 11),
        (8, 12),
        (2, 14),
        (12, 16)
    ]
    
    print("Test Intervals:", test_intervals)
    print(f"Number of intervals: {len(test_intervals)}")
    print("\nRunning exhaustive search...\n")
    
    count, selected = exhaustive_search(test_intervals)
    
    print(f"Optimal count: {count}")
    print(f"Optimal solution: {selected}")
    
    # Compare with optimized version
    count_opt, selected_opt = exhaustive_search_optimized(test_intervals)
    print(f"\nOptimized optimal count: {count_opt}")
    print(f"Match: {count == count_opt}")
