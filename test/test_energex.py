import unittest
from datetime import datetime
from zoneinfo import ZoneInfo
import aemo_to_tariff.energex as energex

class TestEnergex(unittest.TestCase):
    def test_convert(self):
        interval_time = datetime(2023, 7, 15, 10, 0, tzinfo=ZoneInfo('Australia/Brisbane'))
        tariff_code = '6900'
        rrp = 100.0
        expected_price = 14.065
        price = energex.convert(interval_time, tariff_code, rrp)
        self.assertAlmostEqual(price, expected_price, places=2)

    def test_get_daily_fee(self):
        tariff_code = '6900'
        annual_usage = 20000
        expected_fee = 0.556
        fee = energex.get_daily_fee(tariff_code, annual_usage)
        self.assertEqual(fee, expected_fee)
