from setuptools import setup, find_packages

setup(
 name='Datahub_Lib_Leon',
 version='0.2',
 packages=find_packages(),
 include_package_data=True,
 package_data={
 'Datahub_Lib': ['data/data_hub_lib.py'],
 },
 )

