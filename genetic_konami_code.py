import sys
import typing as t
import random
import copy


# The "gamepad" inputs, or "genes".
konami_code_genes = ["↑", "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "START"]


class Player:
    """
    Each Player has an id and dna. The dna are their 11 genes,
    or gampad inputs.
    """
    def __init__(self, player_id: int, dna: t.List[str]) -> None:
        self.player_id = player_id
        self.dna = dna


def populate(size: int = 100) -> t.List[Player]:
    """
    Creates a population of Players with randomized dna. Each player consists
    of an id, and a dna strand of length(konami_code) of random gamepad inputs.
    """
    players = []
    dna_length = len(konami_code_genes)
    for i in range(size):
        dna = [
            random.randint(0, dna_length - 1)
            for _ in range(dna_length)
        ]
        players.append(Player(i, [konami_code_genes[x] for x in dna]))
    return players


def fit(players: t.List[Player]) -> t.Dict[str, int]:
    """
    The Konami Code task is like a linear walk. There is probably a more
    efficient way to do this, but this is easy to conceptualize and feels like
    a platformer videogame which I thought was fun.

    Fitness is calculated as the number of genes corresponding to the Konami
    Code from left to right before hitting an error, like the number of steps
    taken in Mario before hitting a goomba or falling.

    Each player in the players population has one life. From left to right, if
    the player's current gene corresponds to the Konami Code gene at that same
    step, their score goes up by one and they continue along, but if the
    current gene does not correspond to the Konami Code gene at the same step,
    the player loses a life. If they are reduced to 0 lives or reach the end
    of the dna sequence (run out of steps), we move on to the next player. The
    players are added to a dict lookup table with their score as the value.
    """
    scores_table = {}
    for player in players:
        scores_table[f"player_{player.player_id}"] = 0
        curr_gene = 0
        lives = 1
        while lives > 0 and curr_gene < len(konami_code_genes):
            if player.dna[curr_gene] == konami_code_genes[curr_gene]:
                scores_table[f"player_{player.player_id}"] += 1
                curr_gene += 1
            else:
                lives -= 1
    return scores_table


def select(
    players: t.List[Player],
    scores_table: t.Dict[str, int],
    fitness_cutoff: int
) -> t.List[Player]:
    """
    Takes the top <fitness_cutoff> players by their score. These "fit" players
    are the ones selected for crossover.
    """
    player_ranks = sorted(scores_table, key=scores_table.get, reverse=True)
    survivor_indices = [int(x.replace("player_", "")) for x in player_ranks][
        :fitness_cutoff
    ]
    survivors = [x for x in players if x.player_id in survivor_indices]
    return survivors


def crossover(survivors: t.List[Player], size: int) -> t.List[Player]:
    """
    Creates a new player population by combining the survivors into
    "offspring". For simplicity, the player population size will remain the
    same for each generation.
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
        dna = []
        for i in range(len(konami_code_genes)):
            dna.append(parents[random.randint(0, 1)].dna[i])
        new_player = Player(player_id=player_id, dna=dna)
        offspring.append(new_player)
        player_id += 1
    return offspring


def mutate(offspring: t.List[Player], mutation_rate: float) -> t.List[Player]:
    # Randomly change the genes of each offspring by mutation_rate %. If
    # mutation_rate=0.05, then ~5% of the genes of each player should be the
    # result of mutation.
    mutated_offspring = copy.deepcopy(offspring)
    for player_idx in range(len(mutated_offspring)):
        for gene_idx in range(len(mutated_offspring[player_idx].dna)):
            if random.randint(0, 100) <= (100 * mutation_rate):
                mutated_offspring[player_idx].dna[gene_idx] = \
                    konami_code_genes[
                    random.randint(0, len(konami_code_genes) - 1)
                ]
    return mutated_offspring


def play(
    players: t.List[Player],
    fitness_cutoff: int = 10,
    mutation_rate: float = 0.05,
    win_percent: float = 0.75,
    max_iter: int = 10000
) -> t.List[Player]:
    """
    After the initial player population is created, this runs the game. Scores
    are fit, survivors are selected, offspring are crossed over, and mutated.
    The game will continue to run until win_percent of the players have the
    Konami Code genes. If win_percent = 0.75, then 75% of the players must
    have Konami Code genes.
    max_iter is a failsafe, if the algorithm fails to converge within max_iter
    generations, it will break.
    """
    generation = 0
    winners = check_winners(players, win_percent)
    if winners:
        print(f"Generation: {generation}")
        return players
    while not winners:
        print(f"Generation: {generation}")
        scores_table = fit(players)
        survivors = select(players, scores_table, fitness_cutoff)
        players = crossover(survivors, size)
        players = mutate(players, mutation_rate)
        winners = check_winners(players, win_percent)
        generation += 1
        if generation > max_iter:
            print("Failed :(")
            break
    return players


def check_winners(
        players: t.List[Player],
        win_percent: float = 0.75
) -> bool:
    winners = 0
    for player in players:
        if player.dna == konami_code_genes:
            winners += 1
    if winners >= (len(players) * win_percent):
        return True
    else:
        return False


if __name__ == "__main__":
    arg_names = [
        "command",
        "size",
        "fitness_cutoff",
        "mutation_rate",
        "win_percent",
        "max_iter"
    ]
    args = dict(zip(arg_names, sys.argv))
    size = int(args.get("size", None))
    fitness_cutoff = int(args.get("fitness_cutoff", None))
    mutation_rate = float(args.get("mutation_rate", None))
    win_percent = float(args.get("win_percent", None))
    max_iter = int(args.get("max_iter", None))
    players = populate(size)
    play(players, fitness_cutoff, mutation_rate, win_percent, max_iter)
