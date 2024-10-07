import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--size", type=int, help="Sets players amount", default=25)

parser.add_argument(
    "-f",
    "--fitness-cutoff",
    type=int,
    default=5,
    help="Sets the fitness_cutoff for the players",
)

parser.add_argument(
    "-mr",
    "--mutation-rate",
    type=float,
    default=0.05,
    help="Sets the mutation rate for the dna",
)

parser.add_argument(
    "-wp", "--win-percent", type=float, default=0.75, help="Sets the win_percent"
)

parser.add_argument(
    "-mi", "--max-iter", type=int, default=1000, help="Sets the max_iter for the game"
)
