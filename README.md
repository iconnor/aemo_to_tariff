# aemo_to_tariff

This Python package converts spot prices from $/MWh to c/kWh for different networks and tariffs.

## Installation

```bash
pip install aemo_to_tariff
```

## Usage

```python
from aemo_to_tariff import spot_to_tariff

price_c_kwh = spot_to_tariff('2024-07-05 14:00', 'Energex', '6900', 100)
print(price_c_kwh)
```

## AEMO to Tariff Converter within Home Assistant

### Installation

1. Install this integration using HACS by adding it as a custom repository.
2. Restart Home Assistant.

### Configuration

Add the following to your `configuration.yaml`:

```yaml
aemo_to_tariff:
```

## Usage

#### Converting Spot Prices to Tariff Prices

You can use this integration to convert AEMO spot prices to estimated tariff prices. Here's an example of how to create a sensor that converts a spot price to an Energex 6900 tariff price:

1. Add the following to your `configuration.yaml`:

```yaml
sensor:
  - platform: template
    sensors:
      energex_6900_estimated_price:
        friendly_name: "Energex 6900 Estimated Price"
        unit_of_measurement: "c/kWh"
        value_template: >-
          {% set spot_price = states('sensor.your_spot_price_sensor') | float %}
          {% set converted_price = states('sensor.energex_6900_estimated_price') | float(default=0) %}
          {% if spot_price > 0 %}
            {% set data = {
              'interval_time': now().isoformat(),
              'network': 'energex',
              'tariff': '6900',
              'rrp': spot_price
            } %}
            {% set converted_price = service('aemo_to_tariff.convert_spot_to_tariff', **data) %}
          {% endif %}
          {{ converted_price | round(4) }}
```

2. Replace `sensor.your_spot_price_sensor` with the entity ID of your spot price sensor.
3. Adjust the `network` and `tariff` values as needed for your specific use case.
4. Restart Home Assistant.

This will create a new sensor `sensor.energex_6900_estimated_price` that estimates the Energex 6970 tariff price based on your spot price sensor.

#### Available Services

This integration provides the following services:

1. `aemo_to_tariff.convert_spot_to_tariff`: Converts a spot price to a tariff price.
2. `aemo_to_tariff.get_tariff_daily_fee`: Gets the daily fee for a tariff.
3. `aemo_to_tariff.get_tariff_demand_fee`: Calculates the demand fee for a tariff.

You can call these services in your automations or scripts. For example:

```yaml
service: aemo_to_tariff.convert_spot_to_tariff
data:
  interval_time: "{{ now().isoformat() }}"
  network: "energex"
  tariff: "6900"
  rrp: "{{ states('sensor.your_spot_price_sensor') }}"
```

### Notes

- Ensure that your spot price sensor reports the price in $/MWh.
- The converted prices are estimates and may not perfectly reflect actual retail electricity prices due to various factors.
- This integration is for informational purposes only and should not be used for billing or other official purposes.

For more information on supported networks and tariffs, please refer to the documentation.
