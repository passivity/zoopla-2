# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'zoopla',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = zoopla.settings']},
    package_data={
        "zoopla": ["resources/*.txt"]
    },
    zip_safe=False
)
