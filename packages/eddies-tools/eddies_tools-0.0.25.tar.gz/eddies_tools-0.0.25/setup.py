from setuptools import setup, find_packages

setup(
    name='eddies_tools',
    version="0.0.25",
    packages=find_packages(),
    include_package_data=True,  # This line is important
    package_data={
        "eddies_tools": ["eddies_tools/*"]  # Make sure this matches your structure
    }
)