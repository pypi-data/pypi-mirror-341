# Python Luminous Mesh Client

A Python client implementation for the Luminous Mesh service.

## Installation

You can install the package using pip:

```bash
pip install python-luminous-mesh
```

Or directly from the source:

```bash
git clone https://github.com/yourusername/python-luminous-mesh.git
cd python-luminous-mesh
pip install .
```

## Usage

You can run the Luminous Mesh client in two ways:

1. Using the command-line interface:

```bash
# Using environment variables for configuration
luminous-mesh

# Using a configuration file
luminous-mesh --config path/to/config.yaml
```

2. As a Python package:

```python
import asyncio
from python_luminous_mesh.core.client import LuminousMeshClient
from python_luminous_mesh.config.settings import ClientSettings

async def run_client():
    # Load settings from environment variables
    settings = ClientSettings.from_env()
    
    # Or from a YAML file
    # settings = ClientSettings.from_yaml("path/to/config.yaml")
    
    client = LuminousMeshClient(settings)
    
    if await client.connect():
        try:
            # Your client logic here
            while True:
                await asyncio.sleep(1)
        finally:
            await client.close()

if __name__ == "__main__":
    asyncio.run(run_client())
```

## Configuration

The client can be configured either through environment variables or a YAML configuration file. See the documentation for more details on available configuration options.

## License

[Your License Here]
