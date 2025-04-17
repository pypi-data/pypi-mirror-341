from __future__ import annotations
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.objective import MaleoSOAPIEObjectiveGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.vital_sign import MaleoSOAPIEVitalSignGeneralTransfers

class MaleoSOAPIEVitalSignQueryResults:
    class Get(
        MaleoSOAPIEVitalSignGeneralTransfers.Base,
        MaleoSOAPIEObjectiveGeneralTransfers.ObjectiveID,
        BaseServiceQueryResults.Get
    ): pass

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoSOAPIEVitalSignQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoSOAPIEVitalSignQueryResults.Get]