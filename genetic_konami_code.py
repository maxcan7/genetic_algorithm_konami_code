import sys
import typing as t
import random
import copy
from pprint import pprint


konami_code_genes = ["↑", "↑", "↓", "↓", "←", "→", "←", "→", "B", "A", "START"]


class Player(t.NamedTuple):
    # TODO Make this an init function rather than named tuple and adjust
    # indices elsewhere accordingly
    player_number: int
    dna: t.List[str]


def populate(size: int = 100) -> t.List[Player]:
    """
    Create a random population of size. Each member consists of a dna strand
    of length(konami_code) of random inputs on our gamepad.
    """
    population = []
    for i in range(size):
        dna = [
            random.randint(0, len(konami_code_genes) - 1)
            for _ in range(len(konami_code_genes))
        ]
        population.append(Player(i, [konami_code_genes[x] for x in dna]))
    return population


def fit(population: t.List[Player]) -> t.Dict[str, int]:
    """
    Treat the Konami Code task like a linear walk. Probably a more efficient
    way, but this is easy to conceptualize and feels like a platformer
    videogame.
    Fitness is calculated as the number of genes corresponding to the Konami
    Code from left to right before hitting an error, like the number of steps
    taken in Mario before hitting a goomba or falling.
    Each player in the population has one life. From left to right, if the
    player's current gene corresponds to the konami code gene, their score
    goes up by one and they continue along, if the current gene does not
    correspond to the konami code, player loses a life. If they are reduced to
    0 lives or reach the end of the dna sequence, we move on to the next
    player. The population are added to a dictionary lookup table with their
    score as the value.
    """
    # TODO check_winner should be in here
    scores_table = {}
    for player in population:
        scores_table[f"player_{player[0]}"] = 0
        curr_gene = 0
        lives = 1
        while lives > 0 and curr_gene < len(konami_code_genes):
            if player[1][curr_gene] == konami_code_genes[curr_gene]:
                scores_table[f"player_{player[0]}"] += 1
                curr_gene += 1
            else:
                lives -= 1
    return scores_table


def select(
    population: t.List[Player], scores_table: t.Dict[str, int], fitness_cutoff: int
) -> t.List[Player]:
    """
    Take the top <fitness_cutoff> players by their score.
    """
    player_ranks = sorted(scores_table, key=scores_table.get, reverse=True)
    survivor_indices = \
        [int(x.replace("player_", "")) for x in player_ranks][:fitness_cutoff]
    survivors = [x for x in population if x[0] in survivor_indices]
    return survivors


def crossover(survivors: t.List[Player], size: int) -> t.List[Player]:
    """
    Create combinations from the survivors as offspring. For simplicity,
    keeping the population size the same for each generation.
    The offspring can be sampled with replacement, so any two players can
    cross any number of times.
    The crossover rule randomly selects a gene from each parent for that index.
    """
    offspring = []
    player_number = 0
    while len(offspring) < size:
        parents = random.sample(survivors, 2)
        dna = []
        for i in range(len(konami_code_genes)):
            dna.append(parents[random.randint(0, 1)][1][i])
        new_player = Player(player_number=player_number, dna=dna)
        offspring.append(new_player)
        player_number += 1
    return offspring


def mutate(offspring: t.List[Player], mutation_rate: float) -> t.List[Player]:
    # Change mutation_rate% of genes for each offspring randomly
    mutated_offspring = copy.deepcopy(offspring)
    for player_idx in range(len(mutated_offspring)):
        for gene_idx in range(len(mutated_offspring[player_idx][1])):
            if random.randint(0, 100) <= (100 * mutation_rate):
                mutated_offspring[player_idx][1][gene_idx] = konami_code_genes[
                    random.randint(0, len(konami_code_genes) - 1)
                ]
    return mutated_offspring


def play(
    population: t.List[Player], fitness_cutoff: int = 10, mutation_rate: float = 0.1
) -> t.List[Player]:
    scores_table = fit(population)
    survivors = select(population, scores_table, fitness_cutoff)
    offspring = crossover(survivors, size)
    mutated_offspring = mutate(offspring, mutation_rate)
    return mutated_offspring


def check_winners(population: t.List[Player], win_percent: float = 0.99) -> bool:
    winners = []
    for player in population:
        if player[1] == konami_code_genes:
            winners.append(player)
    if len(winners) >= (len(population)*win_percent):
        return True
    else:
        return False


if __name__ == "__main__":
    arg_names = ["command", "size", "fitness_cutoff", "mutation_rate", "win_percent"]
    args = dict(zip(arg_names, sys.argv))
    size = int(args.get("size", None))
    fitness_cutoff = int(args.get("fitness_cutoff", None))
    mutation_rate = float(args.get("mutation_rate", None))
    win_percent = float(args.get("win_percent", None))
    players = populate(size)
    winners = check_winners(players, win_percent)
    generations = 1
    # TODO Clean up how it prints, maybe nest this all in the play function,
    # add better winner handling, etc.
    while not winners:
        players = play(players, fitness_cutoff, mutation_rate)
        winners = check_winners(players)
        print(f"generation: {generations}")
        pprint(players)
        generations += 1
        if generations > 10000:
            print("Fail :(")
            break
