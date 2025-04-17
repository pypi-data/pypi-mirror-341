import numpy as np


def safe_normalize(fractions: np.ndarray) -> np.ndarray:
  """Normalize fractions to sum to 1.0, with a small epsilon for numerical stability."""
  if np.sum(fractions) == 0.0:
    return np.ones_like(fractions)
  return fractions / np.sum(fractions)