from setuptools import setup, find_packages

setup(
    name="busdriver",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'busdriver = busdriver.driver:main',
        ],
    }
)

