# This file serves all MaleoSecurity's General Transfers

from __future__ import annotations
from .secret import MaleoSecuritySecretGeneralTransfers
from .encryption import MaleoSecurityEncryptionGeneralTransfers
from .hash import MaleoSecurityHashGeneralTransfers
from .signature import MaleoSecuritySignatureGeneralTransfers
from .token import MaleoSecurityTokenGeneralTransfers

class MaleoSecurityGeneralTransfers:
    Secret = MaleoSecuritySecretGeneralTransfers
    Encryption = MaleoSecurityEncryptionGeneralTransfers
    Hash = MaleoSecurityHashGeneralTransfers
    Signature = MaleoSecuritySignatureGeneralTransfers
    Token = MaleoSecurityTokenGeneralTransfers

__all__ = [
    "MaleoSecurityGeneralTransfers",
    "MaleoSecuritySecretGeneralTransfers",
    "MaleoSecurityEncryptionGeneralTransfers",
    "MaleoSecurityHashGeneralTransfers",
    "MaleoSecuritySignatureGeneralTransfers",
    "MaleoSecurityTokenGeneralTransfers"
]