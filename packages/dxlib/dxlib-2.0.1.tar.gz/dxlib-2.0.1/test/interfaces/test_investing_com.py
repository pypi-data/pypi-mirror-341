import unittest
from datetime import datetime

from dxlib.interfaces import investing_com as inv
from dxlib.history import History


class TestInvestingCom(unittest.TestCase):
    def setUp(self):
        self.api: MarketInterface = inv.InvestingCom()

    def test_history(self):
        params = {
            "symbols": "AAPL",
            "interval": "D",
            "start": datetime(2021, 1, 1),
            "end": datetime(2022, 1, 1),
        }
        result = self.api.historical(**params)
        self.assertIsInstance(result, History)
        self.assertEqual(260, len(result))
        # Check if
        self.assertEqual(["AAPL"], result.levels("security"))

    def test_multiple_symbols(self):
        params = {
            "symbols": ["AAPL", "MSFT"],
            "interval": "D",
            "start": datetime(2021, 1, 1),
            "end": datetime(2022, 1, 1),
        }
        result = self.api.historical(**params)
        self.assertIsInstance(result, History)
        self.assertEqual(504, len(result))
        # Check if
        self.assertEqual(["AAPL", "MSFT"], result.levels("security"))
