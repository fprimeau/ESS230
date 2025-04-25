import os
import requests
import tarfile
import zipfile
import gzip
import shutil
from tqdm.auto import tqdm  # For progress bar
import numpy as np 
import pandas as pd 
from .database import init_database, record_download, get_download_date
from datetime import datetime


def get_citation(variable=None):
    """
    Returns formatted citation for WOA 2023 data with actual download date.
    
    Parameters:
    -----------
    variable : str, optional
        One-letter code for specific variable citation
    """
    download_dir = "woa_downloads"
    access_date = get_download_date(download_dir, variable) if variable else None
    
    if not access_date:
        access_date = datetime.now().strftime('%Y-%m-%d')
        
    citations = {
        't': (
            "Reagan, J.R., Boyer, T.P., García, H.E., Locarnini, R.A., Baranova, O.K., "
            "Bouchard, C., Cross, S.L., Mishonov, A.V., Paver, C.R., Seidov, D., & "
            "Dukhovskoy, D. (2024). World Ocean Atlas 2023, Volume 1: Temperature. "
            f"NOAA Atlas NESDIS 89. DOI: 10.25923/54bh-1613. Accessed {access_date}."
        ),
        's': (
            "Reagan, J.R., Seidov, D., Wang, Z., Dukhovskoy, D., Boyer, T.P., Locarnini, R.A., "
            "Baranova, O.K., Mishonov, A.V., García, H.E., Bouchard, C., Cross, S.L., & "
            "Paver, C.R. (2024). World Ocean Atlas 2023, Volume 2: Salinity. "
            f"NOAA Atlas NESDIS 90. DOI: 10.25923/70qt-9574. Accessed {access_date}."
        ),
        'o': (
            "García, H.E., Wang, Z., Bouchard, C., Cross, S.L., Paver, C.R., Reagan, J.R., "
            "Boyer, T.P., Locarnini, R.A., Mishonov, A.V., Baranova, O.K., Seidov, D., & "
            "Dukhovskoy, D. (2024). World Ocean Atlas 2023, Volume 3: Dissolved Oxygen, "
            "Apparent Oxygen Utilization, and Oxygen Saturation. NOAA Atlas NESDIS 91. "
            f"DOI: 10.25923/rb67-ns53. Accessed {access_date}."
        ),
        'n': (
            "García, H.E., Bouchard, C., Cross, S.L., Paver, C.R., Wang, Z., Reagan, J.R., "
            "Boyer, T.P., Locarnini, R.A., Mishonov, A.V., Baranova, O.K., Seidov, D., & "
            "Dukhovskoy, D. (2024). World Ocean Atlas 2023, Volume 4: Dissolved Inorganic "
            "Nutrients (phosphate, nitrate, silicate). A. Mishonov, Tech. Ed. NOAA Atlas "
            f"NESDIS 92. DOI: 10.25923/39qw-7j08. Accessed {access_date}."
        )
    }
    # Use same citation for all nutrients
    citations['p'] = citations['n']
    citations['i'] = citations['n']
    
    if variable is None:
        return "\n\n".join(list(set(citations.values())))
    elif variable in citations:
        return citations[variable]
    else:
        raise ValueError(f"Invalid variable code. Valid codes are: {', '.join(citations.keys())}")

