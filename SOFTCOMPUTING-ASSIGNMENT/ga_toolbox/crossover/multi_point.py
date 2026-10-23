import random
from typing import Sequence, TypeVar
T = TypeVar("T")

class MultiPointCrossover:
    def __init__(self, points: int = 2):
        if points < 1:
            raise ValueError("points must be at least 1")
        self.points = points

    def crossover(self, parent_a: Sequence[T], parent_b: Sequence[T],
                  rng: random.Random | None = None) -> tuple[list[T], list[T]]:
        if len(parent_a) != len(parent_b):
            raise ValueError("Parents must have equal length")
        generator = rng if rng is not None else random.Random()
        n = len(parent_a)
        if n < 2:
            return list(parent_a), list(parent_b)
        cuts = sorted(generator.sample(range(1, n), min(self.points, n - 1)))
        bounds = [0] + cuts + [n]
        child_a, child_b = [], []
        for segment in range(len(bounds) - 1):
            start, end = bounds[segment], bounds[segment + 1]
            if segment % 2 == 0:
                child_a.extend(parent_a[start:end])
                child_b.extend(parent_b[start:end])
            else:
                child_a.extend(parent_b[start:end])
                child_b.extend(parent_a[start:end])
        return child_a, child_b
