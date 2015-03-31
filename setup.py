from setuptools import setup
from context import __version__
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='context',
    version=__version__,
    packages=[
        'context',
        'context.data',
        'context.handlers',
    ],
    install_requires=required
)
