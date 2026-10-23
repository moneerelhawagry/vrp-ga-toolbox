from abc import ABC, abstractmethod
from typing import List
from ga_toolbox.chromosome.base import Chromosome


class SelectionMethod(ABC):
    def __init__(self, minimize: bool = True):
        self.minimize = minimize

    def is_better(self, a: float, b: float) -> bool:
        return a < b if self.minimize else a > b

    @abstractmethod
    def select_one(self, population: List[Chromosome]) -> Chromosome:
        pass

    def select(self, population: List[Chromosome], count: int) -> List[Chromosome]:
        return [self.select_one(population).copy() for _ in range(count)]