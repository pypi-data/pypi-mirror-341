from __future__ import annotations
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.assessment import MaleoSOAPIEAssessmentGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.diagnosis import MaleoSOAPIEDiagnosisGeneralTransfers

class MaleoSOAPIEDiagnosisQueryResults:
    class Get(
        MaleoSOAPIEDiagnosisGeneralTransfers.Base,
        MaleoSOAPIEAssessmentGeneralTransfers.AssessmentID,
        BaseServiceQueryResults.Get
    ): pass

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoSOAPIEDiagnosisQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoSOAPIEDiagnosisQueryResults.Get]