from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple
import numpy as np

@dataclass(frozen=True)
class ExhaustiveResult:
    count: int
    selected: Optional[np.ndarray] = None  # shape (k,2)

def _compat_matrix(intervals: np.ndarray) -> np.ndarray:
    """compat[i,j]=True if intervals i and j do NOT overlap (pairwise compatible)."""
    s = intervals[:, 0]
    f = intervals[:, 1]
    # Two intervals i,j are compatible if f_i <= s_j OR f_j <= s_i
    # Build vectorized matrix:
    fi_le_sj = f[:, None] <= s[None, :]
    fj_le_si = f[None, :] <= s[:, None]
    compat = fi_le_sj | fj_le_si
    np.fill_diagonal(compat, True)
    return compat

def _subset_is_feasible(idx: np.ndarray, compat: np.ndarray) -> bool:
    # Check all pairs in subset are compatible
    # For small n this is fine; idx size = k
    k = idx.size
    for a in range(k):
        i = idx[a]
        # Check compatibility of i with all later elements
        if not np.all(compat[i, idx[a:]]):
            return False
    return True

def exhaustive_optimal(intervals: np.ndarray, return_selected: bool=True) -> ExhaustiveResult:
    """
    Exhaustive optimal solver by enumerating all subsets and keeping the largest feasible.
    Intended only for small n (exponential time).
    Worst-case time ~ O(n 2^n) (subset enumeration + feasibility checks).
    """
    n = intervals.shape[0]
    if n > 26:
        # Guardrail: still allow, but warn via exception message.
        raise ValueError(f"n={n} is likely too large for exhaustive subset enumeration. Use smaller n.")

    compat = _compat_matrix(intervals)
    best_mask = 0
    best_size = 0

    # Enumerate all subset masks from 1..(2^n - 1)
    # (mask=0 gives empty set, size=0)
    for mask in range(1, 1 << n):
        # quick upper bound: if number of bits <= best_size, skip
        bits = mask.bit_count()
        if bits <= best_size:
            continue
        # Extract indices
        idx = np.fromiter((i for i in range(n) if (mask >> i) & 1), dtype=int, count=bits)
        if _subset_is_feasible(idx, compat):
            best_size = bits
            best_mask = mask

    if return_selected:
        if best_size == 0:
            return ExhaustiveResult(count=0, selected=np.empty((0,2), dtype=float))
        idx = np.array([i for i in range(n) if (best_mask >> i) & 1], dtype=int)
        return ExhaustiveResult(count=best_size, selected=intervals[idx])
    return ExhaustiveResult(count=best_size, selected=None)
