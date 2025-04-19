from setuptools import setup, find_packages

setup(
    name='cisco_api_files',
    version='0.1',
    packages=find_packages(),
    install_requires=[
         "requests >= 2.31.0"
    ],
     entry_points={
         'console_scripts': [
             'cisco_api_files=cisco_mce_files:main',  # Adjust as needed
        ],
    },
)