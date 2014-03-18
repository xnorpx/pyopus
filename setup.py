#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from setuptools import setup
from setuptools import find_packages

from pyopus import __version__
from pyopus import binding


setup(
        name='pyopus',
        version=__version__,
        description='Python CFFI binding to libopus',
        author='Wang Xuerui',
        author_email='idontknw.wang+pypi@gmail.com',
        license='BSD',
        url='https://github.com/xen0n/pyopus/',
        download_url='https://github.com/xen0n/pyopus/',
        install_requires=('decorator', 'cffi', ),
        packages=find_packages(exclude=['tests', ]),
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Multimedia :: Sound/Audio'
            'Topic :: Software Development :: Libraries :: Python Modules',
            ],
        zip_safe=False,
        ext_modules=[binding.ffi.verifier.get_extension(), ],
        )


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
