from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_core.models.base.general import BaseGeneralModels
from maleo_core.models.maleo_suite.maleo_security.transfers.general.encryption.rsa import MaleoSecurityRSAEncryptionGeneralTransfers

class MaleoSecurityRSAEncryptionGeneralParameters:
    class EncryptSingle(
        MaleoSecurityRSAEncryptionGeneralTransfers.SinglePlain,
        BaseGeneralModels.PublicKey
    ): pass

    class EncryptMultiple(
        MaleoSecurityRSAEncryptionGeneralTransfers.MultiplePlains,
        BaseGeneralModels.PublicKey
    ): pass

    class DecryptSingle(
        MaleoSecurityRSAEncryptionGeneralTransfers.SingleCipher,
        BaseGeneralModels.PrivateKey
    ): pass

    class DecryptMultiple(
        MaleoSecurityRSAEncryptionGeneralTransfers.MultipleCiphers,
        BaseGeneralModels.PrivateKey
    ): pass