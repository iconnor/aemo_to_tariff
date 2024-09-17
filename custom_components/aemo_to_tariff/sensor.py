from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from aemo_to_tariff import spot_to_tariff
from datetime import datetime

class AEMOToTariffSensor(SensorEntity):
    def __init__(self, hass, network, tariff):
        self._hass = hass
        self._network = network
        self._tariff = tariff
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return f"AEMO to Tariff - {self._network} - {self._tariff}"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        # Get the current RRP from another sensor or integration
        rrp = self._hass.states.get('sensor.current_rrp').state
        
        # Get the current time
        now = datetime.now()
        
        # Convert RRP to tariff price
        tariff_price = spot_to_tariff(now, self._network, self._tariff, float(rrp))
        
        self._state = tariff_price
        self._attributes['network'] = self._network
        self._attributes['tariff'] = self._tariff
        self._attributes['rrp'] = rrp

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    network = config.get('network')
    tariff = config.get('tariff')
    async_add_entities([AEMOToTariffSensor(hass, network, tariff)])