from cvrp.problem import CVRPProblem
from cvrp.decoder import decode_chromosome
from ga_toolbox.chromosome.base import Chromosome


def cvrp_feasibility(chromosome: Chromosome, problem: CVRPProblem) -> bool:
    routes = decode_chromosome(chromosome, problem)

    if len(routes) > problem.num_vehicles:
        return False

    for r in routes:
        if r.load > problem.vehicle_capacity:
            return False

    return True
