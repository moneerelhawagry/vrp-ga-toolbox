import random
from typing import Optional, List
from ga_toolbox.chromosome.base import Chromosome


class FloatChromosome(Chromosome):

    def __init__(
        self,
        length: int,
        lower_bound: float = 0.0,
        upper_bound: float = 1.0,
        genes: Optional[List[float]] = None,
    ):
        super().__init__(genes)
        self.length = length
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        if not self.genes:
            self.genes = [self.lower_bound] * self.length

    def randomize(self) -> None:
        self.genes = [
            random.uniform(self.lower_bound, self.upper_bound)
            for _ in range(self.length)
        ]
