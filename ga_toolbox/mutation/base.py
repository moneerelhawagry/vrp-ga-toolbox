from abc import ABC, abstractmethod
from ga_toolbox.chromosome.base import Chromosome


class MutationMethod(ABC):
    """
    Abstract base class for all mutation operators (e.g. Swap, Inversion, Scramble).
    """

    @abstractmethod
    def mutate(self, chromosome: Chromosome, mutation_rate: float) -> Chromosome:
        """
        Mutate the given chromosome according to the specified mutation probability.

        Args:
            chromosome: Chromosome instance to mutate.
            mutation_rate: Probability of mutation (gene-level or chromosome-level).

        Returns:
            The mutated Chromosome.
        """
        pass
