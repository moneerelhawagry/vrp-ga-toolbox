import random
from typing import Optional, List
from ga_toolbox.chromosome.base import Chromosome


class BinaryChromosome(Chromosome):
    """
    Chromosome representation where each gene is a binary bit (0 or 1).

    Useful for classic genetic algorithm benchmarks, knapsack problems,
    and binary-encoded parameter optimization.
    """

    def __init__(self, length: int, genes: Optional[List[int]] = None):
        super().__init__(genes)
        self.length = length
        if not self.genes:
            self.genes = [0] * self.length

    def randomize(self) -> None:
        """Randomize all genes to 0 or 1 uniformly."""
        self.genes = [random.randint(0, 1) for _ in range(self.length)]

    def decode_to_int(self) -> int:
        """Decode the binary chromosome to an unsigned base-10 integer."""
        return int("".join(str(g) for g in self.genes), 2)

    def decode_to_float(self, lower: float, upper: float) -> float:
        """
        Linearly map the binary bitstring to a floating-point value in [lower, upper].
        """
        max_int = (2 ** self.length) - 1
        if max_int == 0:
            return lower
        return lower + (upper - lower) * (self.decode_to_int() / max_int)
