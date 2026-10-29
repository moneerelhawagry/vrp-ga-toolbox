import random
from typing import List
from ga_toolbox.chromosome.base import Chromosome
from ga_toolbox.selection.base import SelectionMethod


class TournamentSelection(SelectionMethod):
    """
    Tournament Selection Operator:
    Samples k individuals at random and selects the one with the best fitness.
    """

    def __init__(self, tournament_size: int = 3, minimize: bool = True):
        super().__init__(minimize=minimize)
        self.tournament_size = tournament_size

    def select_one(self, population: List[Chromosome]) -> Chromosome:
        k = min(self.tournament_size, len(population))
        contestants = random.sample(population, k)

        winner = contestants[0]
        for c in contestants[1:]:
            if self.is_better(c.fitness, winner.fitness):
                winner = c
        return winner
