import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import gsw
from woatools import get_woa, read_woa_csv

# Problem 5: TEOS-10 and WOA23
# a) Volumetrically averaged thermal expansion coefficient (alpha) top 200m
# b) Volumetrically averaged haline contraction coefficient (beta) top 200m
# c) Total mass of salt in the ocean
# d) Total mass of freshwater in the ocean

# 1) Download decadal climatology ("decav") 1° data
temp_files = get_woa(v="t", t="decav", r="1.00", quiet=True)
salt_files = get_woa(v="s", t="decav", r="1.00", quiet=True)

# 2) Read objectively-analyzed fields at time_code="00" (climatology)
t_data, coords = read_woa_csv(temp_files, field_code="an", time_code="00", quiet=True)
s_data, _     = read_woa_csv(salt_files, field_code="an", time_code="00", quiet=True)

# 2b) Drop singleton time dimension if present
if t_data.ndim == 4:
    # shape: (nlat, nlon, ndepth, 1)
    t_data = np.squeeze(t_data, axis=3)
    s_data = np.squeeze(s_data, axis=3)

# 3) Extract coordinates
lats   = coords['lat']     # shape (nlat,)
lons   = coords['lon']     # shape (nlon,)
depths = coords['depth']   # shape (ndepth,)

# 4) Compute horizontal cell area element dA
#    using spherical formula dA = a^2 cos(phi) dphi dlam
a = 6371000.0  # mean Earth radius (m)
phi = lats * np.pi / 180  # latitude in radians
lam = lons * np.pi / 180  # longitude in radians
phi_grid, lam_grid = np.meshgrid(phi, lam, indexing='ij')

# grid spacings
dphi = np.abs(phi[1] - phi[0])
dlam = np.abs(lam[1] - lam[0])

# horizontal area
dA = a**2 * np.cos(phi_grid) * dphi * dlam  # (nlat, nlon)

# 5) Compute vertical layer thickness dz
#    approximate mid-layer thickness
dz = np.empty_like(depths)
dz[:-1] = np.diff(depths)
dz[-1] = dz[-2]

# full 3D volume element dV = dA[...,None] * dz[None,None,...]
dV = dA[:, :, None] * dz[None, None, :]

# 6) Create mask for ocean cells
wet = (~np.isnan(t_data)).astype(float)  # 1 over ocean, 0 over land

# === Top 200m calculations ===
mask200 = depths <= 200.0
# restrict arrays to top 200m
dV200 = dV[:, :, mask200]       # (nlat, nlon, n200)
wet200 = wet[:, :, mask200]

t200 = t_data[:, :, mask200]
m200 = s_data[:, :, mask200]  # practical salinity (PSU)

# Build 3D arrays for pressure, lat, lon over depths
nlat, nlon, n200 = t200.shape

# broadcast lat/lon grids
lat2d = phi_grid  # in radians but gsw expects degrees
lon2d = lam_grid

# convert grids back to degrees for gsw
lat2d_deg = lat2d*180/np.pi
lon2d_deg = lon2d*180/np.pi

# make 3D
lat3 = np.repeat(lat2d_deg[:, :, None], n200, axis=2)
lon3 = np.repeat(lon2d_deg[:, :, None], n200, axis=2)

# pressure ~ depth in dbar
p3   = np.repeat(depths[mask200][None, None, :], nlat, axis=0)
p3   = np.repeat(p3, nlon, axis=1)

# convert SP -> SA, CT -> conservative temperature
SA200 = gsw.SA_from_SP(m200, p3, lon3, lat3)
CT200 = gsw.CT_from_t(SA200, t200, p3)

# compute alpha, beta fields
alpha200 = gsw.alpha(SA200, CT200, p3)
beta200  = gsw.beta(SA200, CT200, p3)

# volumetric mean
vol_weight200 = dV200 * wet200
alpha_mean = np.nansum(alpha200 * vol_weight200) / np.nansum(vol_weight200)
beta_mean  = np.nansum(beta200  * vol_weight200) / np.nansum(vol_weight200)

# === Full-ocean salt & freshwater mass ===
# build 3D for full depths
lat3_full = np.repeat(lat2d_deg[:, :, None], depths.size, axis=2)
lon3_full = np.repeat(lon2d_deg[:, :, None], depths.size, axis=2)
p3_full   = np.repeat(depths[None, None, :], nlat, axis=0)
p3_full   = np.repeat(p3_full, nlon, axis=1)
SA_full  = gsw.SA_from_SP(s_data, p3_full, lon3_full, lat3_full)
CT_full  = gsw.CT_from_t(SA_full, t_data, p3_full)
rho_full = gsw.rho(SA_full, CT_full, p3_full)

# mass of salt = (SA/1000 [kg salt/kg sw]) * rho [kg/m3] * dV_full [m3]
salt_mass = np.nansum((SA_full / 1000.0) * rho_full * dV)

# freshwater mass = (1 - SA/1000) * rho * dV
fresh_mass = np.nansum((1.0 - SA_full / 1000.0) * rho_full * dV)

# 7) Print results
print(f"Volumetric mean thermal expansion (alpha) top 200m: {alpha_mean:.3e} 1/K")
print(f"Volumetric mean haline contraction (beta) top 200m: {beta_mean:.3e} kg/g")
print(f"Total mass of salt in ocean:        {salt_mass:.3e} kg")
print(f"Total mass of freshwater in ocean:  {fresh_mass:.3e} kg")
