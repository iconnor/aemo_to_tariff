# aemo_to_tariff/convert.py

from aemo_to_tariff.energex import (
    convert as energex_convert,
    get_daily_fee as energex_daily_fee,
    calculate_demand_fee as energex_demand_fee
)
from aemo_to_tariff.ausgrid import convert as ausgrid_convert
from aemo_to_tariff.evoenergy import convert as evoenergy_convert

def spot_to_tariff(interval_time, network, tariff, rrp,
                   dlf=1.05905, mlf=1.0154, market=1.0154):
    """
    Convert spot price from $/MWh to c/kWh for a given network and tariff.

    Parameters:
    - interval_time (str): The interval time.
    - network (str): The name of the network (e.g., 'Energex', 'Ausgrid', 'Evoenergy').
    - tariff (str): The tariff code (e.g., '6970', '017').
    - rrp (float): The Regional Reference Price in $/MWh.
    - dlf (float): The Distribution Loss Factor.
    - mlf (float): The Metering Loss Factor.
    - market (float): The market factor.

    Returns:
    - float: The price in c/kWh.
    """
    adjusted_rrp = rrp * dlf * mlf * market
    network = network.lower()

    if network == 'energex':
        return energex_convert(interval_time, tariff, adjusted_rrp)
    elif network == 'ausgrid':
        return ausgrid_convert(interval_time, tariff, adjusted_rrp)
    elif network == 'evoenergy':
        return evoenergy_convert(interval_time, tariff, adjusted_rrp)
    else:
        raise ValueError(f"Unknown network: {network}")

def get_daily_fee(network, tariff, annual_usage=None):
    """
    Calculate the daily fee for a given network and tariff.

    Parameters:
    - network (str): The name of the network (e.g., 'Energex', 'Ausgrid', 'Evoenergy').
    - tariff (str): The tariff code.
    - annual_usage (float): Annual usage in kWh, required for some tariffs.

    Returns:
    - float: The daily fee in dollars.
    """
    network = network.lower()

    if network == 'energex':
        return energex_daily_fee(tariff, annual_usage)
    elif network == 'ausgrid':
        # Placeholder for Ausgrid daily fee calculation
        return 0.0
    elif network == 'evoenergy':
        # Placeholder for Evoenergy daily fee calculation
        return 0.0
    else:
        raise ValueError(f"Unknown network: {network}")

def calculate_demand_fee(network, tariff, demand_kw, days=30):
    """
    Calculate the demand fee for a given network, tariff, demand amount, and time period.

    Parameters:
    - network (str): The name of the network (e.g., 'Energex', 'Ausgrid', 'Evoenergy').
    - tariff (str): The tariff code.
    - demand_kw (float): The maximum demand in kW (or kVA for some tariffs).
    - days (int): The number of days for the billing period (default is 30).

    Returns:
    - float: The demand fee in dollars.
    """
    network = network.lower()

    if network == 'energex':
        return energex_demand_fee(tariff, demand_kw, days)
    elif network == 'ausgrid':
        # Placeholder for Ausgrid demand fee calculation
        return 0.0
    elif network == 'evoenergy':
        # Placeholder for Evoenergy demand fee calculation
        return 0.0
    else:
        raise ValueError(f"Unknown network: {network}")
