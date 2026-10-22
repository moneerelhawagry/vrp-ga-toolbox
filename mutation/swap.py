import random
from typing import TypeVar
T = TypeVar("T")

class SwapMutation:
    """Swap two randomly chosen genes."""
    def mutate(self, chromosome: list[T], rng: random.Random | None = None) -> list[T]:
        result = chromosome.copy()
        if len(result) < 2: return result
        generator = rng if rng is not None else random.Random()
        i, j = generator.sample(range(len(result)), 2)
        result[i], result[j] = result[j], result[i]
        return result
