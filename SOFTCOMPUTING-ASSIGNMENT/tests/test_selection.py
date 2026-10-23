from ga_toolbox.selection.tournament import TournamentSelection
from ga_toolbox.selection.roulette_wheel import RouletteWheelSelection


class Dummy:
    """Fake chromosome just for testing."""
    def __init__(self, fitness):
        self.fitness = fitness

    def copy(self):
        return Dummy(self.fitness)


def make_pop():
    return [Dummy(f) for f in [10, 20, 30, 40, 50]]


def test_tournament_returns_member():
    pop = make_pop()
    assert TournamentSelection(3).select_one(pop) in pop


def test_tournament_full_size_picks_best():
    pop = make_pop()
    assert TournamentSelection(5, minimize=True).select_one(pop).fitness == 10


def test_tournament_maximize():
    pop = make_pop()
    assert TournamentSelection(5, minimize=False).select_one(pop).fitness == 50


def test_roulette_returns_member():
    pop = make_pop()
    assert RouletteWheelSelection(minimize=True).select_one(pop) in pop


def test_roulette_favors_better():
    pop = make_pop()
    sel = RouletteWheelSelection(minimize=True)
    picks = [sel.select_one(pop).fitness for _ in range(2000)]
    assert picks.count(10) > picks.count(50)