#!/usr/bin/python

from setuptools import setup, find_packages

__version__ = '1.0.0'

setup(name="labmix",
      version=__version__,
      description="General System Administrative Utilities",
      long_description="General System Administrative Utilities",
      url="",
      install_requires=['paramiko >= 2.0.2',
                        'isodate',
                        'argparse',
                        'kazoo',
                        'http',
                        'pywinrm',
                        'requests >= 1',
                        'prettytable',
                        'python-dateutil',
                        'dnspython'],
      packages=find_packages(),
      license='BSD (Simplified)',
      platforms='Posix; MacOS X;',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: System Administrators',
                   'Operating System :: OS Independent',
                   'Topic :: System :: Systems Administration'],
      )
