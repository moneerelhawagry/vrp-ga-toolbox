from abc import ABC, abstractmethod
from typing import Tuple
from ga_toolbox.chromosome.base import Chromosome


class CrossoverMethod(ABC):
    @abstractmethod
    def crossover(
        self, parent1: Chromosome, parent2: Chromosome
    ) -> Tuple[Chromosome, Chromosome]:
        pass
