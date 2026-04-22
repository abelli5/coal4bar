"""Setup script for coal4bar package"""

from setuptools import setup, find_packages

setup(
    name="coal4bar",
    version="0.1.0",
    description="Four-Bar Hydraulic Support Simulation and Analysis Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="coal4bar development team",
    author_email="info@coal4bar.dev",
    url="https://github.com/abelli5/coal4bar",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.12.0",
            "black>=21.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="coal-mining hydraulic-support four-bar-linkage simulation",
)
