====
oprf
====

Oblivious pseudo-random function (OPRF) protocol functionality implementations based on Curve25519 primitives, including both pure-Python and libsodium-based variants.

|pypi| |readthedocs| |actions| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/oprf.svg
   :target: https://badge.fury.io/py/oprf
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/oprf/badge/?version=latest
   :target: https://oprf.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |actions| image:: https://github.com/nthparty/oprf/workflows/lint-test-cover-docs/badge.svg
   :target: https://github.com/nthparty/oprf/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/nthparty/oprf/badge.svg?branch=main
   :target: https://coveralls.io/github/nthparty/oprf?branch=main
   :alt: Coveralls test coverage summary.

Purpose
-------
This library provides data structures and methods for a basic `oblivious pseudo-random function (OPRF) <https://en.wikipedia.org/wiki/Pseudorandom_function_family>`_ protocol. Thanks to the underlying `oblivious <https://pypi.org/project/oblivious/>`_ library, users of this library have the option of relying either on pure Python implementations of cryptographic primitives or on wrappers for `libsodium <https://github.com/jedisct1/libsodium>`_.

Package Installation and Usage
------------------------------
The package is available on `PyPI <https://pypi.org/project/oprf/>`_::

    python -m pip install oprf

The library can be imported in the usual ways::

    import oprf
    from oprf import *

Examples
^^^^^^^^
This library makes it possible to concisely prepare binary or string data for masking::

    >>> from oprf import data, mask
    >>> d = data.hash('abc')

A random mask can be constructed and applied to the data. A number of distinct notations is supported for masking in order to minimize differences between the notation within a protocol definition and its implementation::

    >>> m = mask() # Create random mask.
    >>> m.mask(d) == m(d) == m * d
    True
    >>> m(d) == d
    False

Mask inversion and unmasking are also supported::

    >>> c = m(d)
    >>> m.unmask(c) == (~m)(c) == c / m == d
    True

Masks can also be constructed deterministically from a bytes-like object or string::

    >>> m = mask.hash('123')

Because the classes ``data`` and ``mask`` are derived from ``bytes``, `all methods and other operators <https://docs.python.org/3/library/stdtypes.html#bytes>`_ supported by ``bytes`` objects are supported by ``data`` and ``mask`` objects::

    >>> hex = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27a03'
    >>> m = mask.fromhex(hex)
    >>> m.hex()
    'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27a03'

In addition, Base64 conversion methods are included to support concise encoding and decoding of ``data`` and ``mask`` objects::

    >>> d.from_base64(d.to_base64()) == d
    True
    >>> m.from_base64(m.to_base64()) == m
    True

Documentation
-------------
.. include:: toc.rst

The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org/>`_::

    cd docs
    python -m pip install -r requirements.txt
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. ../setup.py && make html

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org/>`_ (see ``setup.cfg`` for configuration details)::

    python -m pip install pytest pytest-cov
    python -m pytest

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python oprf/oprf.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    python -m pip install pylint
    python -m pylint oprf

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/nthparty/oprf>`_ for this library.

Versioning
----------
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.

Publishing
----------
This library can be published as a `package on PyPI <https://pypi.org/project/oprf/>`_ by a package maintainer. Install the `wheel <https://pypi.org/project/wheel/>`_ package, remove any old build/distribution files, and package the source into a distribution archive::

    python -m pip install wheel
    rm -rf dist *.egg-info
    python setup.py sdist bdist_wheel

Next, install the `twine <https://pypi.org/project/twine/>`_ package and upload the package distribution archive to PyPI::

    python -m pip install twine
    python -m twine upload dist/*
