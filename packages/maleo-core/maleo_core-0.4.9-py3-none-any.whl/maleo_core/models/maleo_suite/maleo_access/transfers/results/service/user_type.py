from __future__ import annotations
from typing import Optional
from maleo_core.models.base.transfers.results.services.general import BaseServiceGeneralResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user_type import MaleoAccessUserTypeQueryResults

class MaleoAccessUserTypeServiceResults:
    Fail = BaseServiceGeneralResults.Fail

    class SingleData(BaseServiceGeneralResults.SingleData):
        data:Optional[MaleoAccessUserTypeQueryResults.Get]

    class MultipleData(BaseServiceGeneralResults.MultipleData):
        data:list[MaleoAccessUserTypeQueryResults.Get]