from typing import List
from ga_toolbox.chromosome.base import Chromosome
from cvrp.problem import CVRPProblem


class Route:
    def __init__(self, customers: List[int] = None, load: int = 0):
        self.customers: List[int] = customers if customers is not None else []
        self.load: int = load

    def __repr__(self) -> str:
        return f"Route(customers={self.customers}, load={self.load})"


def decode_chromosome(chromosome: Chromosome, problem: CVRPProblem) -> List[Route]:
    routes: List[Route] = []
    current_route = Route()

    for customer_id in chromosome.genes:
        demand = problem.demands[customer_id]

        if current_route.load + demand > problem.vehicle_capacity and current_route.customers:
            routes.append(current_route)
            current_route = Route()

        current_route.customers.append(customer_id)
        current_route.load += demand

    if current_route.customers:
        routes.append(current_route)

    return routes
