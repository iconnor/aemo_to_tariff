# aemo_to_tariff/sapower.py
from datetime import time, datetime
from pytz import timezone

def time_zone():
    return 'Australia/Adelaide'


tariffs = {
    'RSR': {
        'name': 'Residential Single Rate',
        'periods': [
            ('Anytime', time(0, 0), time(23, 59), 0.1504)
        ]
    },
    'RTOU': {
        'name': 'Residential Time of Use',
        'periods': [
            ('Peak', time(14, 0), time(20, 0), 0.1879),
            ('Off-peak', time(20, 0), time(14, 0), 0.0756),
            ('Solar Sponge', time(10, 0), time(15, 0), 0.0381)
        ]
    },
    'RPRO': {
        'name': 'Residential Prosumer',
        'periods': [
            ('Peak', time(14, 0), time(20, 0), 0.1879),
            ('Off-peak', time(20, 0), time(14, 0), 0.0756),
            ('Solar Sponge', time(10, 0), time(15, 0), 0.0381)
        ]
    },
    'RELE': {
        'name': 'Residential Electrify',
        'periods': [
            ('Peak', time(14, 0), time(20, 0), 0.3309),
            ('Off-peak', time(20, 0), time(14, 0), 0.0978),
            ('Solar Sponge', time(10, 0), time(15, 0), 0.0301)
        ]
    },
    'SBTOU': {
        'name': 'Small Business Time of Use',
        'periods': [
            ('Peak', time(7, 0), time(21, 0), 0.2568),
            ('Off-peak', time(21, 0), time(7, 0), 0.0969)
        ]
    },
    'SBTOUE': {
        'name': 'Small Business Time of Use Electrify',
        'periods': [
            ('Peak', time(7, 0), time(21, 0), 0.3257),
            ('Off-peak', time(21, 0), time(7, 0), 0.0960)
        ]
    }
}

daily_fees = {
    'RSR': 0.5753,
    'RTOU': 0.5753,
    'RPRO': 0.5753,
    'RELE': 0.5753,
    'SBTOU': 0.7259,
    'SBTOUE': 0.7259
}

demand_charges = {
    'RPRO': 0.8339,  # $/kW/day
    'SBTOUD': 0.0842  # $/kW/day
}

def convert(interval_datetime: datetime, tariff_code: str, rrp: float):
    """
    Convert RRP from $/MWh to c/kWh for SA Power Networks.

    Parameters:
    - interval_datetime (datetime): The interval datetime.
    - tariff_code (str): The tariff code.
    - rrp (float): The Regional Reference Price in $/MWh.

    Returns:
    - float: The price in c/kWh.
    """
    interval_time = interval_datetime.astimezone(timezone(time_zone())).time()
    rrp_c_kwh = rrp / 10

    tariff = tariffs.get(tariff_code)

    if not tariff:
        # Handle unknown tariff codes
        slope = 1.037869032618134
        intercept = 5.586606750833143
        return rrp_c_kwh * slope + intercept

    # Find the applicable period and rate
    for period, start, end, rate in tariff['periods']:
        if start <= interval_time < end or (start > end and (interval_time >= start or interval_time < end)):
            total_price = rrp_c_kwh + rate
            return total_price

    # If no period is found, use the first rate as default
    return rrp_c_kwh + tariff['periods'][0][3]

def get_daily_fee(tariff_code: str):
    """
    Get the daily fee for a given tariff code.

    Parameters:
    - tariff_code (str): The tariff code.

    Returns:
    - float: The daily fee in dollars.
    """
    return daily_fees.get(tariff_code, 0.0)

def calculate_demand_fee(tariff_code: str, demand_kw: float, days: int = 30):
    """
    Calculate the demand fee for a given tariff code, demand amount, and time period.

    Parameters:
    - tariff_code (str): The tariff code.
    - demand_kw (float): The maximum demand in kW.
    - days (int): The number of days for the billing period (default is 30).

    Returns:
    - float: The demand fee in dollars.
    """
    daily_charge = demand_charges.get(tariff_code, 0.0)
    return daily_charge * demand_kw * days
