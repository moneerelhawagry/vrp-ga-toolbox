import random
from .base import SelectionMethod


class RouletteWheelSelection(SelectionMethod):
    def select_one(self, population):
        fitnesses = [c.fitness for c in population]

        
        if self.minimize:
            worst = max(fitnesses)
            weights = [worst - f + 1 for f in fitnesses]
        else:
            lowest = min(fitnesses)
            weights = [f - lowest + 1 for f in fitnesses]

        total = sum(weights)
        spin = random.uniform(0, total)
        running = 0
        for chrom, w in zip(population, weights):
            running += w
            if running >= spin:
                return chrom
        return population[-1] 