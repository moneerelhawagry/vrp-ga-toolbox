import random
from typing import Optional, List
from ga_toolbox.chromosome.base import Chromosome


class IntegerChromosome(Chromosome):
    """
    Chromosome representation with integer-valued genes.

    Modes:
        1. Range-bounded mode (permutation=False): Each gene is an integer in [lower_bound, upper_bound].
        2. Permutation mode (permutation=True): Genes form a unique permutation of numbers 1..length.
           Essential for routing problems (CVRP, TSP) where customers cannot be visited multiple times.
    """

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
        """Randomize the genes according to the chosen mode."""
        if self.permutation:
            self.genes = list(range(1, self.length + 1))
            random.shuffle(self.genes)
        else:
            self.genes = [
                random.randint(self.lower_bound, self.upper_bound)
                for _ in range(self.length)
            ]
