from setuptools import setup, find_packages

setup(
    name="nasdaq_news",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={"nasdaq_news": ["data/*.json"]},
    description="Pre-collected news data for NASDAQ-100 companies.",
    author="Your Name",
    python_requires=">=3.7",
)
