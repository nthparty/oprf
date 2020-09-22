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
        """
        return data(_bytes=oblivious.mul(self, d))

    def unmask(self: mask, d: data) -> data:
        """
        Unmask a value that has previously been masked with this mask.
        """
        return data(_bytes=oblivious.mul(oblivious.inv(self), d))

if __name__ == "__main__":
    doctest.testmod()
