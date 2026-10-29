import unittest
from ga_toolbox.chromosome.integer import IntegerChromosome
from ga_toolbox.mutation.swap import SwapMutation
from ga_toolbox.mutation.inversion import InversionMutation
from ga_toolbox.mutation.scramble import ScrambleMutation


class TestMutationMethods(unittest.TestCase):
    def test_swap_mutation(self):
        c = IntegerChromosome(length=5, permutation=True, genes=[1, 2, 3, 4, 5])
        sm = SwapMutation()
        sm.mutate(c, mutation_rate=1.0)
        self.assertEqual(sorted(c.genes), [1, 2, 3, 4, 5])

    def test_inversion_mutation(self):
        c = IntegerChromosome(length=5, permutation=True, genes=[1, 2, 3, 4, 5])
        im = InversionMutation()
        im.mutate(c, mutation_rate=1.0)
        self.assertEqual(sorted(c.genes), [1, 2, 3, 4, 5])

    def test_scramble_mutation(self):
        c = IntegerChromosome(length=5, permutation=True, genes=[1, 2, 3, 4, 5])
        scm = ScrambleMutation()
        scm.mutate(c, mutation_rate=1.0)
        self.assertEqual(sorted(c.genes), [1, 2, 3, 4, 5])


if __name__ == '__main__':
    unittest.main()
