from cvrp.problem import CVRPProblem
from cvrp.decoder import Route, decode_chromosome
from ga_toolbox.chromosome.base import Chromosome


def calculate_route_distance(route: Route, problem: CVRPProblem) -> float:
    """
    Compute total travel distance for a single route:
    Depot -> Customer 1 -> Customer 2 -> ... -> Customer K -> Depot.
    """
    if not route.customers:
        return 0.0

    dist = float(problem.distance_matrix[problem.depot][route.customers[0]])

    for i in range(len(route.customers) - 1):
        u = route.customers[i]
        v = route.customers[i + 1]
        dist += float(problem.distance_matrix[u][v])

    dist += float(problem.distance_matrix[route.customers[-1]][problem.depot])
    return dist


def cvrp_fitness(chromosome: Chromosome, problem: CVRPProblem) -> float:
    """
    Fitness evaluation function for CVRP.
    Calculates total routing cost (distance) across all vehicles.
    Lower is better (minimization).
    """
    routes = decode_chromosome(chromosome, problem)
    return sum(calculate_route_distance(r, problem) for r in routes)
