import random
from typing import TypeVar
T = TypeVar("T")

class InversionMutation:
    """Reverse a randomly selected segment."""
    def mutate(self, chromosome: list[T], rng: random.Random | None = None) -> list[T]:
        result = chromosome.copy()
        if len(result) < 2: return result
        generator = rng if rng is not None else random.Random()
        left, right = sorted(generator.sample(range(len(result)), 2))
        result[left:right + 1] = reversed(result[left:right + 1])
        return result
