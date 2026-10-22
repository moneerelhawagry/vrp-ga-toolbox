from abc import ABC, abstractmethod
from typing import List
from ga_toolbox.chromosome.base import Chromosome


class ReplacementMethod(ABC):
    """
    Abstract base class for population replacement strategies (e.g. Generational, Elitist).
    """

    @abstractmethod
    def replace(
        self,
        old_population: List[Chromosome],
        offspring: List[Chromosome],
        pop_size: int,
    ) -> List[Chromosome]:
        """
        Form the next generation population from the old population and new offspring.

        Args:
            old_population: The evaluated current population.
            offspring: The newly produced offspring.
            pop_size: The required target population size.

        Returns:
            The newly formed population of length pop_size.
        """
        pass
