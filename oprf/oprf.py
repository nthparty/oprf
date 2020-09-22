"""OPRF protocol functionalities.

Oblivious pseudo-random function (OPRF) protocol functionality
implementations based on Ed25519 primitives.
"""

from __future__ import annotations
import doctest
import hashlib
import oblivious

class data(oblivious.point):
    """
    Wrapper class for a bytes-like object that corresponds
    to a data data that can be masked.

    >>> data('abc').hex()
    '5a5dbd5c765abf60b2076133482c1ada189c319034ae0b933f4908b3b68d0225'
    >>> data(bytes([123])).hex()
    'be6f2de25b6907d7e07e6a75424c6f4bbed103c2957b9fa9fbe4fd63dfa5575b'
    >>> data([1, 2, 3])
    Traceback (most recent call last):
      ...
    TypeError: data object must be built from a string or bytes-like object
    """

    def __new__(cls, a=None, _bytes=None) -> data:
        """
        Return data object corresponding to supplied bytes object.
        """
        # Support for constructing a data object using the
        # raw bytes from a valid `oblivious.point` instance.
        # This feature is not part of the public API.
        if a is None and _bytes is not None:
            return bytes.__new__(cls, _bytes)

        if not isinstance(a, (bytes, bytearray, str)):
            raise TypeError('data object must be built from a string or bytes-like object')

        bs = a.encode() if isinstance(a, str) else a
        bs = hashlib.sha512(bs).digest() if len(bs) != 64 else bs

        return bytes.__new__(cls, oblivious.pnt(bs))

class mask(oblivious.scalar):
    """
    Wrapper class for a bytes-like object that corresponds
    to a mask.
    """

    def __new__(cls, bs: bytes = None) -> mask:
        """
        Return either a random mask or a mask corresponding
        to supplied bytes object if it is a valid scalar.

        >>> (len(mask()), len(mask().hex()))
        (32, 64)
        >>> mask(bytes([
        ...     183, 181, 221, 92, 201, 133, 175, 49, 189, 196, 20, 62, 112, 237, 231,
        ...     248, 9, 156, 251, 1, 237, 58, 238, 27, 225, 61, 192, 168, 3, 119, 123, 4
        ... ])).hex()
        'b7b5dd5cc985af31bdc4143e70ede7f8099cfb01ed3aee1be13dc0a803777b04'
        >>> mask(bytes([123]))
        Traceback (most recent call last):
          ...
        ValueError: supplied bytes-like object is not a valid mask
        >>> mask(bytes([123]*32))
        Traceback (most recent call last):
          ...
        ValueError: supplied bytes-like object is not a valid mask
        >>> mask([1, 2, 3])
        Traceback (most recent call last):
          ...
        TypeError: mask object must be built from a bytes-like object
        """
        if bs is not None:
            if not isinstance(bs, (bytes, bytearray)):
                raise TypeError('mask object must be built from a bytes-like object')
            if len(bs) != 32:
                raise ValueError('supplied bytes-like object is not a valid mask')

        bs = oblivious.rnd() if bs is None else oblivious.scl(bs)
        if bs is None:
            raise ValueError('supplied bytes-like object is not a valid mask')

        return bytes.__new__(cls, bs)

    def mask(self: mask, d: data) -> data:
        """
        Mask a value with this mask.

        >>> m = mask(bytes([
        ...     183, 181, 221, 92, 201, 133, 175, 49, 189, 196, 20, 62, 112, 237, 231,
        ...     248, 9, 156, 251, 1, 237, 58, 238, 27, 225, 61, 192, 168, 3, 119, 123, 4
        ... ]))
        >>> n = mask(bytes([
        ...     60, 242, 55, 252, 183, 112, 192, 158, 224, 1, 235, 184, 1, 203, 244, 93,
        ...     186, 20, 154, 245, 60, 116, 11, 209, 153, 214, 144, 220, 136, 122, 161, 4
        ... ]))
        >>> d = data('abc')
        >>> m.mask(d).hex()
        '126713b2598274c5a67968b4f33b933f46f89a622c32188af11936560e886e7b'
        >>> m.mask(n.mask(d)) == n.mask(m.mask(d))
        True
        """
        return data(_bytes=oblivious.mul(self, d))

    def unmask(self: mask, d: data) -> data:
        """
        Unmask a value that has previously been masked with this mask.

        >>> m = mask(bytes([
        ...     183, 181, 221, 92, 201, 133, 175, 49, 189, 196, 20, 62, 112, 237, 231,
        ...     248, 9, 156, 251, 1, 237, 58, 238, 27, 225, 61, 192, 168, 3, 119, 123, 4
        ... ]))
        >>> n = mask(bytes([
        ...     60, 242, 55, 252, 183, 112, 192, 158, 224, 1, 235, 184, 1, 203, 244, 93,
        ...     186, 20, 154, 245, 60, 116, 11, 209, 153, 214, 144, 220, 136, 122, 161, 4
        ... ]))
        >>> d = data('abc')
        >>> m.mask(d).hex()
        '126713b2598274c5a67968b4f33b933f46f89a622c32188af11936560e886e7b'
        >>> d == m.unmask(m.mask(d))
        True
        >>> n.mask(d) == m.unmask(n.mask(m.mask(d)))
        True
        """
        return data(_bytes=oblivious.mul(oblivious.inv(self), d))

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
