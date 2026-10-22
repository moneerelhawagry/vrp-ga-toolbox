import random
import unittest
from mutation.swap import SwapMutation
from mutation.inversion import InversionMutation
from mutation.scramble import ScrambleMutation

class MutationTests(unittest.TestCase):
    def setUp(self):
        self.original = [1,2,3,4,5,6]
        self.rng = random.Random(20)

    def test_swap_preserves_genes(self):
        result = SwapMutation().mutate(self.original, self.rng)
        self.assertEqual(sorted(result), sorted(self.original))

    def test_inversion_preserves_genes(self):
        result = InversionMutation().mutate(self.original, self.rng)
        self.assertEqual(sorted(result), sorted(self.original))

    def test_scramble_preserves_genes(self):
        result = ScrambleMutation().mutate(self.original, self.rng)
        self.assertEqual(sorted(result), sorted(self.original))

    def test_mutations_do_not_change_original(self):
        before = self.original.copy()
        for operation in (SwapMutation(), InversionMutation(), ScrambleMutation()):
            operation.mutate(self.original, self.rng)
        self.assertEqual(self.original, before)

if __name__ == "__main__": unittest.main()
