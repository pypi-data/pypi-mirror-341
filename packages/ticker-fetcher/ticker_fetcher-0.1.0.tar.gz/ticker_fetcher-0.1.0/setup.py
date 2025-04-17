from setuptools import setup, find_packages

setup(
    name="ticker-fetcher",
    version="0.1.0",
    author="Pratham",
    description="A simple package to fetch S&P 500 and crypto tickers",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
