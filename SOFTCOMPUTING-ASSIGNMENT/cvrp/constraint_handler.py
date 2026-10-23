from typing import List, Set, Tuple

from cvrp.decoder import decode_chromosome
from cvrp.problem import CVRPProblem
from ga_toolbox.chromosome.base import Chromosome


def cvrp_constraint_penalty(
    chromosome: Chromosome,
    problem: CVRPProblem,
    penalty_factor: float = 1.0,
) -> float:
    if penalty_factor < 0:
        raise ValueError("penalty_factor must be non-negative")

    routes = decode_chromosome(chromosome, problem)
    route_violations = max(0, len(routes) - problem.num_vehicles)
    capacity_violations = sum(
        max(0, route.load - problem.vehicle_capacity) for route in routes
    )
    return float(penalty_factor * (route_violations + capacity_violations))


def repair_cvrp_chromosome(
    chromosome: Chromosome,
    problem: CVRPProblem,
) -> Chromosome:
    customer_ids = set(range(len(problem.demands))) - {problem.depot}
    genes = chromosome.genes

    if (
        len(genes) != len(customer_ids)
        or any(
            not isinstance(customer_id, int) or isinstance(customer_id, bool)
            for customer_id in genes
        )
        or set(genes) != customer_ids
    ):
        raise ValueError("chromosome genes must contain each customer exactly once")
    if problem.num_vehicles < 0:
        raise ValueError("num_vehicles must be non-negative")
    if problem.vehicle_capacity < 0:
        raise ValueError("vehicle_capacity must be non-negative")
    if any(problem.demands[customer_id] < 0 for customer_id in customer_ids):
        raise ValueError("customer demands must be non-negative")

    if any(
        problem.demands[customer_id] > problem.vehicle_capacity
        for customer_id in customer_ids
    ):
        raise ValueError("a customer demand exceeds vehicle capacity")
    if sum(problem.demands[customer_id] for customer_id in customer_ids) > (
        problem.num_vehicles * problem.vehicle_capacity
    ):
        raise ValueError("total customer demand exceeds fleet capacity")

    if not customer_ids:
        repaired = chromosome.copy()
        repaired.genes = []
        repaired.fitness = None
        repaired.is_feasible = True
        return repaired
    if problem.num_vehicles == 0:
        raise ValueError("customers cannot be served with zero vehicles")

    original_position = {customer_id: index for index, customer_id in enumerate(genes)}
    sorted_customers = sorted(
        customer_ids,
        key=lambda customer_id: (-problem.demands[customer_id], original_position[customer_id]),
    )
    bins: List[List[int]] = [[] for _ in range(problem.num_vehicles)]
    loads = [0] * problem.num_vehicles
    visited: Set[Tuple[int, Tuple[int, ...]]] = set()

    def assign_customer(index: int) -> bool:
        if index == len(sorted_customers):
            return True

        state = (index, tuple(sorted(loads)))
        if state in visited:
            return False
        visited.add(state)

        customer_id = sorted_customers[index]
        demand = problem.demands[customer_id]
        tried_loads: Set[int] = set()
        for bin_index, load in enumerate(loads):
            if load in tried_loads:
                continue
            tried_loads.add(load)
            if load + demand > problem.vehicle_capacity:
                continue

            bins[bin_index].append(customer_id)
            loads[bin_index] += demand
            if assign_customer(index + 1):
                return True
            loads[bin_index] -= demand
            bins[bin_index].pop()

        return False

    if not assign_customer(0):
        raise ValueError("customers cannot be packed into the available vehicles")

    repaired = chromosome.copy()
    repaired.genes = [
        customer_id
        for vehicle_customers in bins
        for customer_id in sorted(vehicle_customers, key=original_position.__getitem__)
    ]
    repaired.fitness = None
    repaired.is_feasible = True
    return repaired