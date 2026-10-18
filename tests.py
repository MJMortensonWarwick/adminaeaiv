import pandas as pd
import pytest

from pipeline import clean_currency, parse_timestamp, latest_status, gbp_amount


def make_rows(*rows):
    """Build a small bronze table. Each row is (txn_id, status, file_date, amount)."""
    return pd.DataFrame(rows, columns=["txn_id", "status", "file_date", "amount"])


# ---------------- worked example ----------------
def test_clean_currency_fixes_case_and_spaces():
    raw = pd.Series(["gbp", "EUR ", " usd", "GBP"])
    assert clean_currency(raw).tolist() == ["GBP", "EUR", "USD", "GBP"]

'''
COMMENTARY ON THE EXAMPLE
We can see that the raw sequence ["gbp", "EUR ", " usd", "GBP"] would fail if there
were no function as they do not match the expected output - ["GBP", "EUR", "USD", "GBP"].
We call the clean_currency function on raw and it should change it to upper case and remove the spaces.
This should mean we pass the test now.
The 'assert' commands basically means test whether the function output matches the expected output.
The test should pass
'''


# ---------------- parse_timestamp ----------------
def test_parse_iso():
    """An ISO timestamp, '2026-03-08 13:25:00', is read correctly."""
    test_stamp = '2026-03-08 13:25:00'
    assert parse_timestamp(test_stamp) == pd.Timestamp('2026-03-08 13:25:00')

def test_parse_day_first():
    """'08/03/2026 13:25' arrives from the processor. Which date is it? Decide, then assert."""
    raise NotImplementedError("write this test")



# ---------------- latest_status ----------------
def test_later_file_wins():
    """T1 is PENDING in the 5 Jan file and POSTED in the 6 Jan file. One row should remain. Which status?"""
    raise NotImplementedError("write this test")


def test_same_file_prefers_posted():
    """T1 appears as POSTED and PENDING in the SAME file (list POSTED first, on purpose). Which status wins?"""
    raise NotImplementedError("write this test")


def test_exact_duplicates_are_removed():
    """The same row arrives twice (a re-sent file). How many rows should remain?"""
    raise NotImplementedError("write this test")


def test_reversal_stays_its_own_row():
    """T1 is POSTED for 10.0. R1 is a REVERSED row for -10.0 with a different txn_id. Neither should disappear."""
    raise NotImplementedError("write this test")


# ---------------- gbp_amount (stretch - if you have time) ----------------
def test_gbp_is_unchanged():
    """10.0 GBP stays 10.0."""
    raise NotImplementedError("write this test")


def test_eur_is_converted():
    """100.0 EUR at a rate of 0.85 is worth how many GBP?"""
    raise NotImplementedError("write this test")


def test_unknown_currency_is_not_guessed():
    """5.0 JPY with no JPY rate available. What should happen, and why is guessing a rate dangerous?"""
    raise NotImplementedError("write this test")
