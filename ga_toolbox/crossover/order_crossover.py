import random
from typing import Tuple, Union, Sequence
from ga_toolbox.chromosome.base import Chromosome
from ga_toolbox.crossover.base import CrossoverMethod


class OrderCrossover(CrossoverMethod):
    """
    Order Crossover (OX) for Permutation Chromosomes (e.g. CVRP, TSP).
    Preserves relative order without creating duplicate visits.
    """

    def crossover(
        self, parent1: Union[Chromosome, Sequence[int]], parent2: Union[Chromosome, Sequence[int]],
        rng: random.Random = None
    ) -> Tuple[Union[Chromosome, list], Union[Chromosome, list]]:
        is_chrom = isinstance(parent1, Chromosome) and isinstance(parent2, Chromosome)
        genes_a = parent1.genes if is_chrom else list(parent1)
        genes_b = parent2.genes if is_chrom else list(parent2)

        if len(genes_a) != len(genes_b):
            raise ValueError("Parents must have equal length")
        if len(set(genes_a)) != len(genes_a) or len(set(genes_b)) != len(genes_b):
            raise ValueError("Parents must not contain duplicate items")
        if set(genes_a) != set(genes_b):
            raise ValueError("Parents must contain the same items")

        generator = rng if rng is not None else random.Random()
        n = len(genes_a)
        if n < 2:
            c1_genes, c2_genes = list(genes_a), list(genes_b)
        else:
            left, right = sorted(generator.sample(range(n), 2))

            def make_child(segment_parent, fill_parent):
                child = [None] * n
                child[left : right + 1] = segment_parent[left : right + 1]
                used = set(child[left : right + 1])
                scan = list(fill_parent[right + 1 :]) + list(fill_parent[: right + 1])
                fill = [item for item in scan if item not in used]
                positions = list(range(right + 1, n)) + list(range(0, left))
                for position, item in zip(positions, fill):
                    child[position] = item
                return child

            c1_genes = make_child(genes_a, genes_b)
            c2_genes = make_child(genes_b, genes_a)

        if is_chrom:
            child1 = parent1.copy()
            child2 = parent2.copy()
            child1.genes = c1_genes
            child2.genes = c2_genes
            return child1, child2
        return c1_genes, c2_genes
