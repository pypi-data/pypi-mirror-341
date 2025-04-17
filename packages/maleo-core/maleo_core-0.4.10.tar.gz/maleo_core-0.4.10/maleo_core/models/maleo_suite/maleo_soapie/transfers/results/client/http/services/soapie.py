from __future__ import annotations
from maleo_core.models.base.transfers.results.clients.http.service import BaseHTTPClientServiceResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.soapie import MaleoSOAPIESOAPIEQueryResults

class MaleoSOAPIEHTTPClientSOAPIEServiceResults:
    Fail = BaseHTTPClientServiceResults.Fail

    class SingleData(BaseHTTPClientServiceResults.SingleData):
        data:MaleoSOAPIESOAPIEQueryResults.Get

    class MultipleData(BaseHTTPClientServiceResults.MultipleData):
        data:list[MaleoSOAPIESOAPIEQueryResults.Get]