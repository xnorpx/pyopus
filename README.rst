pyopus
======

**pyopus** is a Python binding to libopus_ using the excellent CFFI_
interface. It is written mainly because development of the existing
python-opus_ library seems to have ceased. Because of the usage of CFFI,
the library is compatible with both CPython (both 2.x and 3.x) and PyPy, and
its performance shouldn't be bad (testing welcome).

``pyopus`` runs on Linux, and probably any OS that both ``libopus`` and Python
supports. Microsoft Windows should be OK but not tested; pull requests are
welcome.

.. _libopus: http://opus-codec.org/
.. _CFFI: https://cffi.readthedocs.org/
.. _python-opus: https://github.com/svartalf/python-opus/


Features
--------

* Low-level ``libopus`` function wrappers
* Class-based high-level codecs intended for rapid development


License
-------

The ``pyopus`` library is licensed under the 3-clause BSD license; see
``LICENSE.txt`` for details.


Roadmap
-------

The following things are to be finished before a first stable release:

* Full ``libopus`` API coverage, minus Opus Custom
* Documentation work
* Basic test coverage


How to contribute
-----------------

Issues and pull requests are welcome. Please don't hesitate to provide your
feedback if you have tried this library out! It's vital for making Opus a
better codec on Python. Many thanks in advance!


.. vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
