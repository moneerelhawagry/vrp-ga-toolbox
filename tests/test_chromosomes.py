import unittest
from ga_toolbox.chromosome.binary import BinaryChromosome
from ga_toolbox.chromosome.integer import IntegerChromosome
from ga_toolbox.chromosome.floating_point import FloatChromosome


class TestBinaryChromosome(unittest.TestCase):
    def test_creation(self):
        c = BinaryChromosome(length=10)
        self.assertEqual(len(c), 10)
        self.assertTrue(all(g == 0 for g in c.genes))

    def test_randomize(self):
        c = BinaryChromosome(length=100)
        c.randomize()
        self.assertEqual(len(c), 100)
        self.assertTrue(all(g in (0, 1) for g in c.genes))
        self.assertTrue(0 < sum(c.genes) < 100)

    def test_copy_independence(self):
        c = BinaryChromosome(length=10)
        c.randomize()
        c2 = c.copy()
        c2.genes[0] = 1 - c2.genes[0]
        self.assertNotEqual(c.genes, c2.genes)

    def test_decode_to_int(self):
        c = BinaryChromosome(length=4, genes=[1, 0, 1, 0])
        self.assertEqual(c.decode_to_int(), 10)

    def test_decode_to_float(self):
        c = BinaryChromosome(length=4, genes=[1, 1, 1, 1])
        val = c.decode_to_float(0.0, 10.0)
        self.assertAlmostEqual(val, 10.0, places=5)


class TestIntegerChromosome(unittest.TestCase):
    def test_range_mode(self):
        c = IntegerChromosome(length=5, lower_bound=0, upper_bound=100, permutation=False)
        c.randomize()
        self.assertEqual(len(c), 5)
        self.assertTrue(all(0 <= g <= 100 for g in c.genes))

    def test_permutation_mode(self):
        c = IntegerChromosome(length=10, permutation=True)
        c.randomize()
        self.assertEqual(len(c), 10)
        self.assertEqual(sorted(c.genes), list(range(1, 11)))

    def test_permutation_no_duplicates(self):
        c = IntegerChromosome(length=20, permutation=True)
        c.randomize()
        self.assertEqual(len(set(c.genes)), 20)

    def test_copy_independence(self):
        c = IntegerChromosome(length=5, permutation=True)
        c.randomize()
        c2 = c.copy()
        c2.genes[0], c2.genes[1] = c2.genes[1], c2.genes[0]
        self.assertNotEqual(c.genes, c2.genes)


class TestFloatChromosome(unittest.TestCase):
    def test_creation(self):
        c = FloatChromosome(length=5, lower_bound=-5.0, upper_bound=5.0)
        self.assertEqual(len(c), 5)

    def test_randomize_bounds(self):
        c = FloatChromosome(length=100, lower_bound=-10.0, upper_bound=10.0)
        c.randomize()
        self.assertTrue(all(-10.0 <= g <= 10.0 for g in c.genes))

    def test_copy_independence(self):
        c = FloatChromosome(length=5, lower_bound=0.0, upper_bound=1.0)
        c.randomize()
        c2 = c.copy()
        c2.genes[0] = 999.0
        self.assertNotEqual(c.genes[0], 999.0)


if __name__ == '__main__':
    unittest.main()
