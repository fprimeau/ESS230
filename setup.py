from setuptools import setup, find_packages

setup(
    name="woatools",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'requests',
        'tqdm'
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Tools for downloading and processing World Ocean Atlas 2023 data",
    keywords="oceanography, WOA, data analysis",
    url="https://github.com/yourusername/woatools",
)