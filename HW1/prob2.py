import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add parent directory to Python path
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if module_path not in sys.path:
    sys.path.append(module_path)

try:
    from etopotools import get_etopo, read_etopo
except ImportError as e:
    print(f"Error importing etopotools: {e}")
    print(f"Python path: {sys.path}")
    sys.exit(1)

# Download and read ETOPO data
filename = get_etopo(model='ice', resolution='60', quiet=True)
height, lat, lon = read_etopo(filename)

# Convert coordinates to radians
phi = lat * np.pi / 180  # latitude in radians
lam = lon * np.pi / 180  # longitude in radians

# Create coordinate meshgrid
phi_grid, lam_grid = np.meshgrid(phi, lam, indexing='ij')

# Calculate grid spacing in radians
dphi = np.abs(phi[1] - phi[0])
dlam = np.abs(lam[1] - lam[0])

# Earth's mean radius in meters
a = 6371000  # meters

# Calculate area element (without vertical component)
dA = a**2 * np.cos(phi_grid) * dphi * dlam  # units: m²

# Calculate ocean depth = - height (height is positive for land)
depth = -np.where(height < 0, height, 0)  # m, 0 for land

# Calculate volume element
dV = dA * depth  # units: m³

# Calculate total ocean volume
V  = np.sum(dV)

# Print results
print(f"Total volume of the world's oceans: {V:.3e} m³")

