import os
import requests
import tarfile
import zipfile
import gzip
import shutil
from tqdm import tqdm  # For progress bar

def get_woa(v, t, r):
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
        "O": "percent_saturation",
        "A": "apparent_oxygen_utilization"
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
    v_folder = v_full.lower()
    csv_folder = "csv"
    time_folder = t
    resolution_folder = r_mapped
    file_name = f"woa23_{v.lower()}_{t}_{r_mapped}_csv.tar.gz"

    # Construct the URL
    base_url = "https://www.ncei.noaa.gov/data/oceans/woa/WOA23/DATA"
    download_url = f"{base_url}/{v_folder}/{csv_folder}/{time_folder}/{resolution_folder}/{file_name}"
    print("Downloading from:", download_url)

    # Create download directory if it doesn't exist
    download_dir = "woa_downloads"
    os.makedirs(download_dir, exist_ok=True)
    local_path = os.path.join(download_dir, file_name)

    # Check whether the archive file already exists
    if os.path.exists(local_path):
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
        print("Downloaded file saved to:", local_path)

    # Extract the archive
    if file_name.endswith(".tar.gz"):
        print("Extracting tar.gz archive...")
        with tarfile.open(local_path, "r:gz") as tar:
            tar.extractall(path=download_dir)
        print("Extraction complete.")
    elif file_name.endswith(".zip"):
        print("Extracting zip archive...")
        with zipfile.ZipFile(local_path, "r") as zip_ref:
            zip_ref.extractall(download_dir)
        print("Extraction complete.")
    else:
        print("Unknown file format; extraction not performed.")

    # Decompress all '.csv.gz' files in the download directory
    gunzip_files(download_dir)

    # Collect and return the paths of all CSV files
    csv_files = []
    for root, dirs, files in os.walk(download_dir):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))
    return csv_files

def gunzip_files(directory):
    """
    Walks through the given directory and decompresses any file
    ending with '.csv.gz' into a plain .csv file, then removes the .csv.gz file.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv.gz"):
                gz_path = os.path.join(root, file)
                csv_path = os.path.join(root, file[:-3])  # Strip off the .gz extension
                print(f"Decompressing {gz_path} to {csv_path}")
                with gzip.open(gz_path, 'rb') as f_in:
                    with open(csv_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(gz_path)
