from datetime import time, datetime
from zoneinfo import ZoneInfo


def time_zone():
    return 'Australia/Sydney'


tariffs = {
    'N70': {
        'name': 'Residential Flat',
        'periods': [
            ('Anytime', time(0, 0), time(23, 59), 8.4180)
        ]
    },
    'N71': {
        'name': 'Residential Seasonal TOU',
        'periods': [
            ('High-season Peak', time(16, 0), time(20, 0), 20.0116),
            ('Low-season Peak', time(16, 0), time(20, 0), 10.8094),
            ('Off Peak', time(0, 0), time(16, 0), 6.8217),
            ('Off Peak', time(20, 0), time(23, 59), 6.8217)
        ]
    },
    'N90': {
        'name': 'General Supply Block',
        'periods': [
            ('Block 1', time(0, 0), time(23, 59), 8.8705),
            ('Block 2', time(0, 0), time(23, 59), 10.3335)
        ]
    },
    'N91': {
        'name': 'GS Seasonal TOU',
        'periods': [
            ('High-season Peak', time(16, 0), time(20, 0), 20.7287),
            ('Low-season Peak', time(16, 0), time(20, 0), 11.5265),
            ('Off Peak', time(0, 0), time(16, 0), 7.5388),
            ('Off Peak', time(20, 0), time(23, 59), 7.5388)
        ]
    },
    'N19': {
        'name': 'LV Seasonal STOU Demand',
        'periods': [
            ('High-season Peak', time(16, 0), time(20, 0), 4.2883),
            ('Low-season Peak', time(16, 0), time(20, 0), 3.6717),
            ('Off Peak', time(0, 0), time(16, 0), 2.1951),
            ('Off Peak', time(20, 0), time(23, 59), 2.1951)
        ]
    }
}


def calculate_daily_fee(tariff_code: str):
    """
    Calculate the daily fee for a given tariff.

    Parameters:
    - tariff_code (str): The tariff code.

    Returns:
    - float: The daily fee in dollars.
    """
    tariff = tariffs.get(tariff_code)
    if not tariff:
        raise ValueError(f"Unknown tariff code: {tariff_code}")

    return 39.7300

def calculate_demand_fee(tariff: str, demand_kw: float, days=30):
    """
    Calculate the demand fee for a given tariff, demand amount, and time period.

    Parameters:
    - tariff (str): The tariff code.
    - demand_kw (float): The maximum demand in kW (or kVA for some tariffs).
    - days (int): The number of days for the billing period (default is 30).

    Returns:
    - float: The demand fee in dollars.
    """
    tariff = tariffs[tariff]

    # Find the applicable rate
    for period, start, end, rate in tariff['periods']:
        if start <= demand_kw < end:
            return rate * days

    raise ValueError(f"Unknown demand amount: {demand_kw}")

def get_periods(tariff_code: str):
    tariff = tariffs.get(tariff_code)
    if not tariff:
        raise ValueError(f"Unknown tariff code: {tariff_code}")

    return tariff['periods']

def convert(interval_datetime: datetime, tariff_code: str, rrp: float):
    """
    Convert RRP from $/MWh to c/kWh for endeavour.

    Parameters:
    - interval_datetime (datetime): The interval time.
    - tariff (str): The tariff code.
    - rrp (float): The Regional Reference Price in $/MWh.

    Returns:
    - float: The price in c/kWh.
    """
    interval_time = interval_datetime.astimezone(ZoneInfo(time_zone())).time()
    rrp_c_kwh = rrp / 10
    tariff = tariffs[tariff_code]

    # Determine if it's high season (November to March) or low season (April to October)
    current_month = interval_datetime.month
    is_high_season = current_month in [11, 12, 1, 2, 3]

    # Find the applicable period and rate
    for period, start, end, rate in tariff['periods']:
        if start <= interval_time < end:
            if 'season' in tariff['name'].lower():
                if is_high_season and 'high' in period.lower():
                    total_price = rrp_c_kwh + rate
                    return total_price
                elif 'low' in period.lower() and not is_high_season:
                    total_price = rrp_c_kwh + rate
                    return total_price
                elif 'off' in period.lower():
                    total_price = rrp_c_kwh + rate
                    return total_price
                else:
                    continue
            else:
                total_price = rrp_c_kwh + rate
                return total_price

    # Otherwise, this terrible approximation
    slope = 1.037869032618134
    intecept = 5.586606750833143
    return rrp_c_kwh * slope + intecept
