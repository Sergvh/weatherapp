from setuptools import setup, find_namespace_packages

setup(
    name="weatherapp.core",
    version="0.2.0",
    athor="Serhii hrytsenko",
    description="A simple cli weather aggregator",
    long_description="",
    packages=find_namespace_packages,
    entry_points={
        'console_scripts': 'wfapp=weatherapp.core.app:main'
    },
    install_requires=[
        'requests',
        'bs4',
    ]
)