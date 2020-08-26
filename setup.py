from cuefix import __version__
from setuptools import setup

setup(
    name='cuefix',
    version=__version__,
    url='https://github.com/yinyanghu/cuefix',
    autor='Jian Li',
    author_email='lijianxp2005@gmail.com',
    packages=['cuefix'],
    entry_points={
        'console_scripts': ['cuefix=cuefix.cli:main'],
    }
)
