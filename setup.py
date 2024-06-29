from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='dwarf_test_apiV2',
    version='V1.1',
    packages=find_packages(),
    install_requires=requirements,
)