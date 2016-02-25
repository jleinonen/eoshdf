#!/usr/bin/env python

import sys

long_description = """A Python code for simple reading of HDF4 files,
specifically those created by the NASA EOS data systems.

Requires NumPy and PyHDF.
"""


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('eoshdf', parent_package, top_path,
        version = '0.1.0',
        author = "Jussi Leinonen",
        author_email = "jsleinonen@gmail.com",
        description = "Simple reader for NASA EOS HDF4 files",
        license = "MIT",
        url = 'https://github.com/jleinonen/eoshdf',
        long_description = long_description,
        classifiers = [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Scientific/Engineering",
        ]
    )

    return config


if __name__ == "__main__":

    from numpy.distutils.core import setup
    setup(configuration=configuration,
        packages = ['eoshdf'],
        platforms = ['any'],
        requires = ['numpy', 'pyhdf'])
