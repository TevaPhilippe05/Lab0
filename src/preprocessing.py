"""Data preprocessing functions"""

import math
import random


def is_missing(value):
    """Return True if the value is a missing value"""
    if value is None or value == "" or str(value).lower() == "nan":
        return True
    return False


# Clean


def remove_missing(values):
    """Remove missing values from a list"""
    result = []
    for value in values:
        if not is_missing(value):
            result.append(value)
    return result


def fill_missing(values, fill_value=0):
    """Replace missing values of a list with fill_value"""
    result = []
    for value in values:
        if is_missing(value):
            result.append(fill_value)
        else:
            result.append(value)
    return result


def remove_duplicates(values):
    """Return unique values of a list"""
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


# Numeric


def normalize(values, new_min=0.0, new_max=1.0):
    """Normalization min-max method"""
    old_min = min(values)
    old_max = max(values)
    if old_min == old_max:
        return [new_min for _ in values]
    result = []
    for value in values:
        scaled = (value - old_min) / (old_max - old_min)
        result.append(scaled * (new_max - new_min) + new_min)
    return result


def standardize(values):
    """Standardization with the z-score method"""
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    std = math.sqrt(variance)
    if std == 0:
        return [0.0 for _ in values]
    result = []
    for value in values:
        result.append((value - mean) / std)
    return result


def clip(values, min_value, max_value):
    """Clip list of numbers to the range [min_value, max_value]"""
    result = []
    for value in values:
        if value < min_value:
            result.append(min_value)
        elif value > max_value:
            result.append(max_value)
        else:
            result.append(value)
    return result


def to_integers(values):
    """Convert list of strings to integers"""
    result = []
    for value in values:
        try:
            result.append(int(value))
        except ValueError:
            pass
    return result


def log_transform(values):
    """Apply logarithm of a list"""
    result = []
    for value in values:
        if value > 0:
            result.append(math.log(value))
    return result


# Text


def remove_punctuation(text):
    """Keep only alphanumeric characters and spaces"""
    result = ""
    for char in text:
        if char.isalnum() or char == " ":
            result += char
    return result


def tokenize(text):
    """Lowercase the text and keep only alphanumeric words"""
    clean_text = remove_punctuation(text).lower()
    words = clean_text.split()
    return " ".join(words)


def remove_stopwords(text, stopwords):
    """Lowercase the text and remove the stop-words"""
    stopwords = [word.lower() for word in stopwords]
    result = []
    for word in text.lower().split():
        if word not in stopwords:
            result.append(word)
    return " ".join(result)


# Structure


def flatten(list_of_lists):
    """Transform a list of lists into a single list"""
    result = []
    for liste in list_of_lists:
        for value in liste:
            result.append(value)
    return result


def shuffle(values, seed=None):
    """Shuffle a list of values"""
    result = list(values)
    random.Random(seed).shuffle(result)
    return result
