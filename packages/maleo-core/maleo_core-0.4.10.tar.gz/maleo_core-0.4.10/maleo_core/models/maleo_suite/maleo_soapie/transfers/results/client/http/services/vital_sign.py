from __future__ import annotations
from maleo_core.models.base.transfers.results.clients.http.service import BaseHTTPClientServiceResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.vital_sign import MaleoSOAPIEVitalSignQueryResults

class MaleoSOAPIEHTTPClientVitalSignServiceResults:
    Fail = BaseHTTPClientServiceResults.Fail

    class SingleData(BaseHTTPClientServiceResults.SingleData):
        data:MaleoSOAPIEVitalSignQueryResults.Get

    class MultipleData(BaseHTTPClientServiceResults.MultipleData):
        data:list[MaleoSOAPIEVitalSignQueryResults.Get]