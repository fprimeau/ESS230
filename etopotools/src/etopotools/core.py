import os
import requests
from tqdm.auto import tqdm
import sys
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
from datetime import datetime

def get_citation():
    """
    Returns formatted citation for ETOPO data with current access date.
    """
    today = datetime.now().strftime('%Y-%m-%d')
    citation = (
        f"NOAA National Centers for Environmental Information. 2022: "
        f"ETOPO 2022 15 Arc-Second Global Relief Model. "
        f"NOAA National Centers for Environmental Information. "
        f"https://doi.org/10.25921/fd45-gt74. "
        f"Accessed {today}."
    )
    return citation

def get_etopo(model='ice', resolution='60', quiet=False):
    """
    Download ETOPO global relief model data.
    
    Parameters
    ----------
    model : str
        Relief model type:
        - 'ice': Ice surface elevation
        - 'bed': Bedrock elevation
        - 'geoid': Geoid height
    resolution : str
        Grid resolution:
        - '15': 15 arc-seconds
        - '30': 30 arc-seconds
        - '60': 60 arc-seconds
    quiet : bool
        If True, suppresses progress output
        
    Returns
    -------
    str
        Path to downloaded netCDF file
        
    Notes
    -----
    ETOPO 2022 Global Relief Model combines:
    - Land topography from multiple sources
    - Ocean bathymetry from latest seafloor mapping
    - Ice surface, bedrock, and geoid data
    
    Reference:
    NOAA National Centers for Environmental Information. 2022: 
    ETOPO 2022 15 Arc-Second Global Relief Model. 
    DOI: 10.25921/fd45-gt74
    """

   # Validate inputs
    valid_models = {'ice': 'ice_surface', 'bed': 'bedrock', 'geoid': 'geoid'}
    valid_res = {'15', '30', '60'}
    
    if model not in valid_models:
        raise ValueError(f"Model must be one of {list(valid_models.keys())}")
    if resolution not in valid_res:
        raise ValueError(f"Resolution must be one of {valid_res}")


    base_url = "https://www.ngdc.noaa.gov/thredds/fileServer/global/ETOPO2022"

    if model == "ice":
        filename = f"ETOPO_2022_v1_{resolution}s_N90W180_surface.nc"
        subdir = f"{resolution}s/{resolution}s_surface_elev_netcdf"
    elif model == "geoid":
        filename = f"ETOPO_2022_v1_{resolution}s_N90W180_geoid.nc"
        subdir = f"{resolution}s/{resolution}s_geoid_netcdf"
    else:
        filename = f"ETOPO_2022_v1_{resolution}s_N90W180_{model}.nc"
        subdir = f"{resolution}s/{resolution}s_{model}_elev_netcdf"

    url = f"{base_url}/{subdir}/{filename}"
    
    # Create download directory in current working directory
    download_dir = os.path.join(os.getcwd(), "etopo_downloads")
    os.makedirs(download_dir, exist_ok=True)
    local_path = os.path.join(download_dir, filename)

    if os.path.exists(local_path):
        if not quiet:
            print(f"File exists: {local_path}")
        # Verify file is readable
        try:
            with nc.Dataset(local_path) as ds:
                pass
            return local_path
        except OSError:
            if not quiet:
                print(f"Existing file corrupted, re-downloading...")
            #os.remove(local_path)

    # Fetch response first to get total size
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192

    if not quiet:
        if total_size > 0:
            file_size_mb = total_size / (1024 * 1024)
            print(f"Downloading {filename} ({file_size_mb:.2f} MB)...")
        else:
            print(f"Downloading {filename}... (size unknown)")
    
    with open(local_path, 'wb') as f, tqdm(
            total=total_size if total_size > 0 else None,
            unit='iB',
            unit_scale=True,
            disable=quiet,
            ascii=True,
            dynamic_ncols=True,
            desc=filename
    ) as pbar:
        for chunk in response.iter_content(block_size):
            if chunk:
                size = f.write(chunk)
                pbar.update(size)
        f.flush()
        os.fsync(f.fileno())

        # Verify downloaded file
        try:
            with nc.Dataset(local_path) as ds:
                pass
        except OSError:
            #os.remove(local_path)
            raise RuntimeError(f"Downloaded file is corrupted or invalid NetCDF format")
            
        return local_path
        
        
def read_etopo(filename, quiet=False):
    """
    Read ETOPO data from netCDF file.
    
    Parameters
    ----------
    filename : str
        Path to netCDF file
        
    Returns
    -------
    tuple
        (height, lat, lon) arrays
    """
    with nc.Dataset(filename) as ds:
        height = ds.variables['z'][:].data
        lat = ds.variables['lat'][:].data
        lon = ds.variables['lon'][:].data
    return height, lat, lon

def plot_etopo(height, lat, lon, title="Global Relief"):
    """
    Create a global relief map.
    
    Parameters
    ----------
    height : ndarray
        Relief data
    lat : ndarray
        Latitude coordinates
    lon : ndarray
        Longitude coordinates
    title : str
        Plot title
    """
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Create mesh for plotting
    lon_mesh, lat_mesh = np.meshgrid(lon, lat)
    
    # Create relief map
    levels = np.linspace(-11000, 8000, 39)
    cf = ax.contourf(lon_mesh, lat_mesh, height, levels=levels, cmap='terrain')
    
    # Add colorbar
    cbar = plt.colorbar(cf, ax=ax)
    cbar.set_label('Elevation (m)')
    
    # Set labels and title
    ax.set_xlabel('Longitude (°E)')
    ax.set_ylabel('Latitude (°N)')
    ax.set_title(title)
    
    # Set reasonable limits
    ax.set_xlim(lon.min(), lon.max())
    ax.set_ylim(lat.min(), lat.max())
    
    return fig, ax