import sys
import typing as t
import random
from pprint import pprint


# The Konami Code 11-digit inputs.
konami_code = ["↑", "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "START"]
# The list of unique values, the 7 possible genes (gamepad inputs).
gamepad_input_genes = list(set(konami_code))


class Player:
    """
    Class instantiation of a Player.

    Inputs:
    player_id: ID number for player, mostly for visualization.
    dna: 11-digit list of genes, or gamepad inputs, from gamepad_input_genes.
    They are mutated given mutation_rate with the mutate method.
    mutation_rate: Percent chance that a gene will randomly change to any
    other possible value.

    Attributes:
    id: player_id.
    dna: DNA sequence after being passed into the mutate method along with
    mutation_rate.
    lives: Number of lives to test_fitness. 1 means they have not had their
    score evaluated yet, 0 means they've been evaluated.
    score: Output of test_fitness method. Number of correct genes from left to
    right before running out of lives, i.e. whether they pressed the correct
    gamepad inputs.
    winner: True if their dna is exactly the konami_code, else False.
    """

    def __init__(self, player_id: int, dna: t.List[str], mutation_rate: float) -> None:
        self.id = player_id
        self.dna = self.mutate(dna, mutation_rate)
        self.lives = 1
        self.score = self.test_fitness()
        self.winner = True if self.dna == konami_code else False

    def __repr__(self) -> str:
        return f"""
        Player_{self.id}:
        DNA: {self.dna}
        SCORE: {self.score}
        WINNER: {self.winner}
        """

    def mutate(self, dna: t.List[str], mutation_rate: float) -> t.List[str]:
        """
        Mutates Player dna. Each gene in the dna strand has a mutation_rate
        percent chance of mutating into any other gene in the
        gamepad_input_genes list.

        Inputs:
        dna: 11-digit list of genes, or gamepad inputs, from
        gamepad_input_genes.
        mutation_rate: Percent chance that a gene will randomly change to any
        other possible value.

        Returns:
        dna: 11-digit list of genes after mutation.
        """
        for gene_idx in range(len(dna)):
            if random.randint(0, 100) < (100 * mutation_rate):
                dna[gene_idx] = gamepad_input_genes[
                    random.randint(0, len(gamepad_input_genes) - 1)
                ]
        return dna

    def test_fitness(self) -> int:
        """
        Tests Player fitness. From left to right, the player's genes are
        compared to the konami_code. For each correct gene i.e. gamepad input,
        their score goes up by one. If they get one incorrect, they lose a
        life, and with only one life, they end the game.

        Returns:
        score: Total number of correct genes from left to right before running
        out of lives.
        """
        curr_gene = 0
        score = 0
        while self.lives > 0 and curr_gene < len(self.dna):
            if self.dna[curr_gene] == konami_code[curr_gene]:
                score += 1
                curr_gene += 1
            else:
                self.lives -= 1
        return score


def populate(size: int, mutation_rate: float) -> t.List[Player]:
    """
    Creates a playerbase of Players with randomly generated dna.

    Inputs:
    size: Population size / playerbase.
    mutation_rate: Percent chance that a gene will randomly mutate into
    another gene from the gamepad_input_genes list.

    Returns:
    players: List of Players.
    """
    players = []
    for i in range(size):
        dna = [
            random.randint(0, len(gamepad_input_genes) - 1)
            for _ in range(len(konami_code))
        ]
        players.append(
            Player(
                player_id=i,
                dna=[gamepad_input_genes[x] for x in dna],
                mutation_rate=mutation_rate,
            )
        )
    return players


def select(players: t.List[Player], fitness_cutoff: int) -> t.List[Player]:
    """
    Sorts the players by score and takes the top fitness_cutoff players.

    Inputs:
    players: List of Players.
    fitness_cutoff: Top X scoring players to be selected.

    Returns:
    survivors: List of top-scoring Players up to the fitness_cutoff.
    """
    players.sort(key=lambda x: x.score, reverse=True)
    return players[:fitness_cutoff]


def crossover(
    survivors: t.List[Player], size: int, mutation_rate: float
) -> t.List[Player]:
    """
    Creates a new generation of players by combining the survivors of the
    previous generation. For simplicity, the player population size will
    remain the same for each generation.

    Inputs:
    survivors: List of Players who met the fitness_cutoff.
    size: Size for the next generation of players.
    mutation_rate: Percent chance any gene mutates into any other gene in the
    gamepad_input_genes list.

    Returns:
    offspring: List of Players generated via crossover.
    """
    offspring = []
    player_id = 0
    while len(offspring) < size:
        parents = random.sample(survivors, 2)
        dna = [parents[random.randint(0, 1)].dna[x] for x in range(len(konami_code))]
        new_player = Player(player_id=player_id, dna=dna, mutation_rate=mutation_rate)
        offspring.append(new_player)
        player_id += 1
    return offspring


def check_winners(players: t.List[Player], win_percent: float = 0.75) -> bool:
    """
    Checks if the percentage of winners meets the win_percent criteria.

    Inputs:
    players: List of players.
    win_percent: Percent of players who must be winners in order to end the
    game.

    Returns:
    winners: bool True or False whether the win condition has been met.
    """
    winners = 0
    for player in players:
        if player.winner:
            winners += 1
    if winners >= (len(players) * win_percent):
        return True
    else:
        return False


def play(
    players: t.List[Player],
    fitness_cutoff: int,
    mutation_rate: float,
    win_percent: float,
    max_iter: int,
) -> int:
    """
    Runs the game.
    Checks for winners, and if the win condition is not met, a new generation
    will be created and tested again, and this will continue until the win
    condition is met or the max_iter is exceeded.

    Inputs:
    players: List of players for Generation 0.
    fitness_cutoff: Top X scoring players to be selected.
    mutation_rate: Percent chance that a gene will randomly change to any
    other possible value.
    win_percent: Percent of players who must be winners in order to end the
    game.
    max_iter: Maximum number of generations before quitting, even the win
    condition is not met.
    """
    generation = 0
    winners = False
    while not winners:
        print(f"Generation: {generation}")
        pprint(players)
        winners = check_winners(players, win_percent)
        if winners:
            print(f"Generation {generation} wins!")
            return
        survivors = select(players, fitness_cutoff)
        players = crossover(survivors, size, mutation_rate)
        generation += 1
        if generation > max_iter:
            print("Failed :(")
            break


if __name__ == "__main__":
    arg_names = [
        "command",
        "size",
        "fitness_cutoff",
        "mutation_rate",
        "win_percent",
        "max_iter",
    ]
    args = dict(zip(arg_names, sys.argv))
    size = int(args.get("size", 25))
    fitness_cutoff = int(args.get("fitness_cutoff", 5))
    mutation_rate = float(args.get("mutation_rate", 0.05))
    win_percent = float(args.get("win_percent", 0.75))
    max_iter = int(args.get("max_iter", 1000))
    players = populate(size, mutation_rate)
    play(players, fitness_cutoff, mutation_rate, win_percent, max_iter)
