import unittest
import random
from ga_toolbox.chromosome.binary import BinaryChromosome
from ga_toolbox.selection.base import SelectionMethod
from ga_toolbox.crossover.base import CrossoverMethod
from ga_toolbox.mutation.base import MutationMethod
from ga_toolbox.replacement.base import ReplacementMethod
from ga_toolbox.ga_engine import GeneticAlgorithm
from ga_toolbox.utils import set_random_seed


class StubSelection(SelectionMethod):
    def select(self, population, count):
        selected = []
        for _ in range(count):
            tournament = random.sample(population, min(3, len(population)))
            winner = min(tournament, key=lambda c: c.fitness)
            selected.append(winner.copy())
        return selected


class StubCrossover(CrossoverMethod):
    def crossover(self, parent1, parent2):
        point = random.randint(1, max(1, len(parent1) - 1))
        child1 = parent1.copy()
        child2 = parent2.copy()
        child1.genes = parent1.genes[:point] + parent2.genes[point:]
        child2.genes = parent2.genes[:point] + parent1.genes[point:]
        return child1, child2


class StubMutation(MutationMethod):
    def mutate(self, chromosome, mutation_rate):
        if random.random() < mutation_rate:
            idx = random.randint(0, len(chromosome) - 1)
            chromosome.genes[idx] = 1 - chromosome.genes[idx]
        return chromosome


class StubReplacement(ReplacementMethod):
    def replace(self, old_population, offspring, pop_size):
        combined = old_population + offspring
        combined.sort(key=lambda c: c.fitness)
        return combined[:pop_size]


class TestGAEngineLifecycle(unittest.TestCase):
    def test_onemax_minimization(self):
        set_random_seed(42)
        prototype = BinaryChromosome(length=20)

        def fitness_fn(chrom):
            return sum(chrom.genes)

        ga = GeneticAlgorithm(
            chromosome_prototype=prototype,
            fitness_fn=fitness_fn,
            selection_method=StubSelection(),
            crossover_method=StubCrossover(),
            mutation_method=StubMutation(),
            replacement_method=StubReplacement(),
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
        self.assertEqual(len(result.best_fitness_history), 50)
        self.assertEqual(len(result.avg_fitness_history), 50)
        self.assertLessEqual(result.best_fitness, result.best_fitness_history[0])

    def test_feasibility_penalty(self):
        set_random_seed(99)
        prototype = BinaryChromosome(length=10)

        def fitness_fn(chrom):
            return sum(chrom.genes)

        def feasibility_fn(chrom):
            return sum(chrom.genes) <= 5

        ga = GeneticAlgorithm(
            chromosome_prototype=prototype,
            fitness_fn=fitness_fn,
            selection_method=StubSelection(),
            crossover_method=StubCrossover(),
            mutation_method=StubMutation(),
            replacement_method=StubReplacement(),
            feasibility_fn=feasibility_fn,
            population_size=20,
            generations=15,
            penalty_factor=500.0,
            maximize=False,
        )

        result = ga.run(verbose=False)
        self.assertTrue(result.best_chromosome.is_feasible)

    def test_population_size_maintained(self):
        set_random_seed(7)
        prototype = BinaryChromosome(length=15)

        ga = GeneticAlgorithm(
            chromosome_prototype=prototype,
            fitness_fn=lambda c: sum(c.genes),
            selection_method=StubSelection(),
            crossover_method=StubCrossover(),
            mutation_method=StubMutation(),
            replacement_method=StubReplacement(),
            population_size=25,
            generations=5,
        )
        ga.run(verbose=False)
        self.assertEqual(len(ga.population), 25)


if __name__ == '__main__':
    unittest.main()
