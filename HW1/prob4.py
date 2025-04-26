import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import gsw
from woatools import get_woa, read_woa_csv

# 1) Location: 45°N, 30°W (convert to WOA longitude convention if needed)
lat_target = 45.0
lon_target = -30.0  # negative = west

# 2) Download the monthly climatology archives (1° resolution)
temp_files = get_woa(v="t", t="decav", r="1.00", quiet=True)
salt_files = get_woa(v="s", t="decav", r="1.00", quiet=True)

# 3) Read all four seasons at once: time_code="13-16" → dims = (lat, lon, depth, 4)
t_data, coords = read_woa_csv(temp_files, field_code="an", time_code="13-16", quiet=False)
s_data, _      = read_woa_csv(salt_files, field_code="an", time_code="13-16", quiet=False)

# coords contains 'lat', 'lon', 'depth', and a time axis for the 4 seasons
lats   = coords["lat"]    # shape (nlat,)
lons   = coords["lon"]    # shape (nlon,)
depths = coords["depth"]  # shape (ndepth,)

# 4) Find nearest grid indices
#    Make longitude 0–360 if lons is that convention
lon_mod = (lon_target + 360) % 360
ilat = np.abs(lats - lat_target).argmin()
ilon = np.abs(lons - lon_mod).argmin()

# 5) Extract 4 seasonal profiles:
#    t_data[ilat, ilon, :, :] → shape (ndepth, 4)
#    transpose to (4, ndepth) for easy plotting
temp_profiles = t_data[ilat, ilon, :, :].T   # shape (4, ndepth)
salt_profiles = s_data[ilat, ilon, :, :].T   # shape (4, ndepth)

# 6) Convert SP → SA for each season
salt_absolute = []
for sp in salt_profiles:
    # sp: shape (ndepth,)
    SA = gsw.SA_from_SP(sp, depths, lon_target, lat_target)
    salt_absolute.append(SA)
salt_absolute = np.array(salt_absolute)      # shape (4, ndepth)

# 7) Plotting
season_names = ["Winter", "Spring", "Summer", "Fall"]
colors       = ["tab:blue",    "tab:green",     "tab:red",      "tab:orange"]

fig, (axT, axS) = plt.subplots(1, 2, figsize=(8, 10), sharey=True)

# Temperature panel
for prof, name, col in zip(temp_profiles, season_names, colors):
    axT.plot(prof, depths, label=name, color=col)
axT.invert_yaxis()
axT.set_xlabel("Temperature (°C)")
axT.set_ylabel("Depth (m)")
axT.set_title("Seasonal Temperature Profiles\n45°N, 30°W")
axT.grid(True)
axT.legend(loc="lower right")

# Salinity panel
for prof, name, col in zip(salt_absolute, season_names, colors):
    axS.plot(prof, depths, label=name, color=col)
axS.invert_yaxis()
axS.set_xlabel("Absolute Salinity (g/kg)")
axS.set_title("Seasonal Salinity Profiles\n45°N, 30°W")
axS.grid(True)
#axS.legend(loc="upper right")
axS.invert_yaxis()    

# Add insets to zoom into the top 200 m
for ax, profiles, xlabel in [(axT, temp_profiles, "Temperature (°C)"),
                             (axS, salt_absolute, "Absolute Salinity (g/kg)")]:
    
    # Create an inset axis 60% width × 40% height of the parent,
    # positioned in the upper left corner
    axins = inset_axes(ax, width="60%", height="40%", loc='lower right',
                       bbox_to_anchor=(-0.095, 0.18, 1, 1),
                       bbox_transform=ax.transAxes)
    
    # Only plot profiles down to 200 m
    mask = depths <= 200
    for prof, name, col in zip(profiles, season_names, colors):
        axins.plot(prof[mask], depths[mask], color=col)
    
    # **Turn on grid lines in the inset:**
    axins.grid(True, which='both', linestyle='--', linewidth=0.5)

    axins.invert_yaxis()
    axins.set_ylim(200, 0)             # Depth from 0 at top to 200 m at bottom
    axins.set_xlim(None)               # Auto–scale horizontal
    axins.set_xlabel(xlabel, fontsize=8)
    axins.set_ylabel("Depth (m)", fontsize=8)
    axins.tick_params(axis='both', labelsize=6)
    axins.set_title("Top 200 m", fontsize=9)

#plt.tight_layout()
plt.show()
