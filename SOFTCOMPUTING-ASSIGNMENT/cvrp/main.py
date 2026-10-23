import random
from functools import partial
from typing import List

from ga_toolbox.chromosome.integer import IntegerChromosome
from ga_toolbox.ga_engine import GeneticAlgorithm
from ga_toolbox.utils import set_random_seed
from ga_toolbox.selection.base import SelectionMethod
from ga_toolbox.crossover.base import CrossoverMethod
from ga_toolbox.mutation.base import MutationMethod
from ga_toolbox.replacement.base import ReplacementMethod

from cvrp.problem import create_ortools_example, CVRPProblem
from cvrp.decoder import decode_chromosome, Route
from cvrp.fitness import cvrp_fitness, calculate_route_distance
from cvrp.feasibility import cvrp_feasibility


class StubTournamentSelection(SelectionMethod):
    def __init__(self, k: int = 3):
        self.k = k

    def select(self, population, count):
        selected = []
        for _ in range(count):
            tournament = random.sample(population, min(self.k, len(population)))
            winner = min(tournament, key=lambda c: c.fitness)
            selected.append(winner.copy())
        return selected


class StubOrderCrossover(CrossoverMethod):
    def crossover(self, parent1, parent2):
        size = len(parent1.genes)
        child1 = parent1.copy()
        child2 = parent2.copy()

        start, end = sorted(random.sample(range(size), 2))

        c1_genes = [None] * size
        c1_genes[start : end + 1] = parent1.genes[start : end + 1]
        fill1 = [g for g in parent2.genes if g not in c1_genes[start : end + 1]]
        idx = 0
        for i in range(size):
            if c1_genes[i] is None:
                c1_genes[i] = fill1[idx]
                idx += 1
        child1.genes = c1_genes

        c2_genes = [None] * size
        c2_genes[start : end + 1] = parent2.genes[start : end + 1]
        fill2 = [g for g in parent1.genes if g not in c2_genes[start : end + 1]]
        idx = 0
        for i in range(size):
            if c2_genes[i] is None:
                c2_genes[i] = fill2[idx]
                idx += 1
        child2.genes = c2_genes

        return child1, child2


class StubHybridMutation(MutationMethod):
    def mutate(self, chromosome, mutation_rate):
        if random.random() < mutation_rate:
            size = len(chromosome.genes)
            if size >= 2:
                if random.random() < 0.7:
                    i, j = sorted(random.sample(range(size), 2))
                    chromosome.genes[i : j + 1] = chromosome.genes[i : j + 1][::-1]
                else:
                    i, j = random.sample(range(size), 2)
                    chromosome.genes[i], chromosome.genes[j] = chromosome.genes[j], chromosome.genes[i]
        return chromosome


class StubElitistReplacement(ReplacementMethod):
    def replace(self, old_population, offspring, pop_size):
        combined = old_population + offspring
        combined.sort(key=lambda c: c.fitness)
        return combined[:pop_size]

def print_solution(routes: List[Route], problem: CVRPProblem) -> None:
    total_distance = 0.0
    total_load = 0

    for vehicle_id, route in enumerate(routes):
        route_dist = calculate_route_distance(route, problem)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        cumul_load = 0
        plan_output += f" {problem.depot} Load({cumul_load}) -> "

        for node in route.customers:
            cumul_load += problem.demands[node]
            plan_output += f" {node} Load({cumul_load}) -> "

        plan_output += f" {problem.depot} Load({cumul_load})\n"
        plan_output += f"Distance of the route: {int(route_dist)}m\n"
        plan_output += f"Load of the route: {route.load}\n"
        print(plan_output)

        total_distance += route_dist
        total_load += route.load

    # Display unused vehicles if any
    for vehicle_id in range(len(routes), problem.num_vehicles):
        print(f"Route for vehicle {vehicle_id}:\n {problem.depot} Load(0) ->  {problem.depot} Load(0)")
        print("Distance of the route: 0m\nLoad of the route: 0\n")

    print(f"Total distance of all routes: {int(total_distance)}m")
    print(f"Total load of all routes: {total_load}")

def run_cvrp_solver(
    pop_size: int = 200,
    generations: int = 400,
    crossover_rate: float = 0.9,
    mutation_rate: float = 0.2,
    elitism_count: int = 4,
    seed: int = 42,
    verbose: bool = True,
):
    set_random_seed(seed)
    problem = create_ortools_example()

    print("=" * 65)
    print("CAPACITATED VEHICLE ROUTING PROBLEM (CVRP) — GA SOLVER")
    print("=" * 65)
    print(f"Customers: {problem.num_customers} | Vehicles: {problem.num_vehicles} | Vehicle Capacity: {problem.vehicle_capacity}")
    print(f"Total Demand: {sum(problem.demands)} | Max Fleet Capacity: {problem.num_vehicles * problem.vehicle_capacity}")
    print("-" * 65)

    prototype = IntegerChromosome(length=problem.num_customers, permutation=True)

    fitness_fn = partial(cvrp_fitness, problem=problem)
    feasibility_fn = partial(cvrp_feasibility, problem=problem)

    ga = GeneticAlgorithm(
        chromosome_prototype=prototype,
        fitness_fn=fitness_fn,
        selection_method=StubTournamentSelection(k=3),
        crossover_method=StubOrderCrossover(),
        mutation_method=StubHybridMutation(),
        replacement_method=StubElitistReplacement(),
        feasibility_fn=feasibility_fn,
        population_size=pop_size,
        generations=generations,
        crossover_rate=crossover_rate,
        mutation_rate=mutation_rate,
        elitism_count=elitism_count,
        maximize=False,
        penalty_factor=10000.0,
    )

    result = ga.run(verbose=verbose)

    best_routes = decode_chromosome(result.best_chromosome, problem)
    print("\n" + "=" * 65)
    print("BEST CVRP SOLUTION FOUND")
    print("=" * 65)
    print_solution(best_routes, problem)

    optimal_benchmark = 6208
    gap = ((result.best_fitness - optimal_benchmark) / optimal_benchmark) * 100
    print("-" * 65)
    print(f"Benchmark Optimum: {optimal_benchmark}m")
    print(f"GA Best Result:    {int(result.best_fitness)}m (Optimality Gap: {gap:.1f}%)")
    print("=" * 65)

    return result, best_routes


if __name__ == "__main__":
    run_cvrp_solver()
