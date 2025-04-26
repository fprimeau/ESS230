# WOA Tools

Python package for **downloading**, **caching**, and **processing** World Ocean Atlas 2023 data in CSV format.

## Package Structure
```
woatools/
├── src/
│   └── woatools/
│       ├── __init__.py
│       ├── woa.py         # Core download and parsing utilities
│       └── database.py    # SQLite functions for tracking downloads
├── README.md             # This file
├── setup.py or pyproject.toml   # Package metadata and build configuration
└── ...                   # Tests, examples, etc.
```

## Installation
```bash
# Clone repository
git clone https://github.com/yourusername/woatools.git
cd woatools

# Install in editable mode (for development)
pip install -e .
```

## Quickstart
```python
from woatools import get_woa, read_woa_csv, get_citation

# 1. Get citation text for temperature dataset
print(get_citation('t'))

# 2. Download 1° decadal temperature CSV archive
csv_list = get_woa(v='t', t='decav', r='1.00')

# 3. Read objectively‐analyzed data for annual mean (time_code='00')
data, coords = read_woa_csv(csv_list, field_code='an', time_code='00')

# 'data' shape: (nlat, nlon, ndepth)
# 'coords' is a dict with keys: 'lat', 'lon', 'depth', and 'time' if applicable
```

## Core Functions

### `get_citation(variable=None)`
- **Purpose**: Returns formatted citation strings for WOA 2023 data.
- **Arguments**:
  - `variable`: one of the WOA codes (`'t'`, `'s'`, `'i'`, `'n'`, `'p'`, `'o'`, `'O'`, `'A'`).
    - If `None`, returns a combined citation for all variables.
- **Returns**: citation string(s).

### `get_woa(v, t, r, quiet=False)`
- **Purpose**: Downloads and extracts WOA CSV archives.
- **Arguments**:
  - `v` (str): variable code (e.g., `'t'` for temperature, `'s'` for salinity).
  - `t` (str): time span code (`'decav'`, `'all'`, `'00'`–`'12'`, `'13'`–`'16'`).
  - `r` (str): resolution code (`'1.00'`, `'0.25'`, `'5.00'`).
  - `quiet` (bool): suppress progress output if `True`.
- **Behavior**:
  1. Maps input codes to WOA URL paths.
  2. Downloads `.tar.gz` archive into `woa_downloads` directory (skipping if already present).
  3. Extracts the archive, decompresses `*.csv.gz` to `*.csv`.
  4. Records each download in a SQLite database (`downloads.db`).
- **Returns**: list of local CSV file paths.

### `read_woa_csv(csv_files, field_code, time_code, quiet=False)`
- **Purpose**: Parses WOA CSV files into a 4D NumPy array.
- **Arguments**:
  - `csv_files` (list): paths returned by `get_woa()`.
  - `field_code` (str): e.g., `'an'` for objectively‐analyzed field.
  - `time_code` (str): one of `'00'`, `'01'`–`'12'`, or `'13'`–`'16'`.
  - `quiet` (bool): suppress parsing messages if `True`.
- **Behavior**:
  1. Filters and sorts the input CSVs based on `field_code` and `time_code`.
  2. Reads the depth levels from the CSV header.
  3. Scans each CSV to build a 4D array of shape `(nlat, nlon, ndepth, ntime)`.
  4. Builds a `coords` dict with keys `'lat'`, `'lon'`, `'depth'`, and `'time'` (if multiple slices).
- **Returns**: `(data, coords)` tuple.

## Database Utilities

The package tracks downloads to avoid redownloading the same archive.

### `init_database(download_dir)`
Initialize the `downloads.db` in `download_dir`.

### `record_download(download_dir, filename, variable)`
Record a new download entry (filename, variable code, timestamp).

### `get_download_date(download_dir, variable)`
Retrieve the most recent download date for a given variable.

## Examples
```python
# Annual surface salinity map at 0 m depth
csv_sal = get_woa(v='s', t='all', r='1.00')
sal_data, coords = read_woa_csv(csv_sal, 'an', '00')
# sal_data[:,:,0] contains 0 m depth salinity
```

## License
[MIT License](LICENSE)