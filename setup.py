#!/usr/bin/env python

from setuptools import find_packages, setup

from pyopus import __version__, binding

setup(
    name="pyopus",
    version=__version__,
    description="Python CFFI binding to libopus",
    author="Wang Xuerui",
    author_email="idontknw.wang+pypi@gmail.com",
    license="BSD",
    url="https://github.com/xen0n/pyopus/",
    download_url="https://github.com/xen0n/pyopus/",
    install_requires=[
        "cffi>=1.0.0",
    ],
    packages=find_packages(
        exclude=[
            "tests",
        ]
    ),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    zip_safe=False,
    ext_modules=[
        binding.ffi.verifier.get_extension(),
    ],
)
