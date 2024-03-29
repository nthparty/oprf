"""
Oblivious pseudo-random function (OPRF) protocol functionality implementations
based on `Curve25519 <https://cr.yp.to/ecdh.html>`__ and the
`Ristretto <https://ristretto.group>`__ group.
"""
from __future__ import annotations
from typing import Union, Optional
import doctest
import oblivious

class data(oblivious.ristretto.point):
    """
    Wrapper class for a bytes-like object that corresponds to a piece of data
    that can be masked.
    """
    @classmethod
    def hash(cls, argument: Union[str, bytes]) -> data: # pylint: disable=arguments-renamed
        """
        Return data object constructed by hashing the supplied string or
        bytes-like object.

        >>> data.hash('abc').hex()
        '5a5dbd5c765abf60b2076133482c1ada189c319034ae0b933f4908b3b68d0225'
        >>> data.hash(bytes([123])).hex()
        'be6f2de25b6907d7e07e6a75424c6f4bbed103c2957b9fa9fbe4fd63dfa5575b'
        >>> data.hash([1, 2, 3])
        Traceback (most recent call last):
          ...
        TypeError: can only hash a string or bytes-like object to a data object
        """
        if not isinstance(argument, (bytes, bytearray, str)):
            raise TypeError(
                'can only hash a string or bytes-like object to a data object'
            )

        argument = argument.encode() if isinstance(argument, str) else argument
        return bytes.__new__(cls, oblivious.ristretto.point.hash(argument))

    @classmethod
    def from_base64(cls, s: str) -> data:
        """
        Convert Base64 UTF-8 string representation of a data instance to a data
        object.

        >>> d = data.hash('abc')
        >>> data.from_base64(d.to_base64()) == d
        True
        """
        return bytes.__new__(cls, oblivious.ristretto.point.from_base64(s))

    def __new__(cls, bs: Optional[bytes] = None) -> data:
        """
        Return data object corresponding to the supplied bytes-like object. No
        checks are performed to confirm that the bytes-like object is a valid
        representation of a data object.

        >>> d = data.hash('abc')
        >>> bs = bytes(d)
        >>> data(bs) == d
        True
        """
        return bytes.__new__(cls, oblivious.ristretto.point(bs))

    def __truediv__(self: data, argument: mask) -> data:
        """
        Unmask this data object (assuming it has previously been masked with
        the supplied mask).

        >>> d = data.hash('abc')
        >>> m = mask.hash('abc')
        >>> ((m(d)) / m) == d
        True
        """
        return data((~argument) * self)

    def to_base64(self: data) -> str:
        """
        Convert to Base64 UTF-8 string representation.

        >>> d = data.hash('abc')
        >>> d.to_base64()
        'Wl29XHZav2CyB2EzSCwa2hicMZA0rguTP0kIs7aNAiU='
        """
        return oblivious.ristretto.point(self).to_base64()

class mask(oblivious.ristretto.scalar):
    """
    Wrapper class for a bytes-like object that corresponds to a mask.
    """
    @classmethod
    def random(cls) -> mask:
        """
        Return random non-zero mask object.

        >>> m = mask.random()
        >>> len(m) == 32 and oblivious.ristretto.scalar(m) == m
        True
        """
        return bytes.__new__(cls, oblivious.ristretto.scalar())

    @classmethod
    def hash(cls, argument: Union[str, bytes]) -> mask: # pylint: disable=arguments-renamed
        """
        Return mask object constructed by hashing the supplied string or bytes-like
        object.

        >>> mask.hash('abc').hex()
        'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f200150d'
        >>> mask.hash(bytes([123])).hex()
        '904ea0ec29650f3b2bcf481e3ea2553488030c865aae2decba8ce7016c4e380c'
        >>> mask.hash([1, 2, 3])
        Traceback (most recent call last):
          ...
        TypeError: can only hash a string or bytes-like object to a mask object
        """
        if not isinstance(argument, (bytes, bytearray, str)):
            raise TypeError(
                'can only hash a string or bytes-like object to a mask object'
            )

        argument = argument.encode() if isinstance(argument, str) else argument
        return bytes.__new__(cls, oblivious.ristretto.scalar.hash(argument))

    @classmethod
    def from_base64(cls, s: str) -> mask:
        """
        Convert Base64 UTF-8 string representation of a mask instance to a
        mask object.

        >>> m = mask.hash('abc')
        >>> mask.from_base64(m.to_base64()) == m
        True
        """
        return bytes.__new__(cls, oblivious.ristretto.scalar.from_base64(s))

    def __new__(cls, bs: Optional[bytes] = None) -> mask:
        """
        Return mask object corresponding to the supplied bytes-like object. No
        checks are performed to confirm that the bytes-like object is a valid
        representation of a mask object.

        >>> m = mask()
        >>> bs = bytes(m)
        >>> mask(bs) == m
        True
        """
        return bytes.__new__(cls, oblivious.ristretto.scalar(bs))

    def __invert__(self: mask) -> mask:
        """
        Return the inverse of this mask instance.

        >>> m = mask.hash('abc')
        >>> (~m).hex()
        '9d7c69e8dded15ba20544cee233db3148481e713863ddcf0dff9d56470ba8501'
        >>> d = data.hash('abc')
        >>> (~m)(m(d)) == d
        True
        >>> m((~m)(d)) == d
        True
        """
        return mask(~oblivious.ristretto.scalar(self))

    def mask(self: mask, argument: data) -> data:
        """
        Mask a :obj:`data` object with this mask and return the masked data
        object.

        >>> d = data.hash('abc')
        >>> m = mask.hash('abc')
        >>> m.mask(d).hex()
        'f47c8267b28ac5100e0e97b36190e16d4533b367262557a5aa7d97b811344d15'
        """
        return data(oblivious.ristretto.scalar(self) * argument)

    def __call__(self: mask, argument: data) -> data:
        """
        Mask a :obj:`data` object with this mask and return the masked data
        object.

        >>> d = data.hash('abc')
        >>> m = mask.hash('abc')
        >>> m(d).hex()
        'f47c8267b28ac5100e0e97b36190e16d4533b367262557a5aa7d97b811344d15'
        """
        return data(oblivious.ristretto.scalar(self) * argument)

    def __mul__(self: mask, argument: data) -> data:
        """
        Mask a :obj:`data` object with this mask and return the masked data
        object.

        >>> d = data.hash('abc')
        >>> m = mask.hash('abc')
        >>> (m * d).hex()
        'f47c8267b28ac5100e0e97b36190e16d4533b367262557a5aa7d97b811344d15'
        """
        return data(oblivious.ristretto.scalar(self) * argument)

    def unmask(self: mask, argument: data) -> data:
        """
        Unmask a :obj:`data` object that has previously been masked with this
        mask (and return the original :obj:`data` object).

        >>> d = data.hash('abc')
        >>> m = mask.hash('abc')
        >>> m.unmask(m(d)) == d
        True
        """
        return data(oblivious.ristretto.scalar(~self) * argument)

    def to_base64(self: mask) -> str:
        """
        Convert to Base64 UTF-8 string representation.

        >>> m = mask.hash('abc')
        >>> m.to_base64()
        'ungWv48Bz+pBQUDeXa4iI7ADYaOWF3qctBD/YfIAFQ0='
        """
        return oblivious.ristretto.scalar(self).to_base64()

if __name__ == '__main__':
    doctest.testmod() # pragma: no cover
