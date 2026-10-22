import random
import unittest
from crossover.multi_point import MultiPointCrossover
from crossover.order_crossover import OrderCrossover

class CrossoverTests(unittest.TestCase):
    def test_multi_point_keeps_length(self):
        rng = random.Random(10)
        a, b = MultiPointCrossover(2).crossover([0,0,1,1,0,1], [1,1,0,0,1,0], rng)
        self.assertEqual(len(a), 6); self.assertEqual(len(b), 6)
        self.assertTrue(set(a).issubset({0,1})); self.assertTrue(set(b).issubset({0,1}))

    def test_multi_point_rejects_unequal_lengths(self):
        with self.assertRaises(ValueError):
            MultiPointCrossover().crossover([1,2], [1])

    def test_order_crossover_preserves_permutation(self):
        rng = random.Random(11)
        p1, p2 = [1,2,3,4,5,6], [4,1,6,2,5,3]
        c1, c2 = OrderCrossover().crossover(p1, p2, rng)
        self.assertEqual(sorted(c1), sorted(p1)); self.assertEqual(sorted(c2), sorted(p2))
        self.assertEqual(len(set(c1)), len(c1)); self.assertEqual(len(set(c2)), len(c2))

    def test_order_crossover_rejects_different_items(self):
        with self.assertRaises(ValueError):
            OrderCrossover().crossover([1,2,3], [1,2,4])

if __name__ == "__main__": unittest.main()
