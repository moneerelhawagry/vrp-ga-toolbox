import unittest
from ga_toolbox.chromosome.integer import IntegerChromosome
from cvrp.problem import create_ortools_example
from cvrp.decoder import decode_chromosome
from cvrp.fitness import cvrp_fitness, calculate_route_distance
from cvrp.feasibility import cvrp_feasibility


class TestCVRPComponents(unittest.TestCase):
    def setUp(self):
        self.problem = create_ortools_example()

    def test_decoder_serves_all_customers_uniquely(self):
        chrom = IntegerChromosome(length=16, permutation=True)
        chrom.randomize()
        routes = decode_chromosome(chrom, self.problem)
        visited = []
        for r in routes:
            visited.extend(r.customers)
        self.assertEqual(sorted(visited), list(range(1, 17)))

    def test_no_route_violates_vehicle_capacity(self):
        chrom = IntegerChromosome(length=16, permutation=True)
        for _ in range(20):
            chrom.randomize()
            routes = decode_chromosome(chrom, self.problem)
            for r in routes:
                self.assertLessEqual(r.load, self.problem.vehicle_capacity)

    def test_fitness_is_deterministic(self):
        genes = list(range(1, 17))
        c1 = IntegerChromosome(length=16, permutation=True, genes=list(genes))
        c2 = IntegerChromosome(length=16, permutation=True, genes=list(genes))
        self.assertEqual(cvrp_fitness(c1, self.problem), cvrp_fitness(c2, self.problem))

    def test_known_route_distance(self):
        chrom = IntegerChromosome(length=16, permutation=True, genes=list(range(1, 17)))
        routes = decode_chromosome(chrom, self.problem)
        total_dist = sum(calculate_route_distance(r, self.problem) for r in routes)
        self.assertGreater(total_dist, 0.0)

    def test_feasibility_check_contract(self):
        chrom = IntegerChromosome(length=16, permutation=True)
        chrom.randomize()
        res = cvrp_feasibility(chrom, self.problem)
        self.assertIsInstance(res, bool)


if __name__ == "__main__":
    unittest.main()
