import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from woatools import get_woa, read_woa_csv
import numpy as np

def test_download_quiet():
    """Test downloading WOA data"""
    print("Testing data download...")
    csv_files = get_woa(v="t", t="decav", r="1.00", quiet=True)
    assert len(csv_files) > 0, "No files downloaded"
    print(f"Download successful: {len(csv_files)} files found")
    return csv_files

def test_read_data_quiet(csv_files,quiet=True):
    """Test reading different temporal resolutions"""
    print("\nTesting data reading...")
    
    # Test annual mean
    data, coords = read_woa_csv(csv_files, "an", "00",quiet=quiet)
    assert isinstance(data, np.ndarray), "Data should be numpy array"
    assert data.ndim == 4, "Data should be 4-dimensional"
    print(f"Annual data shape: {data.shape}")
    
    # Test seasonal data
    data, coords = read_woa_csv(csv_files, "an", "13-16",quiet=quiet)
    print(f"Seasonal data shape: {data.shape}")

if __name__ == "__main__":

    csv_files = test_download_quiet()
    test_read_data_quiet(csv_files)

