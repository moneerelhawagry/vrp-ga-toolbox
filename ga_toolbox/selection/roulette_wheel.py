import random
from typing import List
from ga_toolbox.chromosome.base import Chromosome
from ga_toolbox.selection.base import SelectionMethod


class RouletteWheelSelection(SelectionMethod):
    """
    Roulette Wheel (Fitness Proportionate) Selection Operator:
    Probability of selection is proportional to an individual's scaled fitness.
    For minimization, fitness is inverted so lower costs receive higher selection chances.
    """

    def __init__(self, minimize: bool = True):
        super().__init__(minimize=minimize)

    def select_one(self, population: List[Chromosome]) -> Chromosome:
        if not population:
            raise ValueError("Population cannot be empty")

        fitnesses = [c.fitness for c in population]

        if self.minimize:
            worst = max(fitnesses)
            weights = [(worst - f) + 1.0 for f in fitnesses]
        else:
            worst = min(fitnesses)
            weights = [(f - worst) + 1.0 for f in fitnesses]

        total_weight = sum(weights)
        if total_weight <= 0:
            return random.choice(population)

        spin = random.uniform(0, total_weight)
        cumulative = 0.0
        for individual, weight in zip(population, weights):
            cumulative += weight
            if cumulative >= spin:
                return individual

        return population[-1]
