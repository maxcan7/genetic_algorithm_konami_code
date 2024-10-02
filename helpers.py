import random

from constants import GENES, KONAMI_CODE
from player import Player

type Players = list[Player]


def populate(size: int, mutation_rate: float) -> Players:
    players = []
    for i in range(size):
        dna = [random.choice(GENES) for _ in KONAMI_CODE]
        players.append(Player(id=i, dna=dna, mutation_rate=mutation_rate))

    return players


def select(players: Players, fitness_cutoff: int) -> Players:
    return sorted(players, key=lambda player: player.score, reverse=True)[
        :fitness_cutoff
    ]


def crossover(survivors: Players, size: int, mutation_rate: float):
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
    winners = 0
    for player in players:
        if player.winner:
            winners += 1
    return winners >= len(players) * win_percent
