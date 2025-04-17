
import re
from unidecode import unidecode

def fingerprint(string):
    """
    Generate a fingerprint of the input string by normalizing, removing punctuation, 
    and sorting unique tokens. Based on the OpenRefine clustering implementation https://openrefine.org/docs/technical-reference/clustering-in-depth and this gist: https://gist.github.com/pietz/d6197f64c34d273a6d456d7b736c028d

    Args:
        string (str): The input string to process.

    Returns:
        str: A normalized, deduplicated, and sorted string of tokens.
    """
    # change all characters to their lowercase representation
    string = string.lower()
    # remove all punctuation and control characters
    string = re.sub("[^A-Za-z0-9 ]+", "", string)
    # normalize extended western characters to their ASCII representation
    string = unidecode(string)
    # split the string into whitespace-separated tokens
    words = string.split()
    # sort the tokens and remove duplicates
    words = sorted(list(set(words)))
    # join the tokens back together
    return " ".join(words)

def tokenize_fingerprint(value):
    """
    Tokenize the fingerprint of the input string into a set of unique tokens.

    Args:
        value (str): The input string to process.

    Returns:
        set: A set of unique tokens derived from the fingerprint of the input string.
    """
    return set(fingerprint(value).split())