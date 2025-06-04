import random
from dataclasses import dataclass
from dataclasses import field

from .constants import GENES
from .constants import KONAMI_CODE


@dataclass(repr=False)
class Player:
    """A player in the genetic algorithm that attempts to learn the Konami code.

    Each player has a DNA sequence representing a sequence of game controller inputs.
    The player's fitness is determined by how many correct inputs they have in sequence
    from the start of the Konami code.

    Attributes:
        id: Unique identifier for the player
        dna: List of genes representing controller inputs
        mutation_rate: Probability of each gene mutating (0.0 to 1.0)
        score: Number of correct inputs in sequence (calculated in __post_init__)
        winner: Whether the player has solved the Konami code
            (calculated in __post_init__)

    Raises:
        ValueError: If mutation_rate is not between 0 and 1, or if dna length doesn't
            match KONAMI_CODE
    """

    id: int
    dna: list[str]
    mutation_rate: float
    score: int = field(init=False)
    winner: bool = field(init=False)

    def __post_init__(self) -> None:
        """Initialize score and winner status, and apply mutations."""
        if not 0 <= self.mutation_rate <= 1:
            raise ValueError("Mutation rate must be between 0 and 1")
        if len(self.dna) != len(KONAMI_CODE):
            raise ValueError(f"DNA length must be {len(KONAMI_CODE)}")
        if not all(gene in GENES for gene in self.dna):
            raise ValueError(f"All genes must be one of: {GENES}")

        self.mutate()
        self.score = self.test_fitness()
        self.winner = self.dna == KONAMI_CODE

    def mutate(self) -> None:
        """Randomly mutate genes based on mutation_rate.

        Each gene has a probability of mutation_rate to be replaced with a random gene.
        """
        for i in range(len(self.dna)):
            mutate_chance = random.random()
            if mutate_chance < self.mutation_rate:
                self.dna[i] = random.choice(GENES)

    def test_fitness(self) -> int:
        """Calculate the player's fitness score.

        The score is the number of correct inputs in sequence from the start
        of the Konami code. The first incorrect input breaks the sequence.

        Returns:
            Number of correct inputs in sequence (0 to len(KONAMI_CODE))
        """
        score = 0
        for idx, gene in enumerate(self.dna):
            if gene != KONAMI_CODE[idx]:
                break
            score += 1
        return score

    def __repr__(self) -> str:
        """Return a string representation of the player.

        Returns:
            Formatted string showing player ID, DNA, score, and winner status
        """
        return f"""
        Player_{self.id}:
        DNA: {self.dna}
        SCORE: {self.score}
        WINNER: {self.winner}
        """
