from setuptools import setup, find_packages

setup(
 name='Datahub_Lib',
 version='0.1',
 packages=find_packages(),
 include_package_data=True,
 package_data={
 'Datahub_Lib': ['data/data_hub_lib.py'],
 },
 )

