import pytest

from player import Player


def test_player_creation():
    player = Player(
        id=1,
        dna=["↑", "↓", "←", "→", "B", "A", "START", "↑", "↓", "←", "→"],
        mutation_rate=0.0,
    )
    assert player.id == 1
    assert len(player.dna) == 11
    assert player.score >= 0


@pytest.mark.parametrize(
    "mutation_rate,should_mutate",
    [
        pytest.param(1.0, True, id="100_percent_mutation_guarantees_changes"),
        pytest.param(0.0, False, id="0_percent_mutation_guarantees_no_changes"),
    ],
)
def test_player_mutation(mutation_rate: float, should_mutate: bool):
    original_dna = ["↑", "↓", "←", "→", "B", "A", "START", "↑", "↓", "←", "→"]
    player = Player(id=1, dna=original_dna.copy(), mutation_rate=mutation_rate)
    if should_mutate:
        assert player.dna != original_dna
    else:
        assert player.dna == original_dna


@pytest.mark.parametrize(
    "dna,expected_score",
    [
        pytest.param(
            ["↑", "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "START"],
            11,
            id="perfect_match",
        ),
        pytest.param(
            ["↑", "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "B"],
            10,
            id="one_wrong_at_end",
        ),
        pytest.param(
            ["↓", "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "START"],
            0,
            id="wrong_at_start",
        ),
    ],
)
def test_player_fitness(dna: list[str], expected_score: int):
    player = Player(id=1, dna=dna, mutation_rate=0.0)
    assert player.score == expected_score


@pytest.mark.parametrize(
    "dna,is_winner",
    [
        pytest.param(
            ["↑", "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "START"],
            True,
            id="perfect_match_is_winner",
        ),
        pytest.param(
            ["↑", "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "B"],
            False,
            id="one_wrong_not_winner",
        ),
        pytest.param(
            ["↓", "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "START"],
            False,
            id="wrong_at_start_not_winner",
        ),
    ],
)
def test_player_winner_status(dna: list[str], is_winner: bool):
    player = Player(id=1, dna=dna, mutation_rate=0.0)
    assert player.winner is is_winner


@pytest.mark.parametrize(
    "invalid_input,error_message",
    [
        pytest.param(
            {"mutation_rate": 1.5},
            "Mutation rate must be between 0 and 1",
            id="invalid_mutation_rate_above_1",
        ),
        pytest.param(
            {"dna": ["↑"] * 10},
            "DNA length must be 11",
            id="invalid_dna_length_too_short",
        ),
        pytest.param(
            {"dna": ["X"] * 11},
            "All genes must be one of",
            id="invalid_gene_value",
        ),
    ],
)
def test_player_invalid_inputs(invalid_input: dict, error_message: str):
    default_input = {
        "id": 1,
        "dna": ["↑"] * 11,
        "mutation_rate": 0.0,
    }
    # Update default input with invalid input
    default_input.update(invalid_input)

    with pytest.raises(ValueError, match=error_message):
        Player(**default_input)
