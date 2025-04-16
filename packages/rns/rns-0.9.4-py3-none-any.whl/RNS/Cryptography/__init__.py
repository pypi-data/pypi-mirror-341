# MIT License
#
# Copyright (c) 2022-2025 Mark Qvist / unsigned.io
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import glob

from .Hashes import sha256
from .Hashes import sha512
from .HKDF import hkdf
from .PKCS7 import PKCS7
from .Token import Token
from .Provider import backend

import RNS.Cryptography.Provider as cp

if cp.PROVIDER == cp.PROVIDER_INTERNAL:
    from RNS.Cryptography.X25519 import X25519PrivateKey, X25519PublicKey
    from RNS.Cryptography.Ed25519 import Ed25519PrivateKey, Ed25519PublicKey

elif cp.PROVIDER == cp.PROVIDER_PYCA:
    from RNS.Cryptography.Proxies import X25519PrivateKeyProxy as X25519PrivateKey
    from RNS.Cryptography.Proxies import X25519PublicKeyProxy as X25519PublicKey
    from RNS.Cryptography.Proxies import Ed25519PrivateKeyProxy as Ed25519PrivateKey
    from RNS.Cryptography.Proxies import Ed25519PublicKeyProxy as Ed25519PublicKey

py_modules  = glob.glob(os.path.dirname(__file__)+"/*.py")
pyc_modules = glob.glob(os.path.dirname(__file__)+"/*.pyc")
modules     = py_modules+pyc_modules
__all__ = list(set([os.path.basename(f).replace(".pyc", "").replace(".py", "") for f in modules if not (f.endswith("__init__.py") or f.endswith("__init__.pyc"))]))