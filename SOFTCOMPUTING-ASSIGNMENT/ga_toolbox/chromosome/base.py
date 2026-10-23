from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Optional, List, Any


class Chromosome(ABC):

    def __init__(self, genes: Optional[List[Any]] = None):
        self.genes: List[Any] = genes if genes is not None else []
        self.fitness: Optional[float] = None
        self.is_feasible: bool = True

    @abstractmethod
    def randomize(self) -> None:
        pass

    def copy(self) -> "Chromosome":
        return deepcopy(self)

    def __len__(self) -> int:
        return len(self.genes)

    def __getitem__(self, index: int) -> Any:
        return self.genes[index]

    def __setitem__(self, index: int, value: Any) -> None:
        self.genes[index] = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(genes={self.genes}, fitness={self.fitness}, feasible={self.is_feasible})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Chromosome):
            return NotImplemented
        return self.genes == other.genes
