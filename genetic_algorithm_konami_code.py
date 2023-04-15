import sys
import typing as t
import random
from pprint import pprint


# The "gamepad" inputs, or "genes".
konami_code_genes = ["↑", "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "START"]


class Player:
    """
    Each Player has an id and dna. The dna are their 11 genes,
    or gampad inputs.
    """

    def __init__(self, player_id: int, dna: t.List[str], mutation_rate: float) -> None:
        self.id = player_id
        self.dna = self.mutate(dna, mutation_rate)
        self.lives = 1
        self.score = self.test_fitness()
        self.winner = True if self.dna == konami_code_genes else False

    def __repr__(self) -> str:
        return f"""
        Player_{self.id}:
        DNA: {self.dna}
        SCORE: {self.score}
        WINNER: {self.winner}
        """

    def mutate(self, dna: t.List[str], mutation_rate: float) -> t.List[str]:
        # For each gene in the dna, there is a mutation_rate % chance that the
        # gene will be replaced with any random gene from the
        # konami_code_genes list.
        for gene_idx in range(len(dna)):
            if random.randint(0, 100) <= (100 * mutation_rate):
                dna[gene_idx] = konami_code_genes[
                    random.randint(0, len(konami_code_genes) - 1)
                ]
        return dna

    def test_fitness(self) -> int:
        """
        There is probably a more efficient way to do this, but this is easy to
        conceptualize and works better for the videogame controller input
        analogy of the task.

        Each player's dna is like the controller inputs they would press for
        the Konami Code. Each correct input from left to right increases their
        score by one. If they make an error, they lose a life, and they only
        have one life, so that's their final score.
        """
        curr_gene = 0
        score = 0
        while self.lives > 0 and curr_gene < len(konami_code_genes):
            if self.dna[curr_gene] == konami_code_genes[curr_gene]:
                score += 1
                curr_gene += 1
            else:
                self.lives -= 1
        return score


def populate(size: int = 100, mutation_rate: float = 0.05) -> t.List[Player]:
    """
    Creates a population of Players with randomized dna. Each player consists
    of an id, and a dna strand of length(konami_code) of random gamepad inputs.
    """
    players = []
    dna_length = len(konami_code_genes)
    for i in range(size):
        dna = [random.randint(0, dna_length - 1) for _ in range(dna_length)]
        players.append(
            Player(
                player_id=i,
                dna=[konami_code_genes[x] for x in dna],
                mutation_rate=mutation_rate,
            )
        )
    return players


def select(players: t.List[Player], fitness_cutoff: int) -> t.List[Player]:
    """
    Sorts the players by score and takes the top <fitness_cutoff> players.
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

    The offspring can be sampled with replacement, so any two players can
    cross any number of times with any other survivors. However, parent
    sampling is without replacement, so there are no parthenogenically
    reproducing players!

    The crossover rule randomly selects a gene from each parent for that index.
    """
    offspring = []
    player_id = 0
    while len(offspring) < size:
        parents = random.sample(survivors, 2)
        dna = [parents[random.randint(0, 1)].dna[x] for x in range(len(konami_code_genes))]
        new_player = Player(player_id=player_id, dna=dna, mutation_rate=mutation_rate)
        offspring.append(new_player)
        player_id += 1
    return offspring


def check_winners(players: t.List[Player], win_percent: float = 0.75) -> bool:
    """
    Checks if the percentage of winners meets the win_percent criteria.
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
    fitness_cutoff: int = 10,
    mutation_rate: float = 0.05,
    win_percent: float = 0.75,
    max_iter: int = 10000,
) -> int:
    """
    After the initial player population is created, this runs the game.
    Fitness and gene mutation is calculated on each player automatically when
    instantiated, but then survivors are selected and a new generation of
    offspring players created via crossover.

    The game will continue to run until win_percent of the players have the
    Konami Code genes. If win_percent = 0.75, then 75% of the players must
    have Konami Code genes.

    max_iter is a failsafe, if the algorithm fails to converge within max_iter
    generations, it will break.

    If it runs successfully, it returns the number of generations to win.
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
    size = int(args.get("size", None))
    fitness_cutoff = int(args.get("fitness_cutoff", None))
    mutation_rate = float(args.get("mutation_rate", None))
    win_percent = float(args.get("win_percent", None))
    max_iter = int(args.get("max_iter", None))
    players = populate(size)
    play(players, fitness_cutoff, mutation_rate, win_percent, max_iter)
