from setuptools import setup, find_packages

setup(
    name="etopotools",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        'numpy',
        'matplotlib',
        'requests',
        'tqdm',
        'netCDF4'
    ],
    author="Francois Primeau",
    author_email="fprimeau@uci.edu",
    description="Tools for downloading and processing ETOPO data",
    python_requires=">=3.8",
)