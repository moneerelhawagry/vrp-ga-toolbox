from abc import ABC, abstractmethod


class ReplacementMethod(ABC):
    def __init__(self, minimize=True):
        self.minimize = minimize

    def sort_best_first(self, population):
        return sorted(population, key=lambda c: c.fitness,
                      reverse=not self.minimize)

    @abstractmethod
    def replace(self, old_pop, offspring):
        pass