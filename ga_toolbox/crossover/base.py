from abc import ABC, abstractmethod
from typing import Tuple, Union, Sequence
from ga_toolbox.chromosome.base import Chromosome


class CrossoverMethod(ABC):
    """Abstract base class for all crossover operators."""

    @abstractmethod
    def crossover(
        self, parent1: Union[Chromosome, Sequence], parent2: Union[Chromosome, Sequence]
    ) -> Tuple[Union[Chromosome, list], Union[Chromosome, list]]:
        """Recombine two parents to produce two offspring."""
        pass
