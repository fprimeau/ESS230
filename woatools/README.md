# WOA Tools

Python package for downloading and processing World Ocean Atlas 2023 data.

## Installation

```bash
pip install -e .
```

## Usage

```python
from woatools import get_woa, read_woa_csv

# Download temperature data
csv_files = get_woa(v="t", t="decav", r="1.00")

# Read data
data, coords = read_woa_csv(csv_files, "an", "00")
```