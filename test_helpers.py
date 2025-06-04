import random

import pytest

from constants import KONAMI_CODE
from helpers import check_winners
from helpers import crossover
from helpers import populate
from helpers import select
from player import Player


@pytest.mark.parametrize(
    "size,mutation_rate",
    [
        pytest.param(10, 0.1, id="normal_population"),
        pytest.param(1, 0.0, id="minimal_population"),
        pytest.param(100, 0.5, id="large_population"),
    ],
)
def test_populate(size: int, mutation_rate: float):
    players = populate(size=size, mutation_rate=mutation_rate)
    assert len(players) == size
    for player in players:
        assert isinstance(player, Player)
        assert len(player.dna) == 11


@pytest.mark.parametrize(
    "invalid_input,error_message",
    [
        pytest.param(
            {"size": 0, "mutation_rate": 0.1},
            "Population size must be at least 1",
            id="zero_population_size",
        ),
        pytest.param(
            {"size": 10, "mutation_rate": 1.5},
            "Mutation rate must be between 0 and 1",
            id="mutation_rate_above_1",
        ),
        pytest.param(
            {"size": 10, "mutation_rate": -0.1},
            "Mutation rate must be between 0 and 1",
            id="mutation_rate_below_0",
        ),
    ],
)
def test_populate_invalid_inputs(invalid_input: dict, error_message: str):
    with pytest.raises(ValueError, match=error_message):
        populate(**invalid_input)


@pytest.mark.parametrize(
    "player_scores,fitness_cutoff,expected_top_score",
    [
        pytest.param(
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            5,
            10,
            id="ascending_scores",
        ),
        pytest.param(
            [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
            3,
            10,
            id="descending_scores",
        ),
        pytest.param(
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 11],
            1,
            11,
            id="single_winner",
        ),
    ],
)
def test_select(player_scores: list[int], fitness_cutoff: int, expected_top_score: int):
    players = [
        Player(id=i, dna=KONAMI_CODE[:score] + ["B"] * (11 - score), mutation_rate=0.0)
        for i, score in enumerate(player_scores)
    ]
    survivors = select(players, fitness_cutoff=fitness_cutoff)
    assert len(survivors) == fitness_cutoff
    assert survivors[0].score == expected_top_score


@pytest.mark.parametrize(
    "invalid_input,error_message",
    [
        pytest.param(
            {
                "players": [Player(id=1, dna=["↑"] * 11, mutation_rate=0.0)],
                "fitness_cutoff": 0,
            },
            "Fitness cutoff must be at least 1",
            id="zero_fitness_cutoff",
        ),
        pytest.param(
            {
                "players": [Player(id=1, dna=["↑"] * 11, mutation_rate=0.0)],
                "fitness_cutoff": 2,
            },
            "Fitness cutoff cannot be greater than population size",
            id="fitness_cutoff_too_large",
        ),
    ],
)
def test_select_invalid_inputs(invalid_input: dict, error_message: str):
    with pytest.raises(ValueError, match=error_message):
        select(**invalid_input)


@pytest.mark.parametrize(
    "parent_dna,size,mutation_rate,expected_genes",
    [
        pytest.param(
            [["↑"] * 11, ["↓"] * 11],
            10,
            0.0,
            ["↑", "↓"],
            id="no_mutation_binary_genes",
        ),
        pytest.param(
            [["↑"] * 11, ["↓"] * 11],
            5,
            1.0,
            None,  # With 100% mutation, any gene is possible
            id="full_mutation_any_gene",
        ),
    ],
)
def test_crossover(
    parent_dna: list[list[str]],
    size: int,
    mutation_rate: float,
    expected_genes: list[str] | None,
):
    random.seed(42)  # For reproducibility
    parents = [
        Player(id=i, dna=dna, mutation_rate=0.0) for i, dna in enumerate(parent_dna)
    ]
    offspring = crossover(survivors=parents, size=size, mutation_rate=mutation_rate)
    assert len(offspring) == size
    if expected_genes:
        for child in offspring:
            assert all(gene in expected_genes for gene in child.dna)


@pytest.mark.parametrize(
    "invalid_input,error_message",
    [
        pytest.param(
            {
                "survivors": [
                    Player(id=0, dna=["↑"] * 11, mutation_rate=0.0),
                    Player(id=1, dna=["↓"] * 11, mutation_rate=0.0),
                ],
                "size": 0,
                "mutation_rate": 0.0,
            },
            "Population size must be at least 1",
            id="zero_population_size",
        ),
        pytest.param(
            {
                "survivors": [
                    Player(id=0, dna=["↑"] * 11, mutation_rate=0.0),
                    Player(id=1, dna=["↓"] * 11, mutation_rate=0.0),
                ],
                "size": 10,
                "mutation_rate": 1.5,
            },
            "Mutation rate must be between 0 and 1",
            id="mutation_rate_above_1",
        ),
        pytest.param(
            {
                "survivors": [Player(id=0, dna=["↑"] * 11, mutation_rate=0.0)],
                "size": 10,
                "mutation_rate": 0.0,
            },
            "Need at least 2 survivors for crossover",
            id="insufficient_survivors",
        ),
    ],
)
def test_crossover_invalid_inputs(invalid_input: dict, error_message: str):
    with pytest.raises(ValueError, match=error_message):
        crossover(**invalid_input)


@pytest.mark.parametrize(
    "win_gene,win_percent,expected_result",
    [
        pytest.param("↑", 1.0, True, id="all_winners_100_percent"),
        pytest.param("↓", 1.0, False, id="all_losers_100_percent"),
        pytest.param("↑", 0.5, True, id="all_winners_50_percent"),
        pytest.param("↓", 0.5, False, id="all_losers_50_percent"),
    ],
)
def test_check_winners(win_gene: str, win_percent: float, expected_result: bool):
    dna = [win_gene, "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "START"]
    players = [
        Player(
            id=i,
            dna=dna,
            mutation_rate=0.0,
        )
        for i in range(10)
    ]
    assert check_winners(players, win_percent=win_percent) is expected_result


@pytest.mark.parametrize(
    "invalid_input,error_message",
    [
        pytest.param(
            {
                "players": [Player(id=1, dna=["↑"] * 11, mutation_rate=0.0)],
                "win_percent": 1.5,
            },
            "Win percentage must be between 0 and 1",
            id="win_percent_above_1",
        ),
        pytest.param(
            {
                "players": [Player(id=1, dna=["↑"] * 11, mutation_rate=0.0)],
                "win_percent": -0.1,
            },
            "Win percentage must be between 0 and 1",
            id="win_percent_below_0",
        ),
    ],
)
def test_check_winners_invalid_inputs(invalid_input: dict, error_message: str):
    with pytest.raises(ValueError, match=error_message):
        check_winners(**invalid_input)
