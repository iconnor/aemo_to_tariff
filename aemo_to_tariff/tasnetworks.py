# aemo_to_tariff/tasnetworks.py
from datetime import time, datetime
from pytz import timezone

def time_zone():
    return 'Australia/Hobart'


tariffs = {
    'TAS93': {
        'name': 'Residential time of use consumption',
        'periods': [
            ('Peak', time(7, 0), time(10, 0), 17.229),
            ('Peak', time(16, 0), time(21, 0), 17.229),
            ('Off-peak', time(21, 0), time(7, 0), 3.618),
            ('Off-peak', time(10, 0), time(16, 0), 3.618),
        ]
    },
    'TAS87': {
        'name': 'Residential time of use demand',
        'periods': [
            ('Peak', time(7, 0), time(10, 0), 30.133),
            ('Peak', time(16, 0), time(21, 0), 30.133),
            ('Off-peak', time(21, 0), time(7, 0), 10.034),
            ('Off-peak', time(10, 0), time(16, 0), 10.034),
        ]
    },
    'TAS97': {
        'name': 'Residential time of use CER',
        'periods': [
            ('Peak', time(7, 0), time(10, 0), 18.090),
            ('Peak', time(16, 0), time(21, 0), 18.090),
            ('Off-peak', time(21, 0), time(7, 0), 2.714),
            ('Off-peak', time(10, 0), time(16, 0), 2.714),
            ('Super off-peak', time(10, 0), time(16, 0), 0.090),
        ]
    },
    'TAS94': {
        'name': 'Small business time of use consumption',
        'periods': [
            ('Peak', time(7, 0), time(22, 0), 16.784),
            ('Shoulder', time(22, 0), time(23, 59), 9.886),
            ('Shoulder', time(0, 0), time(7, 0), 9.886),
            ('Off-peak', time(0, 0), time(23, 59), 2.426),  # Applies on weekends
        ]
    },
    'TAS88': {
        'name': 'Small business time of use demand',
        'periods': [
            ('Peak', time(7, 0), time(22, 0), 68.628),
            ('Off-peak', time(22, 0), time(7, 0), 22.853),
        ]
    },
}

demand_charges = {
    'TAS87': {
        'peak': 30.133,
        'off_peak': 10.034
    },
    'TAS97': {
        'peak': 25.613
    },
    'TAS88': {
        'peak': 68.628,
        'off_peak': 22.853
    },
    'TAS98': {
        'peak': 68.628,
        'off_peak': 22.853
    },
    'TAS89': {
        'peak': 52.542,
        'off_peak': 17.496
    },
    'TAS82': {
        'all': 40.211
    }
}

daily_fees = {
    'TAS93': 70.032,
    'TAS87': 71.258,
    'TAS97': 70.032,
    'TAS94': 83.780,
    'TAS88': 92.661,
    'TAS98': 92.661,
    'TAS89': 619.613,
    'TAS82': 439.841,
}


def get_periods(tariff_code: str):
    tariff = tariffs.get(tariff_code)
    if not tariff:
        raise ValueError(f"Unknown tariff code: {tariff_code}")

    return tariff['periods']

def convert(interval_datetime: datetime, tariff_code: str, rrp: float):
    """
    Convert RRP from $/MWh to c/kWh for TasNetworks.

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

    # Check if it's a weekend for TAS94
    is_weekend = interval_datetime.weekday() >= 5

    # Find the applicable period and rate
    for period, start, end, rate in tariff['periods']:
        if tariff_code == 'TAS94' and period == 'Off-peak' and is_weekend:
            return rrp_c_kwh + rate
        elif start <= interval_time < end or (start > end and (interval_time >= start or interval_time < end)):
            return rrp_c_kwh + rate

    # If no period is found, use the default rate (first rate in the list)
    return rrp_c_kwh + tariff['periods'][0][3]


def calculate_demand_fee(tariff_code: str, demand_kw: float, peak_demand_kw: float = None, days: int = 30):
    """
    Calculate the demand fee for a given tariff code, demand amount, and time period.

    Parameters:
    - tariff_code (str): The tariff code.
    - demand_kw (float): The maximum demand in kW.
    - peak_demand_kw (float): The maximum demand during peak hours in kW (if applicable).
    - days (int): The number of days for the billing period (default is 30).

    Returns:
    - float: The demand fee in dollars.
    """
    if tariff_code not in demand_charges:
        return 0.0  # Return 0 if the tariff doesn't have a demand charge

    charges = demand_charges[tariff_code]
    daily_rate = days / 30  # Convert to daily rate

    if 'peak' in charges and 'off_peak' in charges:
        if peak_demand_kw is None:
            raise ValueError("Peak demand is required for this tariff.")
        peak_charge = charges['peak'] * peak_demand_kw * daily_rate
        off_peak_charge = charges['off_peak'] * (demand_kw - peak_demand_kw) * daily_rate
        return peak_charge + off_peak_charge
    elif 'peak' in charges:
        return charges['peak'] * demand_kw * daily_rate
    elif 'all' in charges:
        return charges['all'] * demand_kw * daily_rate
    else:
        return 0.0  # Return 0 if no applicable charge is found

def get_daily_fee(tariff_code: str):
    """
    Get the daily fee for a given tariff code.

    Parameters:
    - tariff_code (str): The tariff code.

    Returns:
    - float: The daily fee in cents.
    """
    return daily_fees.get(tariff_code, 0.0)
