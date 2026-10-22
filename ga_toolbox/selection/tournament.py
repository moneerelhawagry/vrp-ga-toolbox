import random
from .base import SelectionMethod


class TournamentSelection(SelectionMethod):
    def __init__(self, tournament_size=3, minimize=True):
        super().__init__(minimize)
        self.tournament_size = tournament_size

    def select(self, population):
    
        k = min(self.tournament_size, len(population))
        contestants = random.sample(population, k)

        # the best one among them wins
        winner = contestants[0]
        for c in contestants[1:]:
            if self.is_better(c.fitness, winner.fitness):
                winner = c
        return winner