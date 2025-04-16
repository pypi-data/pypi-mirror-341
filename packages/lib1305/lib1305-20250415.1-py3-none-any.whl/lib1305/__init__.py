'''
Python wrapper around implementation of the Poly1305 one-time authenticator.

Import library:

    from lib1305 import poly1305

Authenticating a message:

    a = poly1305.auth(m, k)

Verifying an authenticator:

    poly1305.verify(a, m, k)

The poly1305.auth function generates an 128-bit authenticator 'a' given
a message 'm' and a 256-bit secret key 'k'. "One-time" means that the secret
key must not be reused to generate an authenticator of another message.

The poly1305.verify function verifies an 128-bit authenticator 'a' given
a messagea 'm' and a 256-bit secret key 'k'.
It raises an exception if the authenticator is not valid.
'''

from .onetimeauth import poly1305
