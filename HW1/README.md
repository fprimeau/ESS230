# Homework 1: World Ocean Atlas Analysis

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