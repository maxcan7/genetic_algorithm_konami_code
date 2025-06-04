import pytest
import pprint

from ..constants import KONAMI_CODE
from ..main import play
from ..player import Player


@pytest.mark.parametrize(
    "winner_count,total_players,win_percent,expected_print_count",
    [
        pytest.param(
            8, 10, 0.75, 3, id="80_percent_winners_meets_75_percent_threshold"  # 2 prints + 1 pprint
        ),
        pytest.param(
            7, 10, 0.75, 3, id="70_percent_winners_below_75_percent_threshold"  # 2 prints + 1 pprint
        ),
        pytest.param(
            10, 10, 0.75, 3, id="100_percent_winners_meets_75_percent_threshold"  # 2 prints + 1 pprint
        ),
    ],
)
def test_play_win_condition(
    winner_count: int,
    total_players: int,
    win_percent: float,
    expected_print_count: int,
    monkeypatch,
):
    # Create a population with specified number of winners
    players = [
        Player(
            id=i,
            dna=KONAMI_CODE,
            mutation_rate=0.0,
        )
        for i in range(winner_count)
    ]
    # Add non-winners
    players.extend(
        [
            Player(
                id=i + winner_count,
                dna=KONAMI_CODE[:-1] + ["B"],
                mutation_rate=0.0,
            )
            for i in range(total_players - winner_count)
        ]
    )

    output_calls = []
    monkeypatch.setattr("builtins.print", lambda *args: output_calls.append(("print", args)))
    monkeypatch.setattr("pprint.pprint", lambda obj: output_calls.append(("pprint", [obj])))

    play(
        players=players,
        fitness_cutoff=5,
        mutation_rate=0.05,
        win_percent=win_percent,
        max_iter=0,
        size=total_players,
    )
    assert len(output_calls) == expected_print_count


@pytest.mark.parametrize(
    "max_iter,expected_print_count",
    [
        pytest.param(2, 7, id="max_iter_reached"),  # 4 prints + 3 pprints
        pytest.param(1, 5, id="single_iteration"),  # 3 prints + 2 pprints
        pytest.param(0, 3, id="zero_iterations"),   # 2 prints + 1 pprint
    ],
)
def test_play_max_iter(max_iter: int, expected_print_count: int, monkeypatch):
    # Create a population with no winners
    players = [
        Player(
            id=i,
            dna=["↑", "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "B"],
            mutation_rate=0.0,
        )
        for i in range(10)
    ]

    output_calls = []
    monkeypatch.setattr("builtins.print", lambda *args: output_calls.append(("print", args)))
    monkeypatch.setattr("pprint.pprint", lambda obj: output_calls.append(("pprint", [obj])))

    play(
        players=players,
        fitness_cutoff=5,
        mutation_rate=0.05,
        win_percent=0.75,
        max_iter=max_iter,
        size=10,
    )
    assert len(output_calls) == expected_print_count


@pytest.mark.parametrize(
    "invalid_input,error_message",
    [
        pytest.param(
            {
                "players": [Player(id=1, dna=KONAMI_CODE, mutation_rate=0.0)],
                "fitness_cutoff": 0,
                "mutation_rate": 0.05,
                "win_percent": 0.75,
                "max_iter": 1000,
                "size": 10,
            },
            "Fitness cutoff must be at least 1",
            id="zero_fitness_cutoff",
        ),
        pytest.param(
            {
                "players": [Player(id=1, dna=KONAMI_CODE, mutation_rate=0.0)],
                "fitness_cutoff": 5,
                "mutation_rate": 1.5,
                "win_percent": 0.75,
                "max_iter": 1000,
                "size": 10,
            },
            "Mutation rate must be between 0 and 1",
            id="mutation_rate_above_1",
        ),
        pytest.param(
            {
                "players": [Player(id=1, dna=KONAMI_CODE, mutation_rate=0.0)],
                "fitness_cutoff": 5,
                "mutation_rate": 0.05,
                "win_percent": 1.5,
                "max_iter": 1000,
                "size": 10,
            },
            "Win percentage must be between 0 and 1",
            id="win_percent_above_1",
        ),
    ],
)
def test_play_invalid_parameters(invalid_input: dict, error_message: str):
    with pytest.raises(ValueError, match=error_message):
        play(**invalid_input)
