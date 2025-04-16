# This file serves all MaleoSecurity's General Results

from __future__ import annotations
from .key import MaleoSecurityKeyGeneralResults
from .encryption import MaleoSecurityEncryptionGeneralResults
from .hash import MaleoSecurityHashGeneralResults
from .signature import MaleoSecuritySignatureGeneralResults
from .token import MaleoSecurityTokenGeneralResults

class MaleoSecurityGeneralResults:
    Key = MaleoSecurityKeyGeneralResults
    Encryption = MaleoSecurityEncryptionGeneralResults
    Hash = MaleoSecurityHashGeneralResults
    Signature = MaleoSecuritySignatureGeneralResults
    Token = MaleoSecurityTokenGeneralResults

__all__ = [
    "MaleoSecurityGeneralResults",
    "MaleoSecurityKeyGeneralResults",
    "MaleoSecurityEncryptionGeneralResults",
    "MaleoSecuritySignatureGeneralResults",
    "MaleoSecurityTokenGeneralResults"
]