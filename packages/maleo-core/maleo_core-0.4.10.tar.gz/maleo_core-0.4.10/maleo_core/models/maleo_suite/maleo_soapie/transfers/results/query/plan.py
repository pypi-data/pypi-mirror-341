from __future__ import annotations
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.soapie import MaleoSOAPIESOAPIEGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.plan import MaleoSOAPIEPlanGeneralTransfers

class MaleoSOAPIEPlanQueryResults:
    class Get(
        MaleoSOAPIEPlanGeneralTransfers.Base,
        MaleoSOAPIESOAPIEGeneralTransfers.SOAPIEID,
        BaseServiceQueryResults.Get
    ): pass

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoSOAPIEPlanQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoSOAPIEPlanQueryResults.Get]