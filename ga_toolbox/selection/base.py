from abc import ABC, abstractmethod


class SelectionMethod(ABC):
    """Base class for all selection methods."""

    def __init__(self, minimize=True):
    
        self.minimize = minimize

    def is_better(self, a, b):
        """Return True if fitness a is better than fitness b."""
        if self.minimize:
            return a < b
        return a > b

    @abstractmethod
    def select(self, population):
        """Pick ONE chromosome from the population."""
        pass