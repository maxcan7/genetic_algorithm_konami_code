from parser import parser
from pprint import pprint

from helpers import Players, check_winners, crossover, populate, select


def play(
    players: Players,
    fitness_cutoff: int,
    mutation_rate: float,
    win_percent: float,
    max_iter: int,
    size: int,
) -> None:
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
    args = parser.parse_args()

    players = populate(args.size, args.mutation_rate)
    play(
        players,
        args.fitness_cutoff,
        args.mutation_rate,
        args.win_percent,
        args.max_iter,
        args.size,
    )