def get_woa(v, t, r, quiet = False):
    """
    csv_list = get_woa(v="t", t="decav", r="1.00")
    csv_list = get_woa(v="s", t="all", r="0.25")
    csv_list = get_woa(v="i", t="decav", r="5.00")
    csv_list = get_woa(v="n", t="all", r="1.00")
    csv_list = get_woa(v="p", t="decav", r="0.25")      
    -------------------------------------------------------------------------
    World Ocean Atlas 2023 - Data Retrieval Utility
    -------------------------------------------------------------------------
    Downloads, extracts, and gunzips a WOA23 CSV archive based on the 
    specified variable, time span, and resolution.
    
    Input Parameters:
      v (str): Variable name (one-letter code mapped to full variable name)
               - 't': Temperature
               - 's': Salinity
               - 'i': Silicate
               - 'n': Nitrate
               - 'p': Phosphate
               - 'o': Dissolved Oxygen
               - 'O': Percent Saturation
               - 'A': Apparent Oxygen Utilization

      t (str): Time span abbreviation (mapped to descriptive time periods)
               - '5564': 1955-1964 (First decade with sufficient data)
               - '6574': 1965-1974 (10-year climatological mean period)
               - '7584': 1975-1984
               - '8594': 1985-1994
               - '95A4': 1995-2004 (Note: "95A4" denotes the 1995-2004 decade)
               - 'A5B4': 2005-2014 (Global coverage of Argo float era data)
               - 'B5C2': 2015-2022 (8-year period)
               - 'decav71A0': 1971-2000 (30-year climate normal)
               - 'decav81B0': 1981-2010 (30-year climate normal)
               - 'decav91C0': 1991-2020 (30-year climate normal)
               - 'decav': 1955-2022 (Average of the seven decadal means)
               - 'all': All available data (for oxygen/nutrients)

      r (str): Resolution designator (mapped to WOA-compatible resolution)
               - '1.00': 1.00-degree grid
               - '0.25': 0.25-degree grid
               - '5.00': 5.00-degree grid
      quiet (bool): If True, suppresses download progress output (default: False)
    -------------------------------------------------------------------------
    The function constructs the file URL and downloads the archive into the
    'woa_downloads' directory. If the archive is already present, the download is skipped.
    After extraction, any .csv.gz files are decompressed.
    -------------------------------------------------------------------------
    Base Data URL:
       https://www.ncei.noaa.gov/access/world-ocean-atlas-2023/
       (This official NOAA URL is the starting point for data access for WOA23.)

    Key References for WOA 2023:
       1. Temperature:
          Reagan, J.R., Boyer, T.P., García, H.E., Locarnini, R.A., Baranova, O.K.,
          Bouchard, C., Cross, S.L., Mishonov, A.V., Paver, C.R., Seidov, D., & Dukhovskoy, D.
          (2024). World Ocean Atlas 2023, Volume 1: Temperature. NOAA Atlas NESDIS 89.
          DOI: https://doi.org/10.25923/54bh-1613

       2. Salinity:
          Reagan, J.R., Seidov, D., Wang, Z., Dukhovskoy, D., Boyer, T.P., Locarnini, R.A.,
          Baranova, O.K., Mishonov, A.V., García, H.E., Bouchard, C., Cross, S.L., & Paver, C.R.
          (2024). World Ocean Atlas 2023, Volume 2: Salinity. NOAA Atlas NESDIS 90.
          DOI: https://doi.org/10.25923/70qt-9574

       3. Dissolved Oxygen:
          García, H.E., Wang, Z., Bouchard, C., Cross, S.L., Paver, C.R., Reagan, J.R., Boyer, T.P.,
          Locarnini, R.A., Mishonov, A.V., Baranova, O.K., Seidov, D., & Dukhovskoy, D.
          (2024). World Ocean Atlas 2023, Volume 3: Dissolved Oxygen, Apparent Oxygen Utilization,
          and Oxygen Saturation. NOAA Atlas NESDIS 91.
          DOI: https://doi.org/10.25923/rb67-ns53

       4. Nutrients:
          García, H.E., Bouchard, C., Cross, S.L., Paver, C.R., Wang, Z., Reagan, J.R., Boyer, T.P.,
          Locarnini, R.A., Mishonov, A.V., Baranova, O.K., Seidov, D., & Dukhovskoy, D.
          (2024). World Ocean Atlas 2023, Volume 4: Dissolved Inorganic Nutrients (phosphate, nitrate, silicate).
          A. Mishonov, Tech. Ed. NOAA Atlas NESDIS 92.
          DOI: https://doi.org/10.25923/39qw-7j08
    -------------------------------------------------------------------------
    """
  # Map one-letter codes to variable names
    variable_map = {
        "t": "temperature",
        "s": "salinity",
        "i": "silicate",
        "n": "nitrate",
        "p": "phosphate",
        "o": "oxygen",
        "O": "o2sat",
        "A": "AOU"
    }

    # Map time span abbreviations to descriptive names
    time_span_map = {
        "5564": "1955-1964",
        "6574": "1965-1974",
        "7584": "1975-1984",
        "8594": "1985-1994",
        "95A4": "1995-2004",
        "A5B4": "2005-2014",
        "B5C2": "2015-2022",
        "decav71A0": "1971-2000",
        "decav81B0": "1981-2010",
        "decav91C0": "1991-2020",
        "decav": "1955-2022",
        "all": "all available data"
    }

    # Map user-friendly resolutions to WOA-compatible resolutions
    resolution_map = {
        "1deg": "1.00",
        "1.00": "1.00",
        "0.25deg": "0.25",
        "0.25": "0.25",
        "5deg": "5.00",
        "5.00": "5.00"
    }

    # Validate and map the input variable
    if v not in variable_map:
        raise ValueError(f"Invalid variable code '{v}'. Valid codes are: {', '.join(variable_map.keys())}")
    v_full = variable_map[v]

    # Validate and map the time span
    if t not in time_span_map:
        raise ValueError(f"Invalid time span code '{t}'. Valid codes are: {', '.join(time_span_map.keys())}")
    t_full = time_span_map[t]

    # Validate and map the resolution
    if r not in resolution_map:
        raise ValueError(f"Invalid resolution code '{r}'. Valid codes are: {', '.join(resolution_map.keys())}")
    r_mapped = resolution_map[r]

    # Prepare URL components
    v_folder = v_full
    csv_folder = "csv"
    time_folder = t
    resolution_folder = r_mapped
    file_name = f"woa23_{v}_{t}_{r_mapped}_csv.tar.gz"

    # Construct the URL
    base_url = "https://www.ncei.noaa.gov/data/oceans/woa/WOA23/DATA"
    download_url = f"{base_url}/{v_folder}/{csv_folder}/{time_folder}/{resolution_folder}/{file_name}"
    if not quiet:
        print("Downloading from:", download_url)

    # Initialize download tracking database
    download_dir = "woa_downloads"
    os.makedirs(download_dir, exist_ok=True)
    init_database(download_dir)

    # Create download directory if it doesn't exist
    download_dir = "woa_downloads"
    os.makedirs(download_dir, exist_ok=True)
    local_path = os.path.join(download_dir, file_name)

    # Check whether the archive file already exists
    if os.path.exists(local_path):
        if not quiet:
            print(f"File {local_path} already exists. Skipping download.")
    else:
        # Download the archive with a progress bar
        with requests.get(download_url, stream=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192  # 8 KB blocks
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=file_name,
                      bar_format='{l_bar}{bar} {percentage:3.0f}%') as progress_bar:
                with open(local_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            progress_bar.update(len(chunk))
        if not quiet:        
            print("Downloaded file saved to:", local_path)

  # If download successful, record it
    if not os.path.exists(local_path):
        # ...existing download code...
        record_download(download_dir, file_name, v)

   # Extract the archive and track extracted files
    extracted_files = []
    if file_name.endswith(".tar.gz"):
        if not quiet:
            print("Extracting tar.gz archive...")
        with tarfile.open(local_path, "r:gz") as tar:
            # Get list of all files in the archive
            members = tar.getmembers()
            # Extract all files
            tar.extractall(path=download_dir)
            # Store the paths of extracted files
            extracted_files = [os.path.join(download_dir, member.name) 
                             for member in members]
        if not quiet:
            print("Extraction complete.")
    elif file_name.endswith(".zip"):
        if not quiet:
            print("Extracting zip archive...")
        with zipfile.ZipFile(local_path, "r") as zip_ref:
            # Get list of all files in the archive
            namelist = zip_ref.namelist()
            # Extract all files
            zip_ref.extractall(download_dir)
            # Store the paths of extracted files
            extracted_files = [os.path.join(download_dir, name) 
                             for name in namelist]
        if not quiet:
            print("Extraction complete.")
    else:
        print("Unknown file format; extraction not performed.")
        return []

    # Decompress only the .csv.gz files that were just extracted
    for gz_file in [f for f in extracted_files if f.endswith('.csv.gz')]:
        csv_path = gz_file[:-3]  # Strip off the .gz extension
        if not quiet:
            print(f"Decompressing {gz_file} to {csv_path}")
        with gzip.open(gz_file, 'rb') as f_in:
            with open(csv_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(gz_file)
        # Add the decompressed file path to our list
        extracted_files.append(csv_path)

    # Return only the paths of CSV files that were just extracted
    csv_files = [f for f in extracted_files if f.endswith('.csv')]
    return csv_files

def read_woa_csv(csv_files, field_code, time_code, quiet = False):
    """
    Read WOA CSV files into a 4D numpy array (lat, lon, depth, time).
    
    Parameters:
    -----------
    csv_files : list
        List of paths to CSV files returned by get_woa()
    field_code : str
        Field type code for selecting specific data fields. Options:
        
         Field Name                           Code   Available in               
         Objectively analyzed climatology      an    0.25°, 1.00°     
         Statistical mean                      mn    0.25°, 1.00°, 5° 
         Number of observations                dd    0.25°, 1.00°, 5° 
         Seasonal/monthly minus annual clim.   ma    0.25°, 1.00°     
         Standard deviation from stat. mean    sd    0.25°, 1.00°, 5° 
         Standard error of stat. mean          se    0.25°, 1.00°, 5° 
         Stat. mean minus obj. analyzed clim.  oa    0.25°, 1.00°     
         Num. of means within radius of infl.  gp    0.25°, 1.00°     
         Objectively analyzed std. deviation   sdo   0.25°, 1.00°     
         Standard error of the analysis        sea   0.25°, 1.00°
         
    time_code : str
        Time resolution code:
        - '00': Annual average
        - '01-12': Monthly values (January to December)
        - '13-16': Seasonal values (Winter, Spring, Summer, Fall)
        
    Returns:
    --------
    data : numpy.ndarray
        4D array with dimensions (latitude, longitude, depth, time)
    coords : dict
        Dictionary containing coordinate arrays:
        - 'lat': latitude values
        - 'lon': longitude values
        - 'depth': depth levels
        - 'time': time points
    """
    # Validate time code
    if time_code == '00':
        pattern = f'00{field_code}'
        expected_files = 1
    elif time_code == '01-12':
        pattern = f'[0-9][0-9]{field_code}'  # Will match 01-12
        expected_files = 12
    elif time_code == '13-16':
        pattern = f'1[3-6]{field_code}'  # Will match 13-16
        expected_files = 4
    else:
        raise ValueError("time_code must be '00' (annual), '01-12' (monthly), or '13-16' (seasonal)")

    # Filter files to match both field_code and time pattern
    import re
    filtered_files = [f for f in csv_files if re.search(pattern, f)]
    if not filtered_files:
        raise ValueError(f"No files found matching field code '{field_code}' and time code '{time_code}'")
    
    if len(filtered_files) != expected_files:
        raise ValueError(f"Found {len(filtered_files)} files, expected {expected_files} for time code {time_code}")
    
    # Sort files to ensure consistent ordering
    filtered_files.sort()
    
    # Read depth levels from the second line of first file
    with open(filtered_files[0], 'r') as f:
        _ = f.readline()  # Skip first line (variable info)
        depth_line = f.readline().strip()
        # Extract depths from the comma-separated list after "DEPTHS (M):"
        depth_str = depth_line.split('DEPTHS (M):')[1]
        depths = np.array([float(d) for d in depth_str.split(',')])

    # Initialize lists to store coordinates
    all_lats = set()
    all_lons = set()
    
    # First pass: collect all unique lat/lon coordinates
    for file in filtered_files:
        with open(file, 'r') as f:
            _ = f.readline()  # Skip header
            _ = f.readline()  # Skip depth line
            for line in f:
                values = line.strip().split(',')
                if len(values) >= 2:  # Ensure line has at least lat,lon
                    try:
                        lat, lon = float(values[0]), float(values[1])
                        all_lats.add(lat)
                        all_lons.add(lon)
                    except ValueError:
                        continue
    
    # Convert to sorted numpy arrays
    lats = np.array(sorted(all_lats))
    lons = np.array(sorted(all_lons))
    
    # Determine temporal resolution from number of files
    if len(filtered_files) == 12:
        n_time = 12  # Monthly data
        time_values = np.arange(1, 13)
    elif len(filtered_files) == 4:
        n_time = 4   # Seasonal data
        time_values = np.arange(1, 5)
    elif len(filtered_files) == 1:
        n_time = 1   # Annual average
        time_values = np.array([0])
    else:
        raise ValueError(f"Unexpected number of CSV files: {len(filtered_files)}. Expected 1, 4, or 12.")

    # Initialize output array with NaN values
    data = np.full((len(lats), len(lons), len(depths), n_time), np.nan)
    
    # Create coordinate mappings for faster indexing
    lat_idx = {lat: i for i, lat in enumerate(lats)}
    lon_idx = {lon: i for i, lon in enumerate(lons)}
    
    # Second pass: fill the data array
    for t, file in enumerate(filtered_files):
        with open(file, 'r') as f:
            _ = f.readline()  # Skip header
            _ = f.readline()  # Skip depth line
            for line in f:
                values = line.strip().split(',')
                if len(values) >= 3:  # Ensure line has data
                    try:
                        lat, lon = float(values[0]), float(values[1])
                        data_values = values[2:]
                        i = lat_idx[lat]
                        j = lon_idx[lon]
                        # Fill data for all available depths
                        for k, val in enumerate(data_values):
                            if val.strip():  # Check if value exists and is not empty
                                try:
                                    data[i, j, k, t] = float(val)
                                except (ValueError, IndexError):
                                    continue
                    except (ValueError, KeyError):
                        continue
    
    # Create coordinate dictionary
    coords = {
        'lat': lats,
        'lon': lons,
        'depth': depths,
        'time': time_values
    }
    
    return data, coords
# Test the functions
if __name__ == "__main__":
    # Add any test code here
    pass
