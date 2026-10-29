import random
from typing import Union, TypeVar
from ga_toolbox.chromosome.base import Chromosome
from ga_toolbox.mutation.base import MutationMethod

T = TypeVar("T")


class ScrambleMutation(MutationMethod):
    """Shuffle genes inside a randomly selected segment."""

    def mutate(
        self, chromosome: Union[Chromosome, list], mutation_rate: float = 1.0, rng: random.Random = None
    ) -> Union[Chromosome, list]:
        is_chrom = isinstance(chromosome, Chromosome)
        genes = chromosome.genes if is_chrom else chromosome

        if len(genes) >= 2 and random.random() < mutation_rate:
            generator = rng if rng is not None else random.Random()
            left, right = sorted(generator.sample(range(len(genes)), 2))
            segment = genes[left : right + 1]
            generator.shuffle(segment)
            genes[left : right + 1] = segment

        return chromosome
