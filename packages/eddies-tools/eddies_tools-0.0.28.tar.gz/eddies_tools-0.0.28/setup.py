from setuptools import setup, find_packages
print(find_packages(where='src'))
setup(
    name='eddies_tools',
    version="0.0.28",
    packages=find_packages(where='src'),
    package_dir={'':'src'},
    include_package_data=True,  # This line is important
)