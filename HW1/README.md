# Homework 1: Oceanographic Data Analysis

## Problem 1: Global Ocean Surface Area and Ocean Coverage

This script (`prob1.py`) downloads global topographic data from ETOPO 2022 and calculates:
- The total surface area of Earth’s oceans
- The total surface area of Earth
- The percentage of Earth’s surface covered by ocean

### Features
- Downloads ETOPO 2022 surface elevation data using `etopotools`
- Calculates surface area elements on the sphere
- Masks regions corresponding to ocean (height < 0)
- Computes total ocean area and Earth’s total surface area

### Dependencies
- etopotools (custom package for ETOPO 2022 data access)
- numpy
- matplotlib

### Usage
```bash
python prob1.py
```

### Results
The script computes and prints:
- Ocean area in m²
- Total Earth surface area in m²
- Ocean coverage in %

---

## Problem 2: Global Ocean Volume Calculation

This script (`prob2.py`) uses ETOPO 2022 data to compute the total volume of the world’s oceans.  
The calculation assumes the volume element:

$$
 dV = a^2 \cos(\phi) \, d\phi \, d\lambda \, dz
$$

where \(a\) is the mean radius of the Earth.

### Features
- Downloads ETOPO 2022 surface elevation data using `etopotools`
- Calculates surface area elements on the sphere
- Masks regions corresponding to ocean (height < 0)
- Computes ocean volume by integrating ocean depth over the surface

### Dependencies
- etopotools (custom package for ETOPO 2022 data access)
- numpy
- matplotlib

### Usage
```bash
python prob2.py
```

### Results
The script computes and prints:
- Total ocean volume in cubic meters (m³)

---

## Problem 3: Global Ocean Temperature and Salinity Analysis

This script (`prob3.py`) computes global volumetric averages of temperature and salinity using World Ocean Atlas 2023 data.

### Features
- Downloads WOA23 temperature and salinity data
- Converts practical salinity to absolute salinity using TEOS-10 (`gsw`)
- Uses trapezoidal integration for vertical averaging
- Applies proper area weighting for horizontal averaging
- Handles land masks appropriately

### Dependencies
- woatools (custom package for WOA data access)
- numpy
- gsw (Gibbs SeaWater Toolbox)
- matplotlib

### Usage
```bash
python prob3.py
```

### Results
The script computes and prints:
- Global volumetric average temperature in °C
- Global volumetric average salinity in g/kg

---

## Problem 4: Seasonal Vertical Profiles at 45°N

This script (`prob4.py`) uses the 2023 World Ocean Atlas objectively analyzed monthly temperature and salinity CSV data to plot vertical profiles in a water column at approximately 45° N (∼30° W) for winter, spring, summer, and fall.

### Features
- Downloads WOA23 temperature and salinity CSV archives using `woatools`
- Reads four seasons at once via `read_woa_csv(..., time_code="13-16")`
- Extracts vertical profiles at the nearest grid point to 45° N, 30° W
- Converts practical salinity to absolute salinity with TEOS-10 (`gsw`)
- Produces a two-panel figure:
  - **Left panel**: temperature (°C) vs. depth (m)
  - **Right panel**: absolute salinity (g/kg) vs. depth (m)
- Inverts y‑axis so depth increases downward
- Includes legends, axis labels, and season‑colored curves
- Optional insets zoom into the top 300 m for detailed structure

### Dependencies
- woatools (custom package for WOA data access)
- numpy
- gsw (Gibbs SeaWater Toolbox)
- matplotlib

### Usage
```bash
python prob4.py
```

### Results
The script displays a figure with:
- Four seasonal temperature profiles in the North Atlantic at 45° N
- Four seasonal absolute salinity profiles at 45° N
- Depth on the vertical axis (in meters), with clear labels and gridlines
- Insets (if enabled) highlighting the top 300 m structure

