from __future__ import annotations
from maleo_core.models.base.general import BaseGeneralModels
from maleo_core.models.base.transfers.results.general import BaseGeneralResults

class MaleoSecurityKeyGeneralResults:
    Fail = BaseGeneralResults.Fail

    class SinglePrivate(BaseGeneralResults.SingleData):
        data:BaseGeneralModels.PrivateKey

    class SinglePublic(BaseGeneralResults.SingleData):
        data:BaseGeneralModels.PublicKey

    class SinglePair(BaseGeneralResults.SingleData):
        data:BaseGeneralModels.KeyPair