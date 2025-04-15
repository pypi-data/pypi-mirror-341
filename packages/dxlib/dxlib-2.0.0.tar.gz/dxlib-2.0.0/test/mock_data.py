import pandas as pd

from dxlib import HistorySchema


class Mock:
    columns = ["open", "close"]
    stocks = ["AAPL", "MSFT", "GOOG", "AMZN", "FB"]

    schema = HistorySchema(
        index={"security": str, "date": pd.Timestamp},
        columns={"open": float, "close": float},
    )

    tight_data = {
        "index": [
            ("AAPL", "2021-01-01"),
            ("MSFT", "2021-01-01"),
            ("AAPL", "2021-01-02"),
            ("MSFT", "2021-01-02"),
            ("GOOG", "2021-01-03"),
            ("AMZN", "2021-01-03"),
            ("FB", "2021-01-04"),
        ],
        "columns": ["open"],
        "data": [[100], [200], [101], [201], [102], [202], [103]],
        "index_names": ["security", "date"],
        "column_names": [""],
    }

    small_data = {
        "index": [
            ("TSLA", "2021-01-01"),
            ("MSFT", "2021-01-01"),
        ],
        "columns": ["open"],
        "data": [[100], [200]],
        "index_names": ["security", "date"],
        "column_names": [""]
    }

    large_data = {
        "index": [
            ("AAPL", "2021-01-01"),
            ("MSFT", "2021-01-01"),
            ("AAPL", "2021-01-02"),
            ("MSFT", "2021-01-02"),
            ("GOOG", "2021-01-03"),
            ("AMZN", "2021-01-03"),
            ("FB", "2021-01-04"),
            ("AAPL", "2021-01-05"),
            ("MSFT", "2021-01-05"),
            ("GOOG", "2021-01-06"),
            ("AMZN", "2021-01-06"),
            ("FB", "2021-01-07"),
            ("AAPL", "2021-01-08"),
            ("MSFT", "2021-01-08"),
            ("GOOG", "2021-01-09"),
            ("AMZN", "2021-01-09"),
            ("FB", "2021-01-10"),
        ],
        "columns": ["open", "volume"],
        "data": [
            [100, 1000],
            [200, 2000],
            [101, 1001],
            [201, 2001],
            [102, 1002],
            [202, 2002],
            [103, 1003],
            [203, 2003],
            [104, 1004],
            [204, 2004],
            [105, 1005],
            [205, 2005],
            [106, 1006],
            [206, 2006],
            [107, 1007],
            [207, 2007],
            [108, 1008],
        ],
        "index_names": ["security", "date"],
        "column_names": [""],
    }
