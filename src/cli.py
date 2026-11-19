"""Command line for preprocessing functions."""

import json
import click
from src import preprocessing


@click.group()
def cli():
    """Data preprocessing tools."""


# G1: clean


@cli.group()
def clean():
    """Commands to clean data"""


@clean.command()
@click.argument("values", nargs=-1)
def remove_missing(values):
    """Remove missing values from a list.

    Example: uv run python -m src.cli clean remove-missing 1 "" nan 3
    """
    result = preprocessing.remove_missing(list(values))
    click.echo(result)


@clean.command()
@click.argument("values", nargs=-1)
@click.option("--fill-value", default="0", help="Value used to replace missing values.")
def fill_missing(values, fill_value):
    """Replace missing values of a list with fill_value

    Example: uv run python -m src.cli clean fill-missing 1 "" 3 --fill-value 0
    """
    result = preprocessing.fill_missing(list(values), fill_value)
    click.echo(result)


# G2: numeric


@cli.group()
def numeric():
    """Commands to deal with numerical values."""


@numeric.command()
@click.argument("values", nargs=-1, type=float)
@click.option("--new-min", default=0.0, type=float, help="Minimum of the new range.")
@click.option("--new-max", default=1.0, type=float, help="Maximum of the new range.")
def normalize(values, new_min, new_max):
    """Normalization min-max method

    Example: uv run python -m src.cli numeric normalize 0 5 10 --new-min 0 --new-max 1
    """
    result = preprocessing.normalize(list(values), new_min, new_max)
    click.echo(result)


@numeric.command()
@click.argument("values", nargs=-1, type=float)
def standardize(values):
    """Standardization with the z-score method

    Example: uv run python -m src.cli numeric standardize 1 2 3
    """
    result = preprocessing.standardize(list(values))
    click.echo(result)


@numeric.command()
@click.argument("values", nargs=-1, type=float)
@click.option("--min-value", default=0.0, type=float, help="Minimum value to clip.")
@click.option("--max-value", default=1.0, type=float, help="Maximum value to clip.")
def clip(values, min_value, max_value):
    """Clip list of numbers to the range [min_value, max_value]

    Example: uv run python -m src.cli numeric clip -- -3 0.5 8
    """
    result = preprocessing.clip(list(values), min_value, max_value)
    click.echo(result)


@numeric.command()
@click.argument("values", nargs=-1)
def to_integers(values):
    """Convert list of strings to integers

    Example: uv run python -m src.cli numeric to-integers 1 abc 3
    """
    result = preprocessing.to_integers(list(values))
    click.echo(result)


@numeric.command()
@click.argument("values", nargs=-1, type=float)
def log_transform(values):
    """Apply logarithm of a list

    Example: uv run python -m src.cli numeric log-transform 1 10 100
    """
    result = preprocessing.log_transform(list(values))
    click.echo(result)


# Group 3: text


@cli.group()
def text():
    """Commands to deal with text."""


@text.command()
@click.argument("text_input")
def tokenize(text_input):
    """Lowercase the text and keep only alphanumeric words

    Example: uv run python -m src.cli text tokenize "Hello, World!"
    """
    result = preprocessing.tokenize(text_input)
    click.echo(result)


@text.command()
@click.argument("text_input")
def remove_punctuation(text_input):
    """Keep only alphanumeric characters and spaces

    Example: uv run python -m src.cli text remove-punctuation "Hello, World!"
    """
    result = preprocessing.remove_punctuation(text_input)
    click.echo(result)


@text.command()
@click.argument("text_input")
@click.option(
    "--stopwords", multiple=True, help="A stop-word to remove (can be repeated)."
)
def remove_stopwords(text_input, stopwords):
    """Lowercase the text and remove the stop-words

    Example: uv run python -m src.cli text remove-stopwords "The cat" --stopwords the
    """
    result = preprocessing.remove_stopwords(text_input, list(stopwords))
    click.echo(result)


# Group 4: struct


@cli.group()
def struct():
    """Commands related to the structure of data."""


@struct.command()
@click.argument("values", nargs=-1)
@click.option(
    "--seed", default=None, type=int, help="Seed to get the same shuffle every time."
)
def shuffle(values, seed):
    """Shuffle a list of values

    Example: uv run python -m src.cli struct shuffle 1 2 3 4 --seed 42
    """
    result = preprocessing.shuffle(list(values), seed)
    click.echo(result)


@struct.command()
@click.argument("list_of_lists")
def flatten(list_of_lists):
    """Transform a list of lists into a single list

    Example: uv run python -m src.cli struct flatten "[[1, 2], [3]]"
    """
    data = json.loads(list_of_lists)
    result = preprocessing.flatten(data)
    click.echo(result)


@struct.command()
@click.argument("values", nargs=-1)
def unique(values):
    """Return unique values of a list

    Example: uv run python -m src.cli struct unique 1 1 2 3 3
    """
    result = preprocessing.remove_duplicates(list(values))
    click.echo(result)


if __name__ == "__main__":
    cli()
