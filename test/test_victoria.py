import unittest
from zoneinfo import ZoneInfo
from datetime import datetime
from aemo_to_tariff.victoria import time_zone, convert, get_daily_fee

class TestVictoria(unittest.TestCase):
    def test_convert(self):
        interval_time = datetime(2023, 7, 15, 10, 0, tzinfo=ZoneInfo(time_zone()))
        tariff_code = 'VICR_TOU'
        rrp = 100.0
        expected_price = 40.0
        price = convert(interval_time, tariff_code, rrp)
        self.assertAlmostEqual(price, expected_price, places=2)

    def test_get_daily_fee(self):
        tariff_code = 'VICR_TOU'
        annual_usage = 20000
        expected_fee = 1.2
        fee = get_daily_fee(tariff_code, annual_usage)
        self.assertEqual(fee, expected_fee)
