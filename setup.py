from distutils.core import setup
import setuptools


setup(
    name='downloadsdotnl',
    version='1.0',
    install_requires=[
        'pymplay',
        'requests'
    ],
    packages=[
        'downloadsdotnl'
    ],
    entry_points={
        "console_scripts": [
            "ddnl = downloadsdotnl.entry_points:search"
        ]
    },
   )
