from abc import ABC, abstractmethod
from typing import Tuple
from ga_toolbox.chromosome.base import Chromosome


class CrossoverMethod(ABC):
    """
    Abstract base class for all crossover operators (e.g. Multi-point, Order Crossover).
    """

    @abstractmethod
    def crossover(
        self, parent1: Chromosome, parent2: Chromosome
    ) -> Tuple[Chromosome, Chromosome]:
        """
        Recombine two parent chromosomes to produce two offspring.

        Args:
            parent1: First parent Chromosome.
            parent2: Second parent Chromosome.

        Returns:
            Tuple of two newly created offspring Chromosomes.
        """
        pass
