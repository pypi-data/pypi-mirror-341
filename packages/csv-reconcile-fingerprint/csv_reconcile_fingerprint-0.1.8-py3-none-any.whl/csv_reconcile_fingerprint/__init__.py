from csv_reconcile import scorer
from .utils import fingerprint
from .utils import tokenize_fingerprint

@scorer.register
def getNormalizedFields():
    return ()


@scorer.register
def processScoreOptions(options):
    if not options:
        return

    options['stopwords'] = [w.lower() for w in options['stopwords']]


@scorer.register
def scoreMatch(left: str, right: str) -> float:
    """
    Calculate the similarity score between two strings based on their fingerprints.

    Args:
        left (str): The first string to compare.
        right (str): The second string to compare.

    Returns:
        float: A similarity score between 0 and 100.
    """
    # Check for empty inputs
    if not left or not right:
        return 0.0

    left_tokens = tokenize_fingerprint(left)
    right_tokens = tokenize_fingerprint(right)

    # Calculate Jaccard similarity
    intersection = len(left_tokens & right_tokens)
    union = len(left_tokens | right_tokens)

    # Avoid division by zero
    if union == 0:
        return 0.0

    # Calculate score as a percentage
    score = (intersection / union) * 100.0
    return score


@scorer.register
def normalizeWord(word, **scoreOptions):
    return ()