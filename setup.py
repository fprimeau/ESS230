from setuptools import setup, find_packages

setup(
    name="ESS230tools",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'requests',
        'tqdm'
    ],
    author="Francois Primeau",
    author_email="fprimeau@uci.edu"
    description="ESS230 Tools for downloading and processing World Ocean Atlas 2023 data",
    keywords="oceanography, WOA, data analysis, UCI ESS230",
    url="https://github.com/fprimeau/woatools",
)