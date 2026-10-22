from cvrp.problem import CVRPProblem
from cvrp.decoder import decode_chromosome
from ga_toolbox.chromosome.base import Chromosome


def cvrp_feasibility(chromosome: Chromosome, problem: CVRPProblem) -> bool:
    """
    Feasibility check for CVRP solutions:
    1. Total routes used must not exceed available fleet size (num_vehicles).
    2. No single route can exceed vehicle capacity.
    """
    routes = decode_chromosome(chromosome, problem)

    if len(routes) > problem.num_vehicles:
        return False

    for r in routes:
        if r.load > problem.vehicle_capacity:
            return False

    return True
