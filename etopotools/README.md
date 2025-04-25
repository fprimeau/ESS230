# ETOPO Global Relief Model Package

Python package for downloading, reading, and visualizing ETOPO 2022 global relief model data.

## Features
- Download ETOPO 2022 data at various resolutions
- Multiple relief models: ice surface, bedrock, and geoid
- Easy-to-use plotting functions
- Proper citation generation

## Installation

```bash
cd /path/to/etopo
pip install -e .
```

## Usage

```python
from etopo import get_etopo, read_etopo, plot_etopo, get_citation

# Get proper citation
print(get_citation())

# Download ice surface data at 60 arc-second resolution
filename = get_etopo(model='ice', resolution='60', quiet=False)

# Read data into arrays
height, lat, lon = read_etopo(filename)

# Create visualization
fig, ax = plot_etopo(height, lat, lon, title="Global Ice Surface Relief")
```

## Available Data Options

### Relief Models
- `'ice'`: Ice surface elevation
- `'bed'`: Bedrock elevation
- `'geoid'`: Geoid height

### Resolutions
- `'15'`: 15 arc-seconds
- `'30'`: 30 arc-seconds
- `'60'`: 60 arc-seconds

## Functions

### get_etopo(model='ice', resolution='60', quiet=False)
Downloads ETOPO global relief model data.

### read_etopo(filename)
Reads ETOPO data from netCDF file.

### plot_etopo(height, lat, lon, title="Global Relief")
Creates a global relief map.

### get_citation()
Returns properly formatted citation with current access date.

## Dependencies
- numpy
- matplotlib
- requests
- tqdm
- netCDF4

## Data Citation
NOAA National Centers for Environmental Information. 2022: ETOPO 2022 15 Arc-Second Global Relief Model. NOAA National Centers for Environmental Information. https://doi.org/10.25921/fd45-gt74

## Author
Francois Primeau (fprimeau@uci.edu)

## License
This project is licensed under the MIT License.
