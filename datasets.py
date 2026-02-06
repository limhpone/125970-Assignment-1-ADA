import numpy as np

def generate_uniform_intervals(n: int, D: int, alpha: float, rng: np.random.Generator):
    """
    Uniform Random Dataset (assignment spec):
      T = alpha * n * D
      s_i ~ Uniform[0, T)
      d_i ~ Uniform[1, D]  (integers by default; can be floats if you want)
      f_i = s_i + d_i

    Returns:
      intervals: np.ndarray shape (n, 2) with columns [start, finish] as floats
      meta: dict with (n, D, alpha, T)
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if D <= 0:
        raise ValueError("D must be positive")
    if alpha <= 0:
        raise ValueError("alpha must be positive")

    T = float(alpha * n * D)
    starts = rng.uniform(0.0, T, size=n)
    durations = rng.integers(1, D + 1, size=n)  # inclusive upper bound
    finishes = starts + durations.astype(float)

    intervals = np.column_stack([starts, finishes]).astype(float)
    return intervals, {"n": n, "D": D, "alpha": float(alpha), "T": T}
