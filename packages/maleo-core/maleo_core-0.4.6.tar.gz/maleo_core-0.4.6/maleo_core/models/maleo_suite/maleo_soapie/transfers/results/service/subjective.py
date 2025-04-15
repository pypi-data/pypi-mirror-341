from __future__ import annotations
from typing import Optional
from maleo_core.models.base.transfers.results.services.general import BaseServiceGeneralResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.subjective import MaleoSOAPIESubjectiveQueryResults

class MaleoSOAPIESubjectiveServiceResults:
    Fail = BaseServiceGeneralResults.Fail

    class SingleData(BaseServiceGeneralResults.SingleData):
        data:Optional[MaleoSOAPIESubjectiveQueryResults.Get]

    class MultipleData(BaseServiceGeneralResults.MultipleData):
        data:list[MaleoSOAPIESubjectiveQueryResults.Get]