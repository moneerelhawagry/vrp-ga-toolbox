from typing import List
from ga_toolbox.chromosome.base import Chromosome
from ga_toolbox.replacement.base import ReplacementMethod


class GenerationalReplacement(ReplacementMethod):
    """Generational replacement: offspring completely replace the old population."""

    def replace(
        self, old_pop: List[Chromosome], offspring: List[Chromosome], pop_size: int = None
    ) -> List[Chromosome]:
        target_size = pop_size if pop_size is not None else len(old_pop)
        if len(offspring) >= target_size:
            return [ind.copy() for ind in offspring[:target_size]]
        needed = target_size - len(offspring)
        sorted_old = self.sort_best_first(old_pop)
        return [ind.copy() for ind in offspring] + [ind.copy() for ind in sorted_old[:needed]]
