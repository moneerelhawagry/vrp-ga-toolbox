from .base import ReplacementMethod


class ElitistReplacement(ReplacementMethod):
    def __init__(self, elitism_count=2, minimize=True):
        super().__init__(minimize)
        self.elitism_count = elitism_count

    def replace(self, old_pop, offspring):
        size = len(old_pop)

    
        elites = [c.copy() for c in
                  self.sort_best_first(old_pop)[:self.elitism_count]]

    
        best_offspring = self.sort_best_first(offspring)
        new_pop = elites + best_offspring[:size - len(elites)]

        if len(new_pop) < size:
            extra = self.sort_best_first(old_pop)[len(elites):]
            new_pop += extra[:size - len(new_pop)]
        return new_pop