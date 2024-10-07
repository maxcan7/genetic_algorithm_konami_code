import argparse
import sys

import pytest

from parser import parser


def assertValues(
    args: argparse.Namespace,
    size: int,
    fitness_cutoff: int,
    mutation_rate: float,
    win_percent: float,
    max_iter: int,
) -> None:

    assert isinstance(args.size, int)
    assert isinstance(args.fitness_cutoff, int)
    assert isinstance(args.mutation_rate, float)
    assert isinstance(args.win_percent, float)
    assert isinstance(args.max_iter, int)

    assert args.size == size
    assert args.fitness_cutoff == fitness_cutoff
    assert args.mutation_rate == mutation_rate
    assert args.win_percent == win_percent
    assert args.max_iter == max_iter


def test_default_arguments():

    sys.argv = ["a.py"]
    args = parser.parse_args()

    assertValues(args, 25, 5, 0.05, 0.75, 1000)


def test_custom_arguments():
    sys.argv = [
        "a.py",
        "-s",
        "50",
        "-f",
        "10",
        "-mr",
        ".1",
        "-wp",
        "0.8",
        "-mi",
        "500",
    ]

    args = parser.parse_args()

    assertValues(args, 50, 10, 0.1, 0.8, 500)


def test_wrong_argument_type(capsys):
    sys.argv = [".py", "--size", "abc"]

    with pytest.raises(SystemExit):
        parser.parse_args()
    captured = capsys.readouterr()
    assert "invalid int value: 'abc'" in captured.err
    assert "error:" in captured.err
