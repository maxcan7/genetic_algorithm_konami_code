import random

import pytest

from helpers import check_winners, crossover, populate, select
from player import Player


def test_populate():
    players = populate(size=10, mutation_rate=0.1)
    assert len(players) == 10
    for player in players:
        assert isinstance(player, Player)
        assert len(player.dna) == 11


def test_select():
    players = [
        Player(id=i, dna=(["↑"] * (11 - i) + ["↓"] * i), mutation_rate=0.0)
        for i in range(11)
    ]
    # Add a player with perfect score for testing efficacy of select.
    players.append(
        Player(
            id=11,
            dna=["↑", "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "START"],
            mutation_rate=0.0,
        )
    )
    survivors = select(players, fitness_cutoff=5)
    assert len(survivors) == 5
    assert survivors[0].score == 11


def test_crossover():
    random.seed(42)
    parents = [
        Player(id=0, dna=["↑"] * 11, mutation_rate=0.0),
        Player(id=1, dna=["↓"] * 11, mutation_rate=0.0),
    ]
    offspring = crossover(survivors=parents, size=10, mutation_rate=0.0)
    assert len(offspring) == 10
    # With 0% mutation rate, all offpsring should only have "↑" or "↓" genes.
    for child in offspring:
        assert all(gene in ["↑", "↓"] for gene in child.dna)


@pytest.mark.parametrize(
    "win_gene, win",
    [pytest.param("↑", True, id="Win"), pytest.param("↓", False, id="Lose")],
)
def test_check_winners(win_gene: str, win: bool):
    # Modify only the first gene to determine win case or lose case.
    dna = [win_gene, "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "START"]
    players = [
        Player(
            id=i,
            dna=dna,
            mutation_rate=0.0,
        )
        for i in range(10)
    ]
    assert check_winners(players, win_percent=1.0) is win
