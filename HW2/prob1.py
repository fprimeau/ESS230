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

# Calculate the horizontal area at each depth level
dz = 50 # meters
z = np.arange(-6000, 0, dz) # depth levels
A = np.zeros(len(z)) # area at each depth level
for i in range(len(z)):
    # Calculate total ocean area
    A[i] = np.sum(dA[height < z[i]]) # area of grid cells below depth z[i]

fig, ax = plt.subplots()
ax.plot(A, z)
ax.set_xlabel('Area (m^2)')
ax.set_ylabel('Depth (m)')
fig.tight_layout()
plt.show()