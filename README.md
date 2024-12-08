# AEMO to Tariff

This is a Python library that converts AEMO (Australian Energy Market Operator) data to tariff data for various Australian energy distributors.

## Supported Distributors
- Ausgrid
- Endeavour Energy
- Energex
- Evoenergy
- SA Power Networks
- TasNetworks

## Installation
You can install the library using pip:

```
pip install aemo-to-tariff
```

## Usage
Here's an example of how to use the library:

```python
from aemo_to_tariff import convert

# Convert AEMO data to Ausgrid tariff data
ausgrid_tariff = convert('ausgrid', aemo_data)

# Convert AEMO data to Energex tariff data 
energex_tariff = convert('energex', aemo_data)
```

## Contributing
If you would like to contribute to this project, please feel free to submit a pull request. We welcome contributions of all kinds, including bug fixes, new features, and documentation improvements.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
