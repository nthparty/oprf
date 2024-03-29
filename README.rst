====
oprf
====

Oblivious pseudo-random function (OPRF) protocol functionality implementations based on `Curve25519 <https://cr.yp.to/ecdh.html>`__ and the `Ristretto <https://ristretto.group>`__ group.

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
This library provides data structures and methods for a basic `oblivious pseudo-random function (OPRF) <https://en.wikipedia.org/wiki/Pseudorandom_function_family>`__ protocol. Method implementations rely on cryptographic primitives involving the `Ristretto <https://ristretto.group>`__ group that are exported by the `oblivious <https://pypi.org/project/oblivious>`__ library. By default, these are wrappers for functions found in the subset of the `libsodium <https://github.com/jedisct1/libsodium>`__ library that is bundled with the `rbcl <https://pypi.org/project/rbcl>`__ library.

Installation and Usage
----------------------
This library is available as a `package on PyPI <https://pypi.org/project/oprf>`__:

.. code-block:: bash

    python -m pip install oprf

By default, this library indirectly relies on `rbcl <https://pypi.org/project/rbcl>`__ (which bundles a subset of the `libsodium <https://github.com/jedisct1/libsodium>`__ library that is compiled for common architectures). However, it is possible to install a fully working pure-Python version of this library by installing only the pure-Python subset of the `oblivious <https://pypi.org/project/oblivious>`__ dependency (*i.e.*, within an environment where `rbcl <https://pypi.org/project/rbcl>`__ is not a required dependency of other installed packages). This approach makes it possible to use this library for rapid prototyping on exotic architectures (with the caveat that pure-Python implementations of primitives are much slower):

.. code-block:: bash

    python -m pip install oblivious~=7.0
    python -m pip install oprf --no-dependencies

The library can be imported in the usual ways:

.. code-block:: python

    import oprf
    from oprf import *

Examples
^^^^^^^^
This library makes it possible to concisely prepare binary or string data for masking:

.. code-block:: python

    >>> from oprf import data, mask
    >>> d = data.hash('abc')

A random mask can be constructed and applied to the data. A number of distinct notations is supported for masking in order to minimize differences between the notation within a protocol definition and its implementation:

.. code-block:: python

    >>> m = mask() # Create random mask.
    >>> m.mask(d) == m(d) == m * d
    True
    >>> m(d) == d
    False

Mask inversion and unmasking are also supported:

.. code-block:: python

    >>> c = m(d)
    >>> m.unmask(c) == (~m)(c) == c / m == d
    True

Masks can also be constructed deterministically from a bytes-like object or string:

.. code-block:: python

    >>> m = mask.hash('123')

.. |data| replace:: ``data``
.. _data: https://oprf.readthedocs.io/en/5.0.0/_source/oprf.html#oprf.oprf.data

.. |mask| replace:: ``mask``
.. _mask: https://oprf.readthedocs.io/en/5.0.0/_source/oprf.html#oprf.oprf.mask

.. |bytes| replace:: ``bytes``
.. _bytes: https://docs.python.org/3/library/stdtypes.html#bytes

Because the classes |data|_ and |mask|_ are derived from |bytes|_, `all methods and other operators <https://docs.python.org/3/library/stdtypes.html#bytes>`__ supported by |bytes|_ objects are supported by |data|_ and |mask|_ objects:

.. code-block:: python

    >>> hex = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27a03'
    >>> m = mask.fromhex(hex)
    >>> m.hex()
    'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27a03'

In addition, Base64 conversion methods are included to support concise encoding and decoding of |data|_ and |mask|_ objects:

.. code-block:: python

    >>> d.from_base64(d.to_base64()) == d
    True
    >>> m.from_base64(m.to_base64()) == m
    True

Development
-----------
All installation and development dependencies are fully specified in ``pyproject.toml``. The ``project.optional-dependencies`` object is used to `specify optional requirements <https://peps.python.org/pep-0621>`__ for various development tasks. This makes it possible to specify additional options (such as ``docs``, ``lint``, and so on) when performing installation using `pip <https://pypi.org/project/pip>`__:

.. code-block:: bash

    python -m pip install .[docs,lint]

Documentation
^^^^^^^^^^^^^
The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org>`__:

.. code-block:: bash

    python -m pip install .[docs]
    cd docs
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. && make html

Testing and Conventions
^^^^^^^^^^^^^^^^^^^^^^^
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org>`__ (see the ``pyproject.toml`` file for configuration details):

.. code-block:: bash

    python -m pip install .[test]
    python -m pytest

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`__:

.. code-block:: bash

    python src/oprf/oprf.py -v

Style conventions are enforced using `Pylint <https://pylint.readthedocs.io>`__:

.. code-block:: bash

    python -m pip install .[lint]
    python -m pylint src/oprf

Contributions
^^^^^^^^^^^^^
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/nthparty/oprf>`__ for this library.

Versioning
^^^^^^^^^^
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`__.

Publishing
^^^^^^^^^^
This library can be published as a `package on PyPI <https://pypi.org/project/oprf>`__ by a package maintainer. First, install the dependencies required for packaging and publishing:

.. code-block:: bash

    python -m pip install .[publish]

Ensure that the correct version number appears in ``pyproject.toml``, and that any links in this README document to the Read the Docs documentation of this package (or its dependencies) have appropriate version numbers. Also ensure that the Read the Docs project for this library has an `automation rule <https://docs.readthedocs.io/en/stable/automation-rules.html>`__ that activates and sets as the default all tagged versions. Create and push a tag for this version (replacing ``?.?.?`` with the version number):

.. code-block:: bash

    git tag ?.?.?
    git push origin ?.?.?

Remove any old build/distribution files. Then, package the source into a distribution archive:

.. code-block:: bash

    rm -rf build dist src/*.egg-info
    python -m build --sdist --wheel .

Finally, upload the package distribution archive to `PyPI <https://pypi.org>`__:

.. code-block:: bash

    python -m twine upload dist/*
