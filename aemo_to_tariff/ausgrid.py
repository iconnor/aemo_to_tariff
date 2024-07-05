# aemo_to_tariff/ausgrid.py
from datetime import datetime
from pytz import timezone

def time_zone():
    return 'Australia/Sydney'

def convert(interval_time: datetime, tariff: str, rrp: float):
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
    interval_time = interval_time.astimezone(timezone(time_zone()))
    rrp_c_kwh = rrp / 10
    if tariff == 'N70':
        return rrp_c_kwh + 14.40  # Todo: Update this value
    else:
        # Terrible approximation
        slope = 1.037869032618134
        intecept = 5.586606750833143
        return rrp_c_kwh * slope + intecept
