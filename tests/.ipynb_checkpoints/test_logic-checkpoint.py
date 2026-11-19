"""Unit tests for the data preprocessing functions"""

import math
import pytest
from src import preprocessing

# Fixtures

@pytest.fixture
def numbers():
    """Return a list of numbers used in several tests"""
    return [1.0, 2.0, 3.0, 4.0, 5.0]

@pytest.fixture
def values_with_missing():
    """Return a list with missing values (None, '' and nan)"""
    return [1, None, 2, "", 3, float("nan")]

# Clean

def test_is_missing():
    """Test that None, '' and nan are missing values and 0 is not"""
    assert preprocessing.is_missing(None)
    assert preprocessing.is_missing("")
    assert preprocessing.is_missing(float("nan"))
    assert preprocessing.is_missing("NaN")
    assert not preprocessing.is_missing(0)

def test_remove_missing(values_with_missing):
    """Test that missing values are removed from a list"""
    assert preprocessing.remove_missing(values_with_missing) == [1, 2, 3]

def test_fill_missing_default(values_with_missing):
    """Test that missing values are replaced with 0 by default"""
    assert preprocessing.fill_missing(values_with_missing) == [1, 0, 2, 0, 3, 0]

def test_fill_missing_fill_value(values_with_missing):
    """Test that missing values are replaced with fill_value"""
    result = preprocessing.fill_missing(values_with_missing, fill_value=-1)
    assert result == [1, -1, 2, -1, 3, -1]

# Parametrize on a function without options
@pytest.mark.parametrize(
    "values, expected",
    [
        ([1, 1, 2, 3, 3], [1, 2, 3]),
        (["a", "b", "a"], ["a", "b"]),
        ([], []),
    ],
)
def test_remove_duplicates(values, expected):
    """Test that only unique values are returned, in the same order"""
    assert preprocessing.remove_duplicates(values) == expected

# Numeric

def test_normalize_default(numbers):
    """Test the min-max normalization with the default range [0, 1]"""
    assert preprocessing.normalize(numbers) == [0.0, 0.25, 0.5, 0.75, 1.0]

# Parametrize on a function with options
@pytest.mark.parametrize(
    "new_min, new_max, expected",
    [
        (0.0, 1.0, [0.0, 0.25, 0.5, 0.75, 1.0]),
        (0.0, 10.0, [0.0, 2.5, 5.0, 7.5, 10.0]),
        (-1.0, 1.0, [-1.0, -0.5, 0.0, 0.5, 1.0]),
    ],
)
def test_normalize_new_range(numbers, new_min, new_max, expected):
    """Test the min-max normalization with different new_min and new_max"""
    assert preprocessing.normalize(numbers, new_min, new_max) == expected

def test_normalize_same_values():
    """Test that equal values all become new_min"""
    assert preprocessing.normalize([3, 3, 3]) == [0.0, 0.0, 0.0]

def test_standardize(numbers):
    """Test that the z-score gives a mean of 0 and a standard deviation of 1"""
    result = preprocessing.standardize(numbers)
    mean = sum(result) / len(result)
    std = math.sqrt(sum((value - mean) ** 2 for value in result) / len(result))
    assert mean == pytest.approx(0.0)
    assert std == pytest.approx(1.0)

def test_standardize_same_values():
    """Test that equal values all become 0"""
    assert preprocessing.standardize([2, 2, 2]) == [0.0, 0.0, 0.0]

@pytest.mark.parametrize(
    "min_value, max_value, expected",
    [
        (2.0, 4.0, [2.0, 2.0, 3.0, 4.0, 4.0]),
        (0.0, 10.0, [1.0, 2.0, 3.0, 4.0, 5.0]),
    ],
)
def test_clip(numbers, min_value, max_value, expected):
    """Test that numbers are clipped to the range [min_value, max_value]"""
    assert preprocessing.clip(numbers, min_value, max_value) == expected

def test_to_integers():
    """Test that strings are converted to integers and the others are removed"""
    assert preprocessing.to_integers(["1", "abc", "3", "2.5"]) == [1, 3]

def test_log_transform():
    """Test the logarithm of a list, keeping only positive numbers"""
    result = preprocessing.log_transform([1, math.e, -2, 0])
    assert result == pytest.approx([0.0, 1.0])

# Text

def test_remove_punctuation():
    """Test that only alphanumeric characters and spaces are kept"""
    assert preprocessing.remove_punctuation("Hello, World! 2024") == "Hello World 2024"

def test_tokenize():
    """Test that the text is lowercased with only alphanumeric words"""
    assert preprocessing.tokenize("Hello,   WORLD!") == "hello world"

def test_remove_stopwords():
    """Test that the text is lowercased and the stop-words are removed"""
    result = preprocessing.remove_stopwords("The Cat is HERE", ["the", "IS"])
    assert result == "cat here"

# Structure

def test_flatten():
    """Test that a list of lists becomes a single list"""
    assert preprocessing.flatten([[1, 2], [3], []]) == [1, 2, 3]

def test_shuffle_same_seed(numbers):
    """Test that the same seed gives the same shuffle"""
    first = preprocessing.shuffle(numbers, seed=42)
    second = preprocessing.shuffle(numbers, seed=42)
    assert first == second

def test_shuffle_keeps_values(numbers):
    """Test that shuffling a list does not add or remove values"""
    assert sorted(preprocessing.shuffle(numbers, seed=1)) == numbers