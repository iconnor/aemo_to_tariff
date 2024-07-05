# aemo_to_tariff

This Python package converts spot prices from $/MWh to c/kWh for different networks and tariffs.

## Installation

```bash
pip install aemo_to_tariff
```

## Usage

```python
from aemo_to_tariff import spot_to_tariff

price_c_kwh = spot_to_tariff('2024-07-05 14:00', 'Energex', '6970', 100)
print(price_c_kwh)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
