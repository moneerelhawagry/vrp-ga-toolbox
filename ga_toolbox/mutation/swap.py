import random
from typing import Union, TypeVar
from ga_toolbox.chromosome.base import Chromosome
from ga_toolbox.mutation.base import MutationMethod

T = TypeVar("T")


class SwapMutation(MutationMethod):
    """Swap two randomly chosen genes."""

    def mutate(
        self, chromosome: Union[Chromosome, list], mutation_rate: float = 1.0, rng: random.Random = None
    ) -> Union[Chromosome, list]:
        is_chrom = isinstance(chromosome, Chromosome)
        genes = chromosome.genes if is_chrom else chromosome

        if len(genes) >= 2 and random.random() < mutation_rate:
            generator = rng if rng is not None else random.Random()
            i, j = generator.sample(range(len(genes)), 2)
            genes[i], genes[j] = genes[j], genes[i]

        return chromosome
