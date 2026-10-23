from .base import ReplacementMethod


class GenerationalReplacement(ReplacementMethod):
    def __init__(self, elitism_count=0, minimize=True):
        super().__init__(minimize)
        self.elitism_count = elitism_count

    def replace(self, old_pop, offspring):
        size = len(old_pop)

        if self.elitism_count == 0:
            return offspring[:size]

        elites = [c.copy() for c in
                  self.sort_best_first(old_pop)[:self.elitism_count]]
        best_offspring = self.sort_best_first(offspring)
        return elites + best_offspring[:size - len(elites)]