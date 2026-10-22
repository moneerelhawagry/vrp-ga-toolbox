from abc import ABC, abstractmethod
from typing import List
from ga_toolbox.chromosome.base import Chromosome


class SelectionMethod(ABC):
    """
    Abstract base class for all selection strategies (e.g. Tournament, Roulette Wheel).
    """

    @abstractmethod
    def select(self, population: List[Chromosome], count: int) -> List[Chromosome]:
        """
        Select `count` individuals from the given population based on their fitness.

        Args:
            population: List of evaluated Chromosomes (with chromosome.fitness set).
            count: Number of individuals to select for mating.

        Returns:
            List of selected Chromosomes.
        """
        pass
