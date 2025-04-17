import pytest
from csv_reconcile_fingerprint.utils import fingerprint, tokenize_fingerprint
from csv_reconcile_fingerprint import scoreMatch, processScoreOptions

def test_fingerprint():
    assert fingerprint("Tom Cruise") == "cruise tom"
    assert fingerprint("Cruise, Tom") == "cruise tom"
    assert fingerprint("") == ""
    assert fingerprint("123 Main St.") == "123 main st"