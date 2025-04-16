'''
Onetimeauth: secret-key single-message authentication module.
'''

from typing import Tuple as _Tuple
import ctypes as _ct
from ._lib import _lib, _check_input


class Poly1305:
    '''
    Poly1305 one-time authenticator.
    '''

    KEYBYTES = 32
    BYTES = 16

    def __init__(self) -> None:
        '''
        '''
        self._c_auth = getattr(_lib, 'lib1305_onetimeauth_poly1305')
        self._c_auth.argtypes = [_ct.c_char_p,
                                 _ct.c_char_p, _ct.c_longlong, _ct.c_char_p]
        self._c_auth.restype = None
        self._c_verify = getattr(_lib, 'lib1305_onetimeauth_poly1305_verify')
        self._c_verify.argtypes = [_ct.c_char_p,
                                   _ct.c_char_p, _ct.c_longlong, _ct.c_char_p]
        self._c_verify.restype = _ct.c_int

    def auth(self, m: bytes, k: bytes) -> bytes:
        '''
        Auth - generates an authenticator 'a' given a message 'm' and a secret key 'k'.

        Parameters:
            m (bytes): message
            k (bytes): secret key

        Returns:
            a (bytes): authenticator
        '''
        _check_input(m, -1, 'm')
        _check_input(k, self.KEYBYTES, 'k')
        mlen = _ct.c_longlong(len(m))
        m = _ct.create_string_buffer(m)
        k = _ct.create_string_buffer(k)
        a = _ct.create_string_buffer(self.BYTES)
        self._c_auth(a, m, mlen, k)
        return a.raw

    def verify(self, a: bytes, m: bytes, k: bytes) -> None:
        '''
        Verify - verifies an authenticator 'a' given a message 'm' and a secret key 'k'.

        Parameters:
            a (bytes): authenticator
            m (bytes): message
            k (bytes): secret key

        Raises:
            ValueError: an authenticator doesn't match

        Returns:
            None
        '''
        _check_input(a, self.BYTES, 'a')
        _check_input(m, -1, 'm')
        _check_input(k, self.KEYBYTES, 'k')
        mlen = _ct.c_longlong(len(m))
        m = _ct.create_string_buffer(m)
        k = _ct.create_string_buffer(k)
        a = _ct.create_string_buffer(a)
        if self._c_verify(a, m, mlen, k):
            raise ValueError('verify failed')


poly1305 = Poly1305()
