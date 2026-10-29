import unittest
from ga_toolbox.chromosome.integer import IntegerChromosome
from ga_toolbox.selection.tournament import TournamentSelection
from ga_toolbox.selection.roulette_wheel import RouletteWheelSelection


class DummyChromosome:
    def __init__(self, fitness):
        self.fitness = fitness
        self.genes = [1]
        self.is_feasible = True

    def copy(self):
        c = DummyChromosome(self.fitness)
        c.genes = list(self.genes)
        return c


class TestSelectionMethods(unittest.TestCase):
    def setUp(self):
        self.population = [DummyChromosome(f) for f in [10, 20, 30, 40, 50]]

    def test_tournament_selection_returns_member(self):
        sel = TournamentSelection(tournament_size=3, minimize=True)
        winner = sel.select_one(self.population)
        self.assertIn(winner.fitness, [10, 20, 30, 40, 50])

    def test_tournament_full_size_picks_best(self):
        sel_min = TournamentSelection(tournament_size=5, minimize=True)
        self.assertEqual(sel_min.select_one(self.population).fitness, 10)

        sel_max = TournamentSelection(tournament_size=5, minimize=False)
        self.assertEqual(sel_max.select_one(self.population).fitness, 50)

    def test_tournament_batch_select(self):
        sel = TournamentSelection(tournament_size=3, minimize=True)
        selected = sel.select(self.population, count=4)
        self.assertEqual(len(selected), 4)

    def test_roulette_wheel_returns_member(self):
        rw = RouletteWheelSelection(minimize=True)
        winner = rw.select_one(self.population)
        self.assertIn(winner.fitness, [10, 20, 30, 40, 50])

    def test_roulette_wheel_favors_better_fitness(self):
        rw = RouletteWheelSelection(minimize=True)
        picks = [rw.select_one(self.population).fitness for _ in range(1000)]
        self.assertGreater(picks.count(10), picks.count(50))


if __name__ == '__main__':
    unittest.main()
