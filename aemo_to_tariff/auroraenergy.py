# aemo_to_tariff/auroraenergy.py
from datetime import time, datetime
from pytz import timezone

def time_zone():
    return 'Australia/Hobart'


tariffs = {
    '93': {
        'name': 'Residential Time-of-use',
        'periods': [
            ('Peak', time(7, 0), time(10, 0), 35.8366),
            ('Peak', time(16, 0), time(21, 0), 35.8366),
            ('Off-peak', time(0, 0), time(7, 0), 16.6862),
            ('Off-peak', time(10, 0), time(16, 0), 16.6862),
            ('Off-peak', time(21, 0), time(23, 59), 16.6862),
        ]
    },
    '94': {
        'name': 'Business Time of Use',
        'periods': [
            ('Peak', time(7, 0), time(22, 0), 29.9482),
            ('Shoulder', time(7, 0), time(22, 0), 21.6461),
            ('Off-peak', time(22, 0), time(7, 0), 12.6613),
        ]
    },
    '75': {
        'name': 'Irrigation Time of Use',
        'periods': [
            ('Peak', time(7, 0), time(22, 0), 33.3501),
            ('Shoulder', time(7, 0), time(22, 0), 24.2859),
            ('Off-peak', time(22, 0), time(7, 0), 15.1754),
        ]
    },
    '31': {
        'name': 'Residential light and power',
        'periods': [
            ('Anytime', time(0, 0), time(23, 59), 29.6477),
        ]
    },
    '22': {
        'name': 'General Use',
        'periods': [
            ('First 500 kWh', time(0, 0), time(23, 59), 36.3932),
            ('Remainder', time(0, 0), time(23, 59), 26.9229),
        ]
    },
    '82': {
        'name': 'Monthly kVA demand low voltage',
        'periods': [
            ('Anytime', time(0, 0), time(23, 59), 17.6438),
        ]
    }
}

def is_winter(date):
    return 4 <= date.month <= 9

def convert(interval_datetime: datetime, tariff_code: str, rrp: float):
    """
    Convert RRP from $/MWh to c/kWh for Aurora Energy.

    Parameters:
    - interval_datetime (datetime): The interval datetime.
    - tariff_code (str): The tariff code.
    - rrp (float): The Regional Reference Price in $/MWh.

    Returns:
    - float: The price in c/kWh.
    """
    interval_time = interval_datetime.astimezone(timezone(time_zone())).time()
    interval_date = interval_datetime.date()
    rrp_c_kwh = rrp / 10

    tariff = tariffs.get(tariff_code)
    if not tariff:
        raise ValueError(f"Unknown tariff code: {tariff_code}")

    # Special handling for Irrigation Time of Use tariff
    if tariff_code == '75':
        if is_winter(interval_date):
            if interval_datetime.weekday() < 5:  # Monday to Friday
                periods = [p for p in tariff['periods'] if p[0] in ['Peak', 'Off-peak']]
            else:  # Saturday and Sunday
                periods = [p for p in tariff['periods'] if p[0] in ['Shoulder', 'Off-peak']]
        else:  # Summer
            if interval_datetime.weekday() < 5:  # Monday to Friday
                periods = [p for p in tariff['periods'] if p[0] in ['Shoulder', 'Off-peak']]
            else:  # Saturday and Sunday
                periods = [p for p in tariff['periods'] if p[0] == 'Off-peak']
    else:
        periods = tariff['periods']

    # Find the applicable period and rate
    for period, start, end, rate in periods:
        if start <= interval_time < end:
            total_price = rrp_c_kwh + rate
            return total_price

    # If no period is found (shouldn't happen with proper setup)
    raise ValueError(f"No applicable period found for tariff {tariff_code} at time {interval_time}")

def get_daily_fee(tariff_code: str):
    """
    Get the daily supply charge for a given tariff code.

    Parameters:
    - tariff_code (str): The tariff code.

    Returns:
    - float: The daily supply charge in cents.
    """
    daily_fees = {
        '93': 134.9834,
        '94': 135.8181,
        '75': 351.2608,
        '31': 121.5081,
        '22': 116.7902,
        '82': 393.1143,
    }

    fee = daily_fees.get(tariff_code)
    if fee is None:
        raise ValueError(f"Unknown tariff code: {tariff_code}")

    return fee

def calculate_demand_fee(tariff_code: str, demand_kva: float, days: int = 30):
    """
    Calculate the demand fee for Tariff 82.

    Parameters:
    - tariff_code (str): The tariff code (should be '82').
    - demand_kva (float): The maximum demand in kVA.
    - days (int): The number of days in the billing period (default is 30).

    Returns:
    - float: The demand fee in dollars.
    """
    if tariff_code != '82':
        return 0.0

    annual_rate = 163.445  # $ per kVA per annum
    daily_rate = annual_rate / 365

    return demand_kva * daily_rate * days
