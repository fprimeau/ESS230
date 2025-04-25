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
height, lat, lon = read_etopo(filename, quiet=True)

# Convert coordinates to radians
phi = lat * np.pi / 180  # latitude in radians
lam = lon * np.pi / 180  # longitude in radians

# Create coordinate meshgrid
phi_grid, lam_grid = np.meshgrid(phi, lam, indexing='ij')

# Calculate grid spacing in radians
dphi = np.abs(phi[1] - phi[0])
dlam = np.abs(lam[1] - lam[0])

# Earth's radius in meters
a = 6371000  # meters

# Calculate area element
dA = a**2 * np.cos(phi_grid) * dphi * dlam

# Create ocean mask (True where there's ocean)
ocean_mask = height < 0

# Calculate total ocean area
ocean_area = np.sum(dA * ocean_mask)

# Calculate total Earth surface area
earth_area = 4 * np.pi * a**2

# Print results
print(f"Ocean area: {ocean_area:.3e} m²")
print(f"Total Earth surface area: {earth_area:.3e}  m²")
print(f"Ocean coverage: {100*ocean_area/earth_area:.1f}%")

# Optional: Create a visualization
#plt.figure(figsize=(12, 6))
#plt.pcolormesh(lon, lat, ocean_mask, cmap='ocean')
#plt.colorbar(label='Ocean')
#plt.title('Ocean Distribution')
#plt.xlabel('Longitude (°E)')
#plt.ylabel('Latitude (°N)')
#plt.show()
