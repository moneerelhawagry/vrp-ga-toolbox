import random
from typing import TypeVar
T = TypeVar("T")

class ScrambleMutation:
    """Shuffle genes inside a randomly selected segment."""
    def mutate(self, chromosome: list[T], rng: random.Random | None = None) -> list[T]:
        result = chromosome.copy()
        if len(result) < 2: return result
        generator = rng if rng is not None else random.Random()
        left, right = sorted(generator.sample(range(len(result)), 2))
        segment = result[left:right + 1]
        generator.shuffle(segment)
        result[left:right + 1] = segment
        return result
