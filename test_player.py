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


def test_player_mutate():
    # 100% mutation rate guarantees changes.
    player = Player(id=1, dna=["↑"] * 11, mutation_rate=1.0)
    assert player.dna != ["↑"] * 11


def test_player_test_fitness():
    # 0% mutation rate and already solved dna.
    player = Player(
        id=1,
        dna=["↑", "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "START"],
        mutation_rate=0.0,
    )
    assert player.score == 11
