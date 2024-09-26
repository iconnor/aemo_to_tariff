from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType

from aemo_to_tariff import spot_to_tariff, get_daily_fee, calculate_demand_fee

DOMAIN = "aemo_to_tariff"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the AEMO to Tariff component."""

    def convert_spot_to_tariff(interval_time, network, tariff, rrp, dlf=1.05905, mlf=1.0154, market=1.0154):
        return spot_to_tariff(interval_time, network, tariff, rrp, dlf, mlf, market)

    def get_tariff_daily_fee(network, tariff, annual_usage=None):
        return get_daily_fee(network, tariff, annual_usage)

    def get_tariff_demand_fee(network, tariff, demand_kw, days=30):
        return calculate_demand_fee(network, tariff, demand_kw, days)

    hass.services.async_register(DOMAIN, "convert_spot_to_tariff", convert_spot_to_tariff)
    hass.services.async_register(DOMAIN, "get_tariff_daily_fee", get_tariff_daily_fee)
    hass.services.async_register(DOMAIN, "get_tariff_demand_fee", get_tariff_demand_fee)

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AEMO to Tariff from a config entry."""
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
