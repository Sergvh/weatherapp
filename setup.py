from setuptools import setup, find_packages

setup(
    name="weatherapp.core",
    version="0.1.0",
    author="Hrytsenko Serhii",
    description="A simple cli weather aggregator",
    long_descriptoin="",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={
        'console_scripts': 'wfapp=weatherapp.core.app:main'
    },
    install_requires=[
        'requests',
        'bs4',
        'prettytable',
    ]
)