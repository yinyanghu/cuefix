from cuefix import __version__
from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='cuefix',
    version=__version__,
    url='https://github.com/yinyanghu/cuefix',
    autor='Jian Li',
    author_email='lijianxp2005@gmail.com',
    packages=['cuefix'],
    description='A simple tool to fix problematic CUE files.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': ['cuefix=cuefix.cli:main'],
    },
    install_requires=[
        'chardet >= 3.0.4',
    ],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
