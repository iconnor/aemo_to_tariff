# test/test_convert.py
import unittest
from datetime import datetime
from aemo_to_tariff import spot_to_tariff, get_daily_fee, calculate_demand_fee

class TestTariffConversions(unittest.TestCase):

    def test_energex_tariff_6970(self):
        # Off peak
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Energex', '6900', 100, 1, 1), 14.22, 2)

        # Peak
        interval_time = datetime.strptime('2024-07-05 18:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Energex', '6970', 100, 1, 1), 16.125, 2)

        # Shoulder
        interval_time = datetime.strptime('2024-07-05 02:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Energex', '6900', 100, 1, 1), 16.422, 2)

        # With loss factor
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Energex', '6900', 200, 1.05, 1.01), 25.60, 2)

    def test_evoenergy_tariff_017(self):
        # Off peak
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Evoenergy', '017', 100, 1, 1), 11.911, 2)

        # Peak
        interval_time = datetime.strptime('2024-07-05 17:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Evoenergy', '017', 100, 1, 1), 24.263, 2)

        # Shoulder
        interval_time = datetime.strptime('2024-07-05 02:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Evoenergy', '017', 100, 1, 1), 14.072, 2)

        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Evoenergy', '017', 200), 23.595, 2)

    def test_ausgrid_tariff_EA116(self):
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Ausgrid', 'EA116', 100, 1, 1), 12.491, 2)
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Ausgrid', 'EA116', 200, 1, 1), 22.645, 2)

    def test_energex_daily_fee(self):
        self.assertAlmostEqual(get_daily_fee('Energex', '3900'), 0.556, 3)
        self.assertAlmostEqual(get_daily_fee('Energex', '6000', annual_usage=15000), 0.739, 3)
        self.assertAlmostEqual(get_daily_fee('Energex', '6000', annual_usage=30000), 1.033, 3)

    def test_energex_demand_fee(self):
        self.assertAlmostEqual(calculate_demand_fee('Energex', '3700', 5.5, 31), 51.1386, 2)
        self.assertAlmostEqual(calculate_demand_fee('Energex', '3900', 5.5, 31), 29.13845, 2)

    def test_ausgrid_daily_fee(self):
        # Placeholder test - update when Ausgrid is implemented
        self.assertEqual(get_daily_fee('Ausgrid', 'EA116'), 0.0)

    def test_ausgrid_demand_fee(self):
        # Placeholder test - update when Ausgrid is implemented
        self.assertEqual(calculate_demand_fee('Ausgrid', 'EA116', 5.5, 31), 0.0)

    def test_evoenergy_daily_fee(self):
        # Placeholder test - update when Evoenergy is implemented
        self.assertEqual(get_daily_fee('Evoenergy', '017'), 0.0)

    def test_evoenergy_demand_fee(self):
        # Placeholder test - update when Evoenergy is implemented
        self.assertEqual(calculate_demand_fee('Evoenergy', '017', 5.5, 31), 0.0)

if __name__ == '__main__':
    unittest.main()
