# Greedy algorithms for interval scheduling
# EFT, EST, and SD implementations

from typing import List, Tuple, Set


def earliest_finish_time(intervals: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]]]:
    # Sort by finish time and greedily select compatible intervals
    if not intervals:
        return 0, []
    
    # Sort by finish time
    sorted_intervals = sorted(intervals, key=lambda x: x[1])
    
    selected = [sorted_intervals[0]]
    last_finish = sorted_intervals[0][1]
    
    # Scan through sorted intervals (O(n))
    for start, finish in sorted_intervals[1:]:
        if start >= last_finish:  # Compatible
            selected.append((start, finish))
            last_finish = finish
    
    return len(selected), selected


def earliest_start_time(intervals: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]]]:
    # Sort by start time
    if not intervals:
        return 0, []
    
    # Sort by start time (O(n log n))
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    selected = [sorted_intervals[0]]
    last_finish = sorted_intervals[0][1]
    
    # Scan through sorted intervals (O(n))
    for start, finish in sorted_intervals[1:]:
        if start >= last_finish:  # Compatible
            selected.append((start, finish))
            last_finish = finish
    
    return len(selected), selected


def shortest_duration(intervals: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]]]:
    # Sort by duration (shortest first)
    if not intervals:
        return 0, []
    
    # Sort by duration (finish - start) (O(n log n))
    sorted_intervals = sorted(intervals, key=lambda x: x[1] - x[0])
    
    selected = [sorted_intervals[0]]
    selected_set = {sorted_intervals[0]}
    
    # Scan through sorted intervals (O(n))
    for start, finish in sorted_intervals[1:]:
        # Check compatibility with all selected intervals
        compatible = True
        for s_start, s_finish in selected:
            if not (finish <= s_start or s_finish <= start):
                compatible = False
                break
        
        if compatible:
            selected.append((start, finish))
            selected_set.add((start, finish))
    
    return len(selected), selected


def run_all_greedy_algorithms(intervals: List[Tuple[int, int]]) -> dict:
    """
    Run all three greedy algorithms on the same dataset.
    
    Args:
        intervals: List of (start, finish) tuples
        
    Returns:
        Dictionary with results from each algorithm
    """
    results = {
        'EFT': earliest_finish_time(intervals),
        'EST': earliest_start_time(intervals),
        'SD': shortest_duration(intervals)
    }
    
    return results


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
    print("\nRunning all greedy algorithms:\n")
    
    results = run_all_greedy_algorithms(test_intervals)
    
    for name, (count, selected) in results.items():
        print(f"{name}:")
        print(f"  Count: {count}")
        print(f"  Selected: {selected}")
        print()
