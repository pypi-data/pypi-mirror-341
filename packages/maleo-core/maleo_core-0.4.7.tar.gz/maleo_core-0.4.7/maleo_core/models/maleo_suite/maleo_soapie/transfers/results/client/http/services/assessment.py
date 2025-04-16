from __future__ import annotations
from maleo_core.models.base.transfers.results.clients.http.service import BaseHTTPClientServiceResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.assessment import MaleoSOAPIEAssessmentQueryResults

class MaleoSOAPIEHTTPClientAssessmentServiceResults:
    Fail = BaseHTTPClientServiceResults.Fail

    class SingleData(BaseHTTPClientServiceResults.SingleData):
        data:MaleoSOAPIEAssessmentQueryResults.Get

    class MultipleData(BaseHTTPClientServiceResults.MultipleData):
        data:list[MaleoSOAPIEAssessmentQueryResults.Get]