import unittest
from ga_toolbox.replacement.generational import GenerationalReplacement
from ga_toolbox.replacement.elitist import ElitistReplacement


class DummyChromosome:
    def __init__(self, fitness):
        self.fitness = fitness
        self.genes = [1]
        self.is_feasible = True

    def copy(self):
        c = DummyChromosome(self.fitness)
        c.genes = list(self.genes)
        return c


class TestReplacementMethods(unittest.TestCase):
    def setUp(self):
        self.old_pop = [DummyChromosome(f) for f in [10, 20, 30]]
        self.offspring = [DummyChromosome(f) for f in [5, 25, 40]]

    def test_generational_replacement(self):
        gen = GenerationalReplacement(minimize=True)
        new_pop = gen.replace(self.old_pop, self.offspring, pop_size=3)
        self.assertEqual(len(new_pop), 3)
        self.assertEqual([c.fitness for c in new_pop], [5, 25, 40])

    def test_elitist_replacement(self):
        elitist = ElitistReplacement(minimize=True)
        new_pop = elitist.replace(self.old_pop, self.offspring, pop_size=3)
        self.assertEqual(len(new_pop), 3)
        # Combined: [5, 10, 20, 25, 30, 40] -> Best 3 in minimization are 5, 10, 20
        self.assertEqual([c.fitness for c in new_pop], [5, 10, 20])


if __name__ == '__main__':
    unittest.main()
