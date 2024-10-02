import random
from dataclasses import dataclass, field

from constants import GENES, KONAMI_CODE


@dataclass(repr=False)
class Player:

    id: int
    dna: list[str]
    score: int = field(init=False)
    winner: bool = field(init=False)
    mutation_rate: float

    def __post_init__(self):
        self.mutate()
        self.lives = 1
        self.score = self.test_fitness()
        self.winner = True if self.dna == KONAMI_CODE else False

    def mutate(self) -> None:
        for i in range(len(self.dna)):
            mutate_chance = random.random()
            if mutate_chance <= self.mutation_rate:
                self.dna[i] = random.choice(GENES)

    def test_fitness(self) -> int:
        """Checks how many equal genes in common with konami code"""
        score = 0
        for idx, gene in enumerate(self.dna):
            if gene == KONAMI_CODE[idx]:
                score += 1

        return score

    def __repr__(self) -> str:
        return f"""
        Player_{self.id}:
        DNA: {self.dna}
        SCORE: {self.score}
        WINNER: {self.winner}
        """
