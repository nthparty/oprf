====
oprf
====

Oblivious pseudo-random function (OPRF) protocol functionality implementations based on Ed25519 primitives, including both pure-Python and libsodium-based variants.

|pypi|

.. |pypi| image:: https://badge.fury.io/py/oprf.svg
   :target: https://badge.fury.io/py/oprf
   :alt: PyPI version and link.

Purpose
-------
This library provides data structures and methods for a basic `oblivious pseudo-random function (OPRF) <https://en.wikipedia.org/wiki/Pseudorandom_function_family>`_ protocol. Thanks to the underlying `oblivious <https://pypi.org/project/oblivious/>`_ library, users of this library have the option of relying either on pure Python implementations of cryptographic primitives or on wrappers for `libsodium <https://github.com/jedisct1/libsodium>`_.

Package Installation and Usage
------------------------------
The package is available on PyPI::

    python -m pip install oprf

The library can be imported in the usual ways::

    import oprf
    from oprf import *

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `nose <https://nose.readthedocs.io/>`_ (see ``setup.cfg`` for configution details)::

    nosetests

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python oprf/oprf.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    pylint oprf

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the GitHub page for this library.

Versioning
----------
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.
