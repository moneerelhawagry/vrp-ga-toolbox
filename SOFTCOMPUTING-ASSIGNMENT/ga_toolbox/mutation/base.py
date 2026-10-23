from abc import ABC, abstractmethod
from ga_toolbox.chromosome.base import Chromosome


class MutationMethod(ABC):

    @abstractmethod
    def mutate(self, chromosome: Chromosome, mutation_rate: float) -> Chromosome:
        pass
