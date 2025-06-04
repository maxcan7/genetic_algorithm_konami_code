import random

from .constants import GENES
from .constants import KONAMI_CODE
from .player import Player

type Players = list[Player]


def populate(size: int, mutation_rate: float) -> Players:
    """Create an initial population of players with random DNA.

    Args:
        size: Number of players to create
        mutation_rate: Probability of each gene mutating (0.0 to 1.0)

    Returns:
        List of Player objects with random DNA

    Raises:
        ValueError: If size is less than 1 or mutation_rate is not between 0 and 1
    """
    if size < 1:
        raise ValueError("Population size must be at least 1")
    if not 0 <= mutation_rate <= 1:
        raise ValueError("Mutation rate must be between 0 and 1")

    players = []
    for i in range(size):
        dna = [random.choice(GENES) for _ in KONAMI_CODE]
        players.append(Player(id=i, dna=dna, mutation_rate=mutation_rate))

    return players


def select(players: Players, fitness_cutoff: int) -> Players:
    """Select the top performing players based on their fitness scores.

    Args:
        players: List of players to select from
        fitness_cutoff: Number of top players to select

    Returns:
        List of selected players sorted by score in descending order

    Raises:
        ValueError: If fitness_cutoff is less than 1 or greater than number of players
    """
    if fitness_cutoff < 1:
        raise ValueError("Fitness cutoff must be at least 1")
    if fitness_cutoff > len(players):
        raise ValueError("Fitness cutoff cannot be greater than population size")

    return sorted(players, key=lambda player: player.score, reverse=True)[
        :fitness_cutoff
    ]


def crossover(survivors: Players, size: int, mutation_rate: float) -> Players:
    """Create a new generation through crossover of selected survivors.

    Args:
        survivors: List of parent players to create offspring from
        size: Number of offspring to create
        mutation_rate: Probability of each gene mutating (0.0 to 1.0)

    Returns:
        List of new Player objects created through crossover

    Raises:
        ValueError: If size is less than 1, mutation_rate is not between 0 and 1,
                   or there are fewer than 2 survivors
    """
    if size < 1:
        raise ValueError("Population size must be at least 1")
    if not 0 <= mutation_rate <= 1:
        raise ValueError("Mutation rate must be between 0 and 1")
    if len(survivors) < 2:
        raise ValueError("Need at least 2 survivors for crossover")

    n = len(KONAMI_CODE)
    id = 0
    offspring = []
    while len(offspring) < size:
        parents = random.sample(survivors, 2)
        dna = [(random.choice(parents)).dna[i] for i in range(n)]
        offspring.append(Player(id=id, dna=dna, mutation_rate=mutation_rate))
        id += 1

    return offspring


def check_winners(players: Players, win_percent: float = 0.75) -> bool:
    """Check if enough players have solved the Konami code.

    Args:
        players: List of players to check
        win_percent: Required percentage of winners (0.0 to 1.0)

    Returns:
        True if enough players have won, False otherwise

    Raises:
        ValueError: If win_percent is not between 0 and 1
    """
    if not 0 <= win_percent <= 1:
        raise ValueError("Win percentage must be between 0 and 1")

    winners = sum(1 for player in players if player.winner)
    return winners >= len(players) * win_percent
