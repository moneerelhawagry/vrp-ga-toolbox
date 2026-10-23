from ga_toolbox.replacement.elitist import ElitistReplacement
from ga_toolbox.replacement.generational import GenerationalReplacement


class Dummy:
    """Fake chromosome just for testing."""
    def __init__(self, fitness):
        self.fitness = fitness

    def copy(self):
        return Dummy(self.fitness)


def make(values):
    return [Dummy(v) for v in values]


def fits(pop):
    return [c.fitness for c in pop]


def test_elitist_keeps_size():
    old = make([10, 20, 30, 40, 50])
    new = make([60, 70, 80, 90, 100])
    result = ElitistReplacement(elitism_count=2).replace(old, new)
    assert len(result) == len(old)


def test_elitist_keeps_best_old_even_if_offspring_worse():
    old = make([10, 20, 30, 40, 50])
    new = make([60, 70, 80, 90, 100])
    result = ElitistReplacement(elitism_count=2, minimize=True).replace(old, new)

    assert 10 in fits(result)
    assert 20 in fits(result)


def test_elitist_maximize():
    old = make([10, 20, 30, 40, 50])
    new = make([60, 70, 80, 90, 100])
    result = ElitistReplacement(elitism_count=2, minimize=False).replace(old, new)

    assert 50 in fits(result)
    assert 40 in fits(result)


def test_elitist_not_enough_offspring():
    old = make([10, 20, 30, 40, 50])
    new = make([1, 2])
    result = ElitistReplacement(elitism_count=2).replace(old, new)

    assert len(result) == 5

def test_generational_pure_returns_offspring():
    old = make([10, 20, 30, 40, 50])
    new = make([60, 70, 80, 90, 100])
    result = GenerationalReplacement(elitism_count=0).replace(old, new)
    assert fits(result) == [60, 70, 80, 90, 100]


def test_generational_with_elitism_keeps_best_old():
    old = make([10, 20, 30, 40, 50])
    new = make([60, 70, 80, 90, 100])
    result = GenerationalReplacement(elitism_count=1).replace(old, new)
    assert len(result) == 5
    assert 10 in fits(result)