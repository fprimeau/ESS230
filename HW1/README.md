# Homework 1: Oceanographic Data Analysis

## Problem 1: Global Ocean Surface Area and Ocean Coverage

This script (`prob1.py`) downloads global topographic data from ETOPO 2022 and calculates:
- The total surface area of Earth's oceans
- The total surface area of Earth
- The percentage of Earth's surface covered by ocean

### Features
- Downloads ETOPO 2022 surface elevation data using `etopotools`
- Calculates surface area elements on the sphere
- Masks regions corresponding to ocean (height < 0)
- Computes total ocean area and Earth's total surface area

### Dependencies
- etopotools (custom package for ETOPO 2022 data access)
- numpy
- matplotlib

### Usage
```bash
python prob1.py
```


### Results
The script computes and prints
- Ocean area m²
- Total Earth surface area  m²
- Ocean coverage %

## Problem 3: Global Ocean Temperature and Salinity Analysis

This script (`prob3.py`) computes global volumetric averages of temperature and salinity using World Ocean Atlas 2023 data. 

### Features
- Downloads WOA23 temperature and salinity data
- Converts practical salinity to absolute salinity using TEOS-10
- Uses trapezoidal integration for vertical averaging
- Applies proper area weighting for horizontal averaging
- Handles land masks appropriately

### Dependencies
- woatools (custom package for WOA data access)
- numpy
- gsw (Gibbs SeaWater Oceanographic Package)
- matplotlib

### Usage
```python
python prob3.py
```

### Results
The script computes and prints:
- Global volumetric average temperature in °C
- Global volumetric average salinity in g/kg