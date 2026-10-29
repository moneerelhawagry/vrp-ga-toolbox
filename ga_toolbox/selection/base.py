from abc import ABC, abstractmethod
from typing import List
from ga_toolbox.chromosome.base import Chromosome


class SelectionMethod(ABC):
    """Base class for all selection methods."""

    def __init__(self, minimize: bool = True):
        self.minimize = minimize

    def is_better(self, a: float, b: float) -> bool:
        """Return True if fitness a is better than fitness b."""
        if self.minimize:
            return a < b
        return a > b

    @abstractmethod
    def select_one(self, population: List[Chromosome]) -> Chromosome:
        """Select a single chromosome from the population."""
        pass

    def select(self, population: List[Chromosome], count: int = 1) -> List[Chromosome]:
        """Select `count` individuals from the population."""
        return [self.select_one(population).copy() for _ in range(count)]
