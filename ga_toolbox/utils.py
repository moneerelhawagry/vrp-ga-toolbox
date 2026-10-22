import random
from dataclasses import dataclass, field
from typing import List, Optional
from ga_toolbox.chromosome.base import Chromosome


@dataclass
class GAResult:
    """Container holding summary and convergence history for a GA run."""
    best_chromosome: Optional[Chromosome] = None
    best_fitness: float = float('inf')
    best_fitness_history: List[float] = field(default_factory=list)
    avg_fitness_history: List[float] = field(default_factory=list)
    generations_run: int = 0


def set_random_seed(seed: int) -> None:
    """Set pseudo-random generator seed for reproducible experiments."""
    random.seed(seed)
