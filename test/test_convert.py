# test/test_convert.py

import unittest
from datetime import datetime
from aemo_to_tariff import spot_to_tariff

class TestSpotToTariff(unittest.TestCase):

    def test_energex_tariff_6970(self):
        # Off peak
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Energex', '6970', 100, 1, 1), 22.84, 2)
        
        # Peak
        interval_time = datetime.strptime('2024-07-05 17:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Energex', '6970', 100, 1, 1), 35.936, 2)
        
        #Shoulder
        interval_time = datetime.strptime('2024-07-05 02:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Energex', '6970', 100, 1, 1), 23.51, 2)
        
        # With loss factor
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Energex', '6970', 200, 1.05, 1.01), 45.26)
    
    def test_energex_tariff_017(self):
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Energex', '017', 100, 1, 1), 15.965, 2)
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Energex', '017', 200, 1, 1), 26.343, 2)
    
    def test_ausgrid_tariff_6970(self):
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Ausgrid', '6970', 100, 1, 1), 15.965, 2)
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Ausgrid', '6970', 200, 1, 1), 26.343, 2)
    
    def test_ausgrid_tariff_017(self):
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Ausgrid', '017', 100, 1, 1), 15.965, 2)
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Ausgrid', '017', 200, 1, 1), 26.343, 2)
    
    def test_evoenergy_tariff_6970(self):
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Evoenergy', '6970', 100, 1, 1), 15.965, 2)
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Evoenergy', '6970', 200, 1, 1), 26.34, 2)
    
    def test_evoenergy_tariff_017(self):
        # Off peak
        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Evoenergy', '017', 100, 1, 1), 11.757, 2)
        
        # Peak
        interval_time = datetime.strptime('2024-07-05 17:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Evoenergy', '017', 100, 1, 1), 24.109, 2)
        
        #Shoulder
        interval_time = datetime.strptime('2024-07-05 02:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Evoenergy', '017', 100, 1, 1), 13.918, 2)

        interval_time = datetime.strptime('2024-07-05 14:00+10:00', '%Y-%m-%d %H:%M%z')
        self.assertAlmostEqual(spot_to_tariff(interval_time, 'Evoenergy', '017', 200), 23.264, 2)


if __name__ == '__main__':
    unittest.main()
