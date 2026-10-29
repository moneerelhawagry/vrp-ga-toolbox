from abc import ABC, abstractmethod
from typing import Union
from ga_toolbox.chromosome.base import Chromosome


class MutationMethod(ABC):
    """Abstract base class for all mutation operators."""

    @abstractmethod
    def mutate(self, chromosome: Union[Chromosome, list], mutation_rate: float = 1.0) -> Union[Chromosome, list]:
        """Apply mutation to the chromosome."""
        pass
