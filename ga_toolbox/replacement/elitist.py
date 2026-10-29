from typing import List
from ga_toolbox.chromosome.base import Chromosome
from ga_toolbox.replacement.base import ReplacementMethod


class ElitistReplacement(ReplacementMethod):
    """Elitist replacement: selects the best individuals from old population + offspring."""

    def replace(
        self, old_pop: List[Chromosome], offspring: List[Chromosome], pop_size: int = None
    ) -> List[Chromosome]:
        target_size = pop_size if pop_size is not None else len(old_pop)
        combined = old_pop + offspring
        sorted_combined = self.sort_best_first(combined)
        return [ind.copy() for ind in sorted_combined[:target_size]]
