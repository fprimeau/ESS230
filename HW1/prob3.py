import numpy as np
import matplotlib.pyplot as plt
from woatools import get_woa, read_woa_csv
import gsw 

# Get temperature data
temp_files = get_woa(v="t", t="decav", r="1.00", quiet=True)
temp_data, temp_coords = read_woa_csv(temp_files, "an", "00", quiet=True)   
    
# Get salinity data
salt_files = get_woa(v="s", t="decav", r="1.00", quiet=True)
salt_data, salt_coords = read_woa_csv(salt_files, "an", "00", quiet=True)

# Create a mesh of grid points
lam = temp_coords['lon'] * np.pi / 180  # longitude in radians
phi = temp_coords['lat'] * np.pi / 180  # latitude in radians
z   = -1.0 * temp_coords['depth']       # height above sea level

dphi = np.abs(phi[1] - phi[0])  # Assume uniform spacing
dlam = np.abs(lam[1] - lam[0])

# Create a mesh of pressures
p  = gsw.p_from_z(z[np.newaxis,:], phi[:,np.newaxis])
p = p[:, np.newaxis, :, np.newaxis] 

# Create a mesh of longitude and latitude
# Note: GSW functions expect longitude in degrees and latitude in degrees
# Create a mesh of longitude and latitude
lon_grid = lam[np.newaxis, :,np.newaxis, np.newaxis]*180/np.pi
lat_grid = phi[:,np.newaxis, np.newaxis, np.newaxis]*180/np.pi

# Convert practical salinity to absolute salinity
SA = gsw.SA_from_SP(salt_data, p, lon_grid, lat_grid)

# Convert temperature to conservative temperature
CT = gsw.CT_from_t(SA, temp_data, p)

temp = np.nan_to_num(temp_data, nan = 0.0)
salt = np.nan_to_num(SA, nan = 0.0)

# Create an area element array
a = 6.371e6  # Earth's radius in meters
dA = a**2 * np.cos(phi) * dphi * dlam 
dA = dA[:, np.newaxis] 

# create a wet dry mask wet = 1, dry = 0
wet = (~np.isnan(temp_data)).astype(np.float64)
h = np.trapezoid(wet, z, axis=2).squeeze()

# First compute vertical integrals for each water column using trapezoidal rule
T_col_int = np.trapezoid(temp, z, axis=2).squeeze() 
S_col_int = np.trapezoid(salt, z, axis=2).squeeze()


T_avg = np.sum( T_col_int * dA ) / np.sum( h*dA )
S_avg = np.sum( S_col_int * dA ) / np.sum( h*dA )

print(f"Global volumetric average temperature: {T_avg:.2f} °C")
print(f"Global volumetric average salinity: {S_avg:.2f} g/kg")

