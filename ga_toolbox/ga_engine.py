import random
from typing import Callable, Optional, List

from ga_toolbox.chromosome.base import Chromosome
from ga_toolbox.selection.base import SelectionMethod
from ga_toolbox.crossover.base import CrossoverMethod
from ga_toolbox.mutation.base import MutationMethod
from ga_toolbox.replacement.base import ReplacementMethod
from ga_toolbox.utils import GAResult


class GeneticAlgorithm:
    """
    Core Genetic Algorithm optimization engine.

    Follows clean OOP principles: takes abstract operators via Dependency Injection
    and uses the Prototype pattern for chromosome instantiation.
    """

    def __init__(
        self,
        chromosome_prototype: Chromosome,
        fitness_fn: Callable[[Chromosome], float],
        selection_method: SelectionMethod,
        crossover_method: CrossoverMethod,
        mutation_method: MutationMethod,
        replacement_method: ReplacementMethod,
        feasibility_fn: Optional[Callable[[Chromosome], bool]] = None,
        population_size: int = 100,
        generations: int = 200,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.05,
        elitism_count: int = 2,
        maximize: bool = False,
        penalty_factor: float = 1000.0,
    ):
        self.chromosome_prototype = chromosome_prototype
        self.fitness_fn = fitness_fn
        self.selection_method = selection_method
        self.crossover_method = crossover_method
        self.mutation_method = mutation_method
        self.replacement_method = replacement_method
        self.feasibility_fn = feasibility_fn

        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism_count = max(0, min(elitism_count, population_size))
        self.maximize = maximize
        self.penalty_factor = penalty_factor

        self.population: List[Chromosome] = []
        self.result = GAResult()

    def initialize_population(self) -> List[Chromosome]:
        """Initialize population by cloning the prototype and randomizing each instance."""
        population = []
        for _ in range(self.population_size):
            ind = self.chromosome_prototype.copy()
            ind.randomize()
            population.append(ind)
        return population

    def evaluate_population(self, population: List[Chromosome]) -> None:
        """Calculate fitness and apply feasibility check/penalty."""
        for ind in population:
            raw_fitness = float(self.fitness_fn(ind))

            if self.feasibility_fn is not None:
                ind.is_feasible = bool(self.feasibility_fn(ind))
            else:
                ind.is_feasible = True

            if not ind.is_feasible:
                if self.maximize:
                    raw_fitness -= self.penalty_factor
                else:
                    raw_fitness += self.penalty_factor

            ind.fitness = raw_fitness

    def _sort_population(self, population: List[Chromosome]) -> List[Chromosome]:
        """Sort population with best individuals first."""
        return sorted(population, key=lambda c: c.fitness, reverse=self.maximize)

    def _get_best(self, population: List[Chromosome]) -> Chromosome:
        """Retrieve the best individual according to optimization objective."""
        if self.maximize:
            return max(population, key=lambda c: c.fitness)
        return min(population, key=lambda c: c.fitness)

    def _is_better(self, fitness_a: float, fitness_b: float) -> bool:
        if self.maximize:
            return fitness_a > fitness_b
        return fitness_a < fitness_b

    def step(self, population: List[Chromosome]) -> List[Chromosome]:
        """Execute a single evolutionary generation."""
        sorted_pop = self._sort_population(population)

        # 1. Elitism: preserve top individuals
        elites = [ind.copy() for ind in sorted_pop[:self.elitism_count]]

        # 2. Selection: select parents for mating
        offspring_needed = self.population_size - self.elitism_count
        parents = self.selection_method.select(population, offspring_needed)

        # 3. Crossover: generate offspring
        offspring: List[Chromosome] = []
        i = 0
        while len(offspring) < offspring_needed:
            p1 = parents[i % len(parents)]
            p2 = parents[(i + 1) % len(parents)]
            if random.random() < self.crossover_rate:
                c1, c2 = self.crossover_method.crossover(p1.copy(), p2.copy())
            else:
                c1, c2 = p1.copy(), p2.copy()
            offspring.append(c1)
            if len(offspring) < offspring_needed:
                offspring.append(c2)
            i += 2

        # 4. Mutation: apply mutation to each child
        for k in range(len(offspring)):
            offspring[k] = self.mutation_method.mutate(offspring[k], self.mutation_rate)

        # 5. Evaluate offspring
        self.evaluate_population(offspring)

        # 6. Replacement: delegate population synthesis to replacement operator
        if self.elitism_count == 0:
            return self.replacement_method.replace(sorted_pop, offspring, self.population_size)

        remaining_pop = self.replacement_method.replace(
            sorted_pop,
            offspring,
            offspring_needed
        )
        return elites + remaining_pop

    def run(self, verbose: bool = False) -> GAResult:
        """Run the evolutionary loop for the configured number of generations."""
        self.population = self.initialize_population()
        self.evaluate_population(self.population)

        best_overall = self._get_best(self.population)
        self.result.best_chromosome = best_overall.copy()
        self.result.best_fitness = best_overall.fitness

        for gen in range(self.generations):
            current_best = self._get_best(self.population)
            avg_fitness = sum(c.fitness for c in self.population) / len(self.population)

            self.result.best_fitness_history.append(current_best.fitness)
            self.result.avg_fitness_history.append(avg_fitness)

            self.population = self.step(self.population)

            gen_best = self._get_best(self.population)
            if self._is_better(gen_best.fitness, self.result.best_fitness):
                self.result.best_fitness = gen_best.fitness
                self.result.best_chromosome = gen_best.copy()

            if verbose and (gen == 0 or (gen + 1) % 50 == 0 or gen == self.generations - 1):
                print(f"Gen {gen + 1}/{self.generations} | Best: {self.result.best_fitness:.4f} | Avg: {avg_fitness:.4f}")

        self.result.generations_run = self.generations
        return self.result
