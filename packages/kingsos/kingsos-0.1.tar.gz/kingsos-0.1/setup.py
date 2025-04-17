# setup.py

from setuptools import setup, find_packages

setup(
    name="kingsos",           # Name of your package
    version="0.1",                     # Package version
    packages=find_packages(),          # Automatically find all packages
    include_package_data=True,         # Includes non-Python files (like your ZIP)
    description="A package to upload KingsOS Operating System",
    author="KralMatko",                 # Your name or company
    author_email="kingmartinv2015@gmail.com",  # Your email
    long_description=open("README.md").read(),  # Read long description from README
    long_description_content_type="text/markdown",
)
