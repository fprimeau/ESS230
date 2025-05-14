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

# Problem 1 (a):
for i in range(len(z)):
    A[i] = np.sum(dA[height < z[i]]) # area of grid cells below depth z[i]

# Problem 1 (b):
# Convert Sv to m³/s
Sv_to_m3s = 1e6

# Initialize volume flux array (in m³/s)
Q = np.zeros(len(z))

# Add deep water formation fluxes
z_5000m = np.abs(z + 5000).argmin()
z_4000m = np.abs(z + 4000).argmin()
z_500m = np.abs(z + 500).argmin()

# Add 20Sv at 5000m and 4000m
Q[z_5000m:] = 20 * Sv_to_m3s
Q[z_4000m:] = Q[z_4000m:] + 20 * Sv_to_m3s

# Calculate removal rate needed to get w=0 at surface
removal_rate = Q[z_500m] / (0 - z[z_500m])

# Remove water linearly from 500m to surface
for i in range(z_500m,len(z)):
    Q[i] = Q[i-1] - removal_rate * dz

# Calculate vertical velocity w = Q/A
w = Q / A  # m/s

# Create two-panel figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 10))

# Plot Area vs depth
ax1.plot(A, z, 'b-') 
ax1.set_xlabel('Area (m²)')
ax1.set_ylabel('Depth (m)')
ax1.grid(True)
ax1.set_title('Ocean Area vs Depth')
#ax1.set_aspect(1/4)

# Plot vertical velocity vs depth
ax2.plot(w, z, 'r-')
ax2.set_xlabel('Vertical velocity (m/s)')
ax2.set_ylabel('Depth (m)')
ax2.grid(True)
ax2.set_title('Vertical Velocity vs Depth')
#ax2.set_aspect(1/4)

# Format the figure
fig.tight_layout()
plt.savefig('ocean_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Print diagnostic values
print(f"Vertical velocity at 5000m: {w[z_5000m]:.2e} m/s")
print(f"Vertical velocity at 4000m: {w[z_4000m]:.2e} m/s")
print(f"Vertical velocity at 500m: {w[z_500m]:.2e} m/s")
print(f"Surface vertical velocity: {w[0]:.2e} m/s")
