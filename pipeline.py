"""The above magic function ("%%writefile") means we are creating a .py script in this cell"""

"""Small, pure functions for the card-spend pipeline (silver layer)."""
import pandas as pd

# Later statuses outrank earlier ones when two rows share a file date.
RANK = {"PENDING": 0, "POSTED": 1, "REVERSED": 2}


def clean_currency(series):
    """
    Strip spaces and upper-case currency codes.
    INPUT: a Series of data
    OUTPUT: Returns a new Series.
    """
    return series.str.strip().str.upper()


def parse_timestamp(text):
    """
    Read a processor timestamp. Two formats arrive:
    ISO 'YYYY-MM-DD HH:MM:SS' and day-first 'DD/MM/YYYY HH:MM' (contains a '/').
    Anything else raises ValueError.
    INPUT: A date value as string
    OUTPUT: A date value as datetime (or an error)
    """
    fmt = "%d/%m/%Y %H:%M" if "/" in text else "%Y-%m-%d %H:%M:%S"
    return pd.to_datetime(text, format=fmt)


def latest_status(df):
    """
    Return one row per txn_id: the row from the latest file_date.
    If two rows share a file_date, the higher-ranked status wins (see RANK).
    Exact duplicate rows are removed first. The input is not changed.
    INPUT: A dataframe
    OUTPUT: A modified dataframe
    """
    d = df.drop_duplicates().copy()
    d["_rank"] = d["status"].map(RANK)
    d = d.sort_values(["txn_id", "file_date", "_rank"])
    return d.groupby("txn_id").tail(1).drop(columns="_rank").reset_index(drop=True)


def gbp_amount(amount, currency, rates):
    """
    Convert an amount to GBP. `rates` maps currency -> GBP value of one unit.
    GBP is returned unchanged. An unknown currency raises KeyError (it is never guessed).
    INPUT: Amount, currency, rates
    OUTPUT: Amount in GBP
    """
    if currency == "GBP":
        return amount
    return amount * rates[currency]


def build_silver(bronze):
    """
    Bronze transactions -> silver: duplicates removed, codes cleaned, timestamps parsed, latest status kept.
    INPUT: A dataframe (bronze)
    OUTPUT: A modified dataframe (silver)
    """
    d = bronze.drop_duplicates().copy()
    d["currency"] = clean_currency(d["currency"])
    d["ts"] = d["txn_timestamp"].map(parse_timestamp)
    return latest_status(d)
