import random
from typing import Tuple, Union, Sequence, TypeVar
from ga_toolbox.chromosome.base import Chromosome
from ga_toolbox.crossover.base import CrossoverMethod

T = TypeVar("T")


class MultiPointCrossover(CrossoverMethod):
    """N-point crossover for binary or real sequences."""

    def __init__(self, points: int = 2):
        if points < 1:
            raise ValueError("points must be at least 1")
        self.points = points

    def crossover(
        self, parent1: Union[Chromosome, Sequence[T]], parent2: Union[Chromosome, Sequence[T]],
        rng: random.Random = None
    ) -> Tuple[Union[Chromosome, list], Union[Chromosome, list]]:
        is_chrom = isinstance(parent1, Chromosome) and isinstance(parent2, Chromosome)
        genes_a = parent1.genes if is_chrom else list(parent1)
        genes_b = parent2.genes if is_chrom else list(parent2)

        if len(genes_a) != len(genes_b):
            raise ValueError("Parents must have equal length")

        generator = rng if rng is not None else random.Random()
        n = len(genes_a)
        if n < 2:
            child_a_genes, child_b_genes = list(genes_a), list(genes_b)
        else:
            cuts = sorted(generator.sample(range(1, n), min(self.points, n - 1)))
            bounds = [0] + cuts + [n]
            child_a_genes, child_b_genes = [], []
            for segment in range(len(bounds) - 1):
                start, end = bounds[segment], bounds[segment + 1]
                if segment % 2 == 0:
                    child_a_genes.extend(genes_a[start:end])
                    child_b_genes.extend(genes_b[start:end])
                else:
                    child_a_genes.extend(genes_b[start:end])
                    child_b_genes.extend(genes_a[start:end])

        if is_chrom:
            c1 = parent1.copy()
            c2 = parent2.copy()
            c1.genes = child_a_genes
            c2.genes = child_b_genes
            return c1, c2
        return child_a_genes, child_b_genes
