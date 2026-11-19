"""Integration tests"""

import pytest
from click.testing import CliRunner
from src.cli import cli

# Fixture

@pytest.fixture
def runner():
    """Return a CliRunner shared by all the tests"""
    return CliRunner()

# G1: clean

def test_remove_missing(runner):
    """Test the command clean remove-missing"""
    result = runner.invoke(cli, ["clean", "remove-missing", "1", "", "nan", "3"])
    assert result.exit_code == 0
    assert result.output.strip() == "['1', '3']"

def test_fill_missing(runner):
    """Test the command clean fill-missing with the default value 0"""
    result = runner.invoke(cli, ["clean", "fill-missing", "1", "", "3"])
    assert result.exit_code == 0
    assert result.output.strip() == "['1', '0', '3']"

def test_fill_missing_fill_value(runner):
    """Test the command clean fill-missing with the option --fill-value"""
    result = runner.invoke(
        cli, ["clean", "fill-missing", "1", "", "3", "--fill-value", "x"]
    )
    assert result.exit_code == 0
    assert result.output.strip() == "['1', 'x', '3']"

# G2: numeric

def test_normalize(runner):
    """Test the command numeric normalize with the default range"""
    result = runner.invoke(cli, ["numeric", "normalize", "0", "5", "10"])
    assert result.exit_code == 0
    assert result.output.strip() == "[0.0, 0.5, 1.0]"

def test_normalize_options(runner):
    """Test the command numeric normalize with --new-min and --new-max"""
    result = runner.invoke(
        cli,
        ["numeric", "normalize", "0", "5", "10", "--new-min", "0", "--new-max", "100"],
    )
    assert result.exit_code == 0
    assert result.output.strip() == "[0.0, 50.0, 100.0]"

def test_standardize(runner):
    """Test the command numeric standardize"""
    result = runner.invoke(cli, ["numeric", "standardize", "2", "2", "2"])
    assert result.exit_code == 0
    assert result.output.strip() == "[0.0, 0.0, 0.0]"

def test_clip(runner):
    """Test the command numeric clip with the default range [0, 1]"""
    result = runner.invoke(cli, ["numeric", "clip", "--", "-3", "0.5", "8"])
    assert result.exit_code == 0
    assert result.output.strip() == "[0.0, 0.5, 1.0]"

def test_clip_options(runner):
    """Test the command numeric clip with --min-value and --max-value"""
    result = runner.invoke(
        cli, ["numeric", "clip", "1", "5", "9", "--min-value", "2", "--max-value", "8"]
    )
    assert result.exit_code == 0
    assert result.output.strip() == "[2.0, 5.0, 8.0]"


def test_to_integers(runner):
    """Test the command numeric to-integers"""
    result = runner.invoke(cli, ["numeric", "to-integers", "1", "abc", "3"])
    assert result.exit_code == 0
    assert result.output.strip() == "[1, 3]"

def test_log_transform(runner):
    """Test the command numeric log-transform"""
    result = runner.invoke(cli, ["numeric", "log-transform", "--", "1", "-5"])
    assert result.exit_code == 0
    assert result.output.strip() == "[0.0]"

# Group 3: text

def test_tokenize(runner):
    """Test the command text tokenize"""
    result = runner.invoke(cli, ["text", "tokenize", "Hello, World!"])
    assert result.exit_code == 0
    assert result.output.strip() == "hello world"

def test_remove_punctuation(runner):
    """Test the command text remove-punctuation"""
    result = runner.invoke(cli, ["text", "remove-punctuation", "Hello, World!"])
    assert result.exit_code == 0
    assert result.output.strip() == "Hello World"

def test_remove_stopwords(runner):
    """Test the command text remove-stopwords with two stop-words"""
    result = runner.invoke(
        cli,
        [
            "text",
            "remove-stopwords",
            "The cat is here",
            "--stopwords",
            "the",
            "--stopwords",
            "is",
        ],
    )
    assert result.exit_code == 0
    assert result.output.strip() == "cat here"

# Group 4: struct

def test_shuffle(runner):
    """Test the command struct shuffle: same seed gives the same result"""
    first = runner.invoke(
        cli, ["struct", "shuffle", "1", "2", "3", "4", "--seed", "42"]
    )
    second = runner.invoke(
        cli, ["struct", "shuffle", "1", "2", "3", "4", "--seed", "42"]
    )
    assert first.exit_code == 0
    assert first.output == second.output

def test_flatten(runner):
    """Test the command struct flatten"""
    result = runner.invoke(cli, ["struct", "flatten", "[[1, 2], [3]]"])
    assert result.exit_code == 0
    assert result.output.strip() == "[1, 2, 3]"

def test_unique(runner):
    """Test the command struct unique"""
    result = runner.invoke(cli, ["struct", "unique", "1", "1", "2"])
    assert result.exit_code == 0
    assert result.output.strip() == "['1', '2']"

def test_help(runner):
    """Test that the four groups appear in the help of cli"""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    for group in ["clean", "numeric", "text", "struct"]:
        assert group in result.output