from abc import ABC, abstractmethod
from typing import List
from ga_toolbox.chromosome.base import Chromosome


class ReplacementMethod(ABC):
    """Base class for population replacement strategies."""

    def __init__(self, minimize: bool = True):
        self.minimize = minimize

    def sort_best_first(self, population: List[Chromosome]) -> List[Chromosome]:
        return sorted(population, key=lambda c: c.fitness, reverse=not self.minimize)

    @abstractmethod
    def replace(
        self, old_pop: List[Chromosome], offspring: List[Chromosome], pop_size: int = None
    ) -> List[Chromosome]:
        """Return the new population."""
        pass
