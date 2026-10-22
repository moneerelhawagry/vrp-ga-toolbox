from typing import List
from ga_toolbox.chromosome.base import Chromosome
from cvrp.problem import CVRPProblem


class Route:
    """
    Represents an individual vehicle route in a CVRP solution.

    Attributes:
        customers: List of customer node IDs visited in sequential order.
        load: Cumulative demand fulfilled along this route.
    """

    def __init__(self, customers: List[int] = None, load: int = 0):
        self.customers: List[int] = customers if customers is not None else []
        self.load: int = load

    def __repr__(self) -> str:
        return f"Route(customers={self.customers}, load={self.load})"


def decode_chromosome(chromosome: Chromosome, problem: CVRPProblem) -> List[Route]:
    """
    Deterministic Greedy Split algorithm:
    Transforms a permutation chromosome of customer IDs into distinct vehicle routes.
    Scans left-to-right and greedily partitions whenever adding the next customer
    would exceed the vehicle's capacity.

    Args:
        chromosome: Permutation chromosome containing customer IDs (1..N).
        problem: CVRPProblem instance with demands and vehicle_capacity.

    Returns:
        List of Route objects representing the fleet's delivery tours.
    """
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
