import random
from typing import Optional, List
from ga_toolbox.chromosome.base import Chromosome


class IntegerChromosome(Chromosome):
    def __init__(
        self,
        length: int,
        lower_bound: int = 0,
        upper_bound: int = 10,
        permutation: bool = False,
        genes: Optional[List[int]] = None,
    ):
        super().__init__(genes)
        self.length = length
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.permutation = permutation

        if not self.genes:
            if self.permutation:
                self.genes = list(range(1, self.length + 1))
            else:
                self.genes = [self.lower_bound] * self.length

    def randomize(self) -> None:
        if self.permutation:
            self.genes = list(range(1, self.length + 1))
            random.shuffle(self.genes)
        else:
            self.genes = [
                random.randint(self.lower_bound, self.upper_bound)
                for _ in range(self.length)
            ]
