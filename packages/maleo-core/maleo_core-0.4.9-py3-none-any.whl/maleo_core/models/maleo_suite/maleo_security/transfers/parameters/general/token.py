from __future__ import annotations
from maleo_core.models.base.general import BaseGeneralModels
from maleo_core.models.maleo_suite.maleo_security.transfers.general.token import MaleoSecurityTokenGeneralTransfers

class MaleoSecurityTokenGeneralParameters:
    class Encode(MaleoSecurityTokenGeneralTransfers.Payload, BaseGeneralModels.PrivateKey): pass
    class Decode(MaleoSecurityTokenGeneralTransfers.Token, BaseGeneralModels.PublicKey): pass