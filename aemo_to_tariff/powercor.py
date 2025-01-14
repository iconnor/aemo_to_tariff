# aemo_to_tariff/powercor.py
from datetime import datetime
from zoneinfo import ZoneInfo
from datetime import time

def time_zone():
    return 'Australia/Melbourne'


tariffs = {
    'D1': {
        'name': 'Residential Single Rate',
        'periods': [
            ('Anytime', time(0, 0), time(23, 59), 9.6700)
        ]
    },
    'PRTOU': {
        'name': 'Residential TOU',
        'periods': [
            ('Off-peak', time(0, 0), time(16, 0), 4.8700),
            ('Peak', time(16, 0), time(21, 0), 18.3400),
            ('Off-peak', time(21, 0), time(23, 59), 4.8700),
        ]
    }
}

def get_daily_fee(tariff_code: str):
    return 39.7300

def get_periods(tariff_code: str):
    tariff = tariffs.get(tariff_code)
    if not tariff:
        raise ValueError(f"Unknown tariff code: {tariff_code}")

    return tariff['periods']

def convert(interval_datetime: datetime, tariff_code: str, rrp: float):
    """
    Convert RRP from $/MWh to c/kWh for Powercor.

    Parameters:
    - interval_time (str): The interval time.
    - tariff (str): The tariff code.
    - rrp (float): The Regional Reference Price in $/MWh.

    Returns:
    - float: The price in c/kWh.
    """
    interval_time = interval_datetime.astimezone(ZoneInfo(time_zone())).time()

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
    intercept = 5.586606750833143
    return rrp_c_kwh * slope + intercept
