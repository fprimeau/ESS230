from setuptools import setup, find_packages

setup(
    name="woatools",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        'numpy',
        'pandas',
        'requests',
        'tqdm'
    ],
    author="Francois Primeau",
    author_email="fprimeau@uci.edu",
    description="Tools for downloading and processing WOA23 data",
    python_requires=">=3.8",
)