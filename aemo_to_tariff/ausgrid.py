# aemo_to_tariff/ausgrid.py
from datetime import time, datetime
from pytz import timezone

def time_zone():
    return 'Australia/Sydney'

tariffs = {
        'EA010': {
            'name': 'Residential flat',
            'periods': [
                ('Anytime', time(0, 0), time(23, 59), 10.8007)
            ]
        },
        'EA025': {
            'name': 'Residential ToU',
            'periods': [
                ('Peak', time(14, 0), time(20, 0), 26.8969),
                ('Off-peak', time(20, 0), time(14, 0), 4.6503)
            ]
        },
        'EA111': {
            'name': 'Residential demand (introductory)',
            'periods': [
                ('Anytime', time(0, 0), time(23, 59), 10.7805)
            ]
        },
        'EA116': {
            'name': 'Residential demand',
            'periods': [
                ('Anytime', time(0, 0), time(23, 59), 2.3370)
            ]
        },
        'EA225': {
            'name': 'Small Business ToU',
            'periods': [
                ('Peak', time(14, 0), time(20, 0), 33.0130),
                ('Off-peak', time(20, 0), time(14, 0), 5.2507)
            ]
        }
    }

    
def convert(interval_datetime: datetime, tariff_code: str, rrp: float):
    """
    Convert RRP from $/MWh to c/kWh for Ausgrid.
    
    Parameters:
    - interval_time (str): The interval time.
    - network (str): The name of the network.
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
        if start <= interval_time < end or (start > end and (interval_time >= start or interval_time < end)):
            total_price = rrp_c_kwh + rate
            return total_price

    # Otherwise, this terrible approximation
    slope = 1.037869032618134
    intecept = 5.586606750833143
    return rrp_c_kwh * slope + intecept
