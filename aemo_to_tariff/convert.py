# aemo_to_tariff/convert.py

from aemo_to_tariff.energex import convert as energex_convert
from aemo_to_tariff.ausgrid import convert as ausgrid_convert
from aemo_to_tariff.evoenergy import convert as evoenergy_convert

def spot_to_tariff(interval_time, network, tariff, rrp,
                   dlf=1.05905, mlf=1.0154,
                   market=1.0154):
    """
    Convert spot price from $/MWh to c/kWh for a given network and tariff.

    Parameters:
    - interval_time (str): The interval time.
    - network (str): The name of the network (e.g., 'Energex', 'Ausgrid', 'Evoenergy').
    - tariff (str): The tariff code (e.g., '6970', '017').
    - rrp (float): The Regional Reference Price in $/MWh.
    - dlf (float): The Distribution Loss Factor.
    - mlf (float): The Metering Loss Factor.

    Returns:
    - float: The price in c/kWh.
    """
    adjusted_rrp = rrp * dlf * mlf
    network = network.lower()
    if network == 'energex':
        return energex_convert(interval_time, tariff, adjusted_rrp)
    elif network == 'ausgrid':
        return ausgrid_convert(interval_time, tariff, adjusted_rrp)
    elif network == 'evoenergy':
        return evoenergy_convert(interval_time, tariff, adjusted_rrp)
    else:
        raise ValueError(f"Unknown network: {network}")
