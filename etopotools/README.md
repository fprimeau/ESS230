[![PyPI version](https://badge.fury.io/py/etopotools.svg)](https://badge.fury.io/py/etopotools)  [![Build Status](https://github.com/fprimeau/ESS230/actions/workflows/ci.yml/badge.svg)](https://github.com/fprimeau/ESS230/actions)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# etopotools

Python package for downloading, reading, and visualizing ETOPO 2022 global relief model data.

[Documentation](https://github.com/fprimeau/ESS230/tree/main/etopotools) • [Issues](https://github.com/fprimeau/ESS230/issues)

## Features

- Download ETOPO 2022 data at three resolutions (15", 30", 60")
- Relief models: ice surface, bedrock, geoid
- Simple functions to read NetCDF into NumPy arrays
- Plotting utility for global relief maps
- Automatic citation generation
- Caching and re-use of downloaded files

## Installation

Supports Python 3.8+.  Requires netCDF4 and its HDF5 dependencies.

```bash
# From PyPI
pip install etopotools

# From source (developer/editable mode)
git clone https://github.com/fprimeau/ESS230.git
cd ESS230/etopotools
pip install -e .
```

## Quickstart

```python
from etopotools import get_etopo, read_etopo, plot_etopo, get_citation

# 1. Citation for ETOPO
print(get_citation())  # prints NOAA citation with access date

# 2. Download ice surface at 60" resolution
fn = get_etopo(model='ice', resolution='60', quiet=False)

# 3. Read relief data into arrays
height, lat, lon = read_etopo(fn)

# 4. Plot a global relief map
fig, ax = plot_etopo(height, lat, lon, title='Global Ice Surface')
ax.coastlines(); fig.show()
```

## API Reference

### `get_etopo(model='ice', resolution='60', quiet=False)`
Download an ETOPO 2022 NetCDF file.

- **model** (`str`) – `'ice'`, `'bed'`, or `'geoid'`.
- **resolution** (`str`) – `'15'`, `'30'`, or `'60'` (arc-seconds).
- **quiet** (`bool`) – suppress output if `True`.

**Returns**: local file path (`str`).

### `read_etopo(filename)`
Read a NetCDF ETOPO file into NumPy.

- **filename** (`str`) – path to `.nc`.

**Returns**: `(height, lat, lon)` where `height` is 2D array (m), `lat` and `lon` 1D arrays (°N, °E).

### `plot_etopo(height, lat, lon, title=None)`
Plot relief using Matplotlib.

- **height** (`ndarray`) – relief data (m).
- **lat**, **lon** (`ndarray`) – coordinate vectors.
- **title** (`str`, optional).

**Returns**: `(fig, ax)` Matplotlib objects.

### `get_citation()`
Generate a formatted citation string for NOAA ETOPO 2022.

**Returns**: citation (`str`).

## Configuration & Caching

Downloaded `.nc` files are stored in `~/.etopo_downloads/` by default.  Repeat calls reuse existing files.

## Contributing

1. Fork the repo and create a feature branch.
2. Install in editable mode and add tests under `tests/`.
3. Submit a pull request.

## License

MIT © François Primeau

