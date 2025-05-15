from setuptools import setup, find_packages

setup(
    name="coregame",
    version="0.1",
    packages=find_packages(include=['coregame', 'coregame.*']),
)