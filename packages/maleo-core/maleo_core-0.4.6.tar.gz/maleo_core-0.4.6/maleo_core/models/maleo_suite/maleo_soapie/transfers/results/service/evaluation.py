from __future__ import annotations
from typing import Optional
from maleo_core.models.base.transfers.results.services.general import BaseServiceGeneralResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.evaluation import MaleoSOAPIEEvaluationQueryResults

class MaleoSOAPIEEvaluationServiceResults:
    Fail = BaseServiceGeneralResults.Fail

    class SingleData(BaseServiceGeneralResults.SingleData):
        data:Optional[MaleoSOAPIEEvaluationQueryResults.Get]

    class MultipleData(BaseServiceGeneralResults.MultipleData):
        data:list[MaleoSOAPIEEvaluationQueryResults.Get]