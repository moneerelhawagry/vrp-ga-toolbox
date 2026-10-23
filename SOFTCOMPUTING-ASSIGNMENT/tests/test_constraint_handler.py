import unittest

from cvrp.constraint_handler import cvrp_constraint_penalty, repair_cvrp_chromosome
from cvrp.decoder import decode_chromosome
from cvrp.problem import CVRPProblem
from ga_toolbox.chromosome.integer import IntegerChromosome


class TestCVRPConstraintHandler(unittest.TestCase):
    def setUp(self):
        self.problem = CVRPProblem(
            distance_matrix=[[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]],
            demands=[0, 2, 2, 2],
            num_vehicles=2,
            vehicle_capacity=4,
        )

    def test_penalty_is_zero_for_feasible_chromosome(self):
        chromosome = IntegerChromosome(
            length=3, permutation=True, genes=[1, 2, 3]
        )

        self.assertEqual(cvrp_constraint_penalty(chromosome, self.problem), 0.0)

    def test_penalty_scales_with_excess_vehicle_routes(self):
        chromosome = IntegerChromosome(
            length=3, permutation=True, genes=[1, 2, 3]
        )
        problem = CVRPProblem(
            distance_matrix=self.problem.distance_matrix,
            demands=self.problem.demands,
            num_vehicles=1,
            vehicle_capacity=4,
        )

        self.assertEqual(cvrp_constraint_penalty(chromosome, problem, 10), 10.0)

    def test_penalty_includes_excess_customer_demand(self):
        problem = CVRPProblem(
            distance_matrix=self.problem.distance_matrix,
            demands=[0, 5, 1, 1],
            num_vehicles=2,
            vehicle_capacity=4,
        )
        chromosome = IntegerChromosome(
            length=3, permutation=True, genes=[1, 2, 3]
        )

        self.assertEqual(cvrp_constraint_penalty(chromosome, problem, 10), 10.0)

    def test_repair_reorders_customers_into_feasible_routes(self):
        chromosome = IntegerChromosome(
            length=3, permutation=True, genes=[1, 2, 3]
        )

        repaired = repair_cvrp_chromosome(chromosome, self.problem)

        self.assertEqual(chromosome.genes, [1, 2, 3])
        self.assertEqual(sorted(repaired.genes), [1, 2, 3])
        self.assertLessEqual(
            len(decode_chromosome(repaired, self.problem)), self.problem.num_vehicles
        )
        self.assertIsNone(repaired.fitness)

    def test_repair_rejects_customer_demand_exceeding_capacity(self):
        problem = CVRPProblem(
            distance_matrix=self.problem.distance_matrix,
            demands=[0, 5, 1, 1],
            num_vehicles=2,
            vehicle_capacity=4,
        )
        chromosome = IntegerChromosome(
            length=3, permutation=True, genes=[1, 2, 3]
        )

        with self.assertRaises(ValueError):
            repair_cvrp_chromosome(chromosome, problem)

    def test_repair_rejects_invalid_customer_permutations(self):
        chromosome = IntegerChromosome(
            length=3, permutation=True, genes=[1, 1, 3]
        )

        with self.assertRaises(ValueError):
            repair_cvrp_chromosome(chromosome, self.problem)


if __name__ == "__main__":
    unittest.main()
