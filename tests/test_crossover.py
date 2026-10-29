import unittest
from ga_toolbox.chromosome.integer import IntegerChromosome
from ga_toolbox.chromosome.binary import BinaryChromosome
from ga_toolbox.crossover.multi_point import MultiPointCrossover
from ga_toolbox.crossover.order_crossover import OrderCrossover


class TestCrossoverMethods(unittest.TestCase):
    def test_multipoint_crossover_binary(self):
        p1 = BinaryChromosome(length=6, genes=[0, 0, 0, 0, 0, 0])
        p2 = BinaryChromosome(length=6, genes=[1, 1, 1, 1, 1, 1])
        mp = MultiPointCrossover(points=2)
        c1, c2 = mp.crossover(p1, p2)
        self.assertEqual(len(c1), 6)
        self.assertEqual(len(c2), 6)

    def test_order_crossover_permutation(self):
        p1 = IntegerChromosome(length=8, permutation=True, genes=[1, 2, 3, 4, 5, 6, 7, 8])
        p2 = IntegerChromosome(length=8, permutation=True, genes=[8, 7, 6, 5, 4, 3, 2, 1])
        ox = OrderCrossover()
        c1, c2 = ox.crossover(p1, p2)
        self.assertEqual(sorted(c1.genes), list(range(1, 9)))
        self.assertEqual(sorted(c2.genes), list(range(1, 9)))


if __name__ == '__main__':
    unittest.main()
