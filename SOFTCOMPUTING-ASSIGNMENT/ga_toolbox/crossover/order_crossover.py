import random
from typing import Sequence

class OrderCrossover:
    def crossover(self, parent_a: Sequence[int], parent_b: Sequence[int],
                  rng: random.Random | None = None) -> tuple[list[int], list[int]]:
        if len(parent_a) != len(parent_b):
            raise ValueError("Parents must have equal length")
        if len(set(parent_a)) != len(parent_a) or len(set(parent_b)) != len(parent_b):
            raise ValueError("Parents must not contain duplicate items")
        if set(parent_a) != set(parent_b):
            raise ValueError("Parents must contain the same items")
        generator = rng if rng is not None else random.Random()
        n = len(parent_a)
        if n < 2:
            return list(parent_a), list(parent_b)
        left, right = sorted(generator.sample(range(n), 2))
        def make_child(segment_parent, fill_parent):
            child = [None] * n
            child[left:right + 1] = segment_parent[left:right + 1]
            used = set(child[left:right + 1])
            scan = list(fill_parent[right + 1:]) + list(fill_parent[:right + 1])
            fill = [item for item in scan if item not in used]
            positions = list(range(right + 1, n)) + list(range(0, left))
            for position, item in zip(positions, fill):
                child[position] = item
            return child
        return make_child(parent_a, parent_b), make_child(parent_b, parent_a)
