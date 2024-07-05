# aemo_to_tariff/evoenergy.py
from datetime import datetime
from pytz import timezone
from datetime import time

def time_zone():
    return 'Australia/ACT'

tariffs = {
        '015': {
            'name': 'Residential TOU Network (closed)',
            'periods': [
                ('Peak', time(7, 0), time(9, 0), 14.063),
                ('Peak', time(17, 0), time(20, 0), 14.063),
                ('Shoulder', time(9, 0), time(17, 0), 6.285),
                ('Shoulder', time(20, 0), time(22, 0), 6.285),
                ('Off-peak', time(22, 0), time(7, 0), 3.210)
            ]
        },
        '016': {
            'name': 'Residential TOU Network (closed) XMC',
            'periods': [
                ('Peak', time(7, 0), time(9, 0), 14.063),
                ('Peak', time(17, 0), time(20, 0), 14.063),
                ('Shoulder', time(9, 0), time(17, 0), 6.285),
                ('Shoulder', time(20, 0), time(22, 0), 6.285),
                ('Off-peak', time(22, 0), time(7, 0), 3.210)
            ]
        },
        '017': {
            'name': 'New Residential TOU Network',
            'periods': [
                ('Peak', time(7, 0), time(9, 0), 14.109),
                ('Peak', time(17, 0), time(21, 0), 14.109),
                ('Solar Soak', time(11, 0), time(15, 0), 1.757),
                ('Off-peak', time(21, 0), time(7, 0), 3.918),
                ('Off-peak', time(9, 0), time(11, 0), 3.918),
                ('Off-peak', time(15, 0), time(17, 0), 3.918)
            ]
        },
        '018': {
            'name': 'New Residential TOU Network XMC',
            'periods': [
                ('Peak', time(7, 0), time(9, 0), 14.109),
                ('Peak', time(17, 0), time(21, 0), 14.109),
                ('Solar Soak', time(11, 0), time(15, 0), 1.757),
                ('Off-peak', time(21, 0), time(7, 0), 3.918),
                ('Off-peak', time(9, 0), time(11, 0), 3.918),
                ('Off-peak', time(15, 0), time(17, 0), 3.918)
            ]
        }
    }

def convert(interval_datetime: datetime, tariff_code: str, rrp: float):
    """
    Convert RRP from $/MWh to c/kWh for Evoenergy.
    
    Parameters:
    - interval_time (str): The interval time.
    - tariff (str): The tariff code.
    - rrp (float): The Regional Reference Price in $/MWh.
    
    Returns:
    - float: The price in c/kWh.
    """
    interval_time = interval_datetime.astimezone(timezone(time_zone())).time()
    
    rrp_c_kwh = rrp / 10
    tariff = tariffs[tariff_code]
    
    # Find the applicable period and rate
    for period, start, end, rate in tariff['periods']:
        if start <= interval_time < end:
            total_price = rrp_c_kwh + rate
            return total_price
        
        # Handle overnight periods (e.g., 22:00 to 07:00)
        if start > end and (interval_time >= start or interval_time < end):
            total_price = rrp_c_kwh + rate
            return total_price

    # Otherwise, this terrible approximation
    slope = 1.037869032618134
    intecept = 5.586606750833143
    return rrp_c_kwh * slope + intecept    
