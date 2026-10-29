import unittest
from ga_toolbox.chromosome.binary import BinaryChromosome
from ga_toolbox.selection.tournament import TournamentSelection
from ga_toolbox.crossover.multi_point import MultiPointCrossover
from ga_toolbox.mutation.swap import SwapMutation
from ga_toolbox.replacement.elitist import ElitistReplacement
from ga_toolbox.ga_engine import GeneticAlgorithm
from ga_toolbox.utils import set_random_seed


class TestGAEngineLifecycle(unittest.TestCase):
    def test_onemax_minimization(self):
        set_random_seed(42)
        prototype = BinaryChromosome(length=20)

        def fitness_fn(chrom):
            return sum(chrom.genes)

        ga = GeneticAlgorithm(
            chromosome_prototype=prototype,
            fitness_fn=fitness_fn,
            selection_method=TournamentSelection(tournament_size=3, minimize=True),
            crossover_method=MultiPointCrossover(points=1),
            mutation_method=SwapMutation(),
            replacement_method=ElitistReplacement(minimize=True),
            population_size=30,
            generations=50,
            crossover_rate=0.8,
            mutation_rate=0.2,
            elitism_count=2,
            maximize=False,
        )

        result = ga.run(verbose=False)
        self.assertIsNotNone(result.best_chromosome)
        self.assertEqual(result.generations_run, 50)
        self.assertLessEqual(result.best_fitness, result.best_fitness_history[0])


if __name__ == '__main__':
    unittest.main()
