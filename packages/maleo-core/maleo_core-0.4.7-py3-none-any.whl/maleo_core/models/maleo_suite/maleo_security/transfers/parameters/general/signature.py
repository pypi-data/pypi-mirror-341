from __future__ import annotations
from maleo_core.models.base.general import BaseGeneralModels
from maleo_core.models.maleo_suite.maleo_security.transfers.general.signature import MaleoSecuritySignatureGeneralTransfers

class MaleoSecuritySignatureGeneralParameters:
    class SignSingle(
        MaleoSecuritySignatureGeneralTransfers.SingleMessage,
        BaseGeneralModels.PrivateKey
    ): pass

    class SignMultiple(
        MaleoSecuritySignatureGeneralTransfers.MultipleMessages,
        BaseGeneralModels.PrivateKey
    ): pass

    class VerifySingle(
        MaleoSecuritySignatureGeneralTransfers.SingleSignature,
        BaseGeneralModels.PublicKey
    ): pass

    class VerifyMultiple(
        MaleoSecuritySignatureGeneralTransfers.MultipleSignatures,
        BaseGeneralModels.PublicKey
    ): pass