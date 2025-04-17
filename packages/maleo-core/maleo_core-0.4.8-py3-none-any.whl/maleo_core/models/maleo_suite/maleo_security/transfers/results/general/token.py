from __future__ import annotations
from maleo_core.models.base.transfers.results.general import BaseGeneralResults
from maleo_core.models.maleo_suite.maleo_security.transfers.general.token import MaleoSecurityTokenGeneralTransfers

class MaleoSecurityTokenGeneralResults:
    Fail = BaseGeneralResults.Fail

    class Encode(BaseGeneralResults.SingleData):
        data:MaleoSecurityTokenGeneralTransfers.Token

    class Decode(BaseGeneralResults.SingleData):
        data:MaleoSecurityTokenGeneralTransfers.Payload