# aemo_to_tariff/energex.py
from datetime import time, datetime
from pytz import timezone

def time_zone():
    return 'Australia/Brisbane'
from datetime import time, datetime

tariffs = {
        '8400': {
            'name': 'Residential Flat',
            'periods': [
                ('Anytime', time(0, 0), time(23, 59), 9.648)
            ]
        },
        '3900': {
            'name': 'Residential Transitional Demand',
            'periods': [
                ('Anytime', time(0, 0), time(23, 59), 4.085)
            ]
        },
        '3700': {
            'name': 'Residential Demand',
            'periods': [
                ('Anytime', time(0, 0), time(23, 59), 3.320)
            ]
        },
        '6900': {
            'name': 'Residential Time of Use Energy',
            'periods': [
                ('Evening', time(16, 0), time(21, 0), 17.861),
                ('Overnight', time(21, 0), time(9, 0), 6.268),
                ('Day', time(9, 0), time(16, 0), 4.066)
            ]
        },
        '9100': {
            'name': 'Economy (Secondary)',
            'periods': [
                ('Anytime', time(0, 0), time(23, 59), 5.564)
            ]
        },
        '9000': {
            'name': 'Super Economy (Secondary)',
            'periods': [
                ('Anytime', time(0, 0), time(23, 59), 4.463)
            ]
        }
    }



def convert(interval_datetime: datetime, tariff_code: str, rrp: float):
    """
    Convert RRP from $/MWh to c/kWh for Energex.
    
    Parameters:
    - interval_time (str): The interval time.
    - tariff (str): The tariff code.
    - rrp (float): The Regional Reference Price in $/MWh.
    
    Returns:
    - float: The price in c/kWh.
    """
    interval_time = interval_datetime.astimezone(timezone(time_zone())).time()
    rrp_c_kwh = rrp / 10

    tariff_code = str(tariff_code)[:2] + '00'
    tariff = tariffs[tariff_code]
    
    # Find the applicable period and rate
    for period, start, end, rate in tariff['periods']:
        if start <= interval_time < end:
            total_price = rrp_c_kwh + rate
            return total_price
        
        # Handle overnight periods
        if start > end and (interval_time >= start or interval_time < end):
            total_price = rrp_c_kwh + rate
            return total_price
    
    # Terrible approximation
    slope = 1.037869032618134
    intecept = 5.586606750833143
    return rrp_c_kwh * slope + intecept
