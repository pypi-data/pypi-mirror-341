from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pywmm",
    version="1.1.1",
    description="World Magnetic Model (WMM) calculations in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Douglas Rojas",
    author_email="dougcr95@gmail.com",
    url="https://github.com/dougcr95/pywmm",
    packages=find_packages(include=["pywmm", "pywmm.*"]),
    package_data={
        "pywmm": ["data/*.COF"],
    },
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: GIS",
        "Operating System :: OS Independent",
    ],
    keywords="geomagnetic field navigation compass declination inclination WMM",
    python_requires=">=3.6",
    project_urls={
        "Bug Reports": "https://github.com/dougc95/pywmm/issues",  
        "Source": "https://github.com/dougc95/pywmm",  
        "Documentation": "https://github.com/dougc95/pywmm/blob/main/README.md", 
    }
)