from abc import ABC, abstractmethod


class ReplacementMethod(ABC):
    def __init__(self, minimize=True):
        self.minimize = minimize

    def sort_best_first(self, population):
        # returns a new sorted list, best individual first
        return sorted(population, key=lambda c: c.fitness,
                      reverse=not self.minimize)

    @abstractmethod
    def replace(self, old_pop, offspring):
        """Return the new population (same size as old_pop)."""
        pass