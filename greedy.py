from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, List, Tuple, Optional
import numpy as np

@dataclass(frozen=True)
class GreedyResult:
    count: int
    selected: Optional[np.ndarray] = None  # shape (k,2) if requested

def _select_compatible(sorted_intervals: np.ndarray, return_selected: bool) -> GreedyResult:
    # Compatibility rule used in interval scheduling:
    # pick (s,f) if s >= last_finish
    selected = []
    last_finish = -np.inf
    for s, f in sorted_intervals:
        if s >= last_finish:
            selected.append((s, f))
            last_finish = f
    if return_selected:
        return GreedyResult(count=len(selected), selected=np.array(selected, dtype=float))
    return GreedyResult(count=len(selected), selected=None)

def greedy_earliest_finish(intervals: np.ndarray, return_selected: bool=False) -> GreedyResult:
    """EFT: sort by increasing finish time f_i."""
    order = np.argsort(intervals[:, 1], kind="mergesort")
    return _select_compatible(intervals[order], return_selected)

def greedy_earliest_start(intervals: np.ndarray, return_selected: bool=False) -> GreedyResult:
    """EST: sort by increasing start time s_i."""
    order = np.argsort(intervals[:, 0], kind="mergesort")
    return _select_compatible(intervals[order], return_selected)

def greedy_shortest_duration(intervals: np.ndarray, return_selected: bool=False) -> GreedyResult:
    """SD: sort by increasing duration (f_i - s_i)."""
    durations = intervals[:, 1] - intervals[:, 0]
    order = np.argsort(durations, kind="mergesort")
    return _select_compatible(intervals[order], return_selected)
