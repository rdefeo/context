from distutils.core import setup
import os
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='context',
    version='0.0.2',
    packages=[
        'context',
        'context.data',
        'context.views',
    ],
    install_requires=required
)
