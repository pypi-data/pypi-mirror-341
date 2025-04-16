from __future__ import annotations
from pydantic import Field
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.soapie import MaleoSOAPIESOAPIEGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.objective import MaleoSOAPIEObjectiveGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.vital_sign import MaleoSOAPIEVitalSignQueryResults

class MaleoSOAPIEObjectiveQueryResults:
    class Get(
        MaleoSOAPIEObjectiveGeneralTransfers.Base,
        MaleoSOAPIESOAPIEGeneralTransfers.SOAPIEID,
        BaseServiceQueryResults.Get
    ):
        vital_sign:Optional[MaleoSOAPIEVitalSignQueryResults.Get] = Field(None, description="Vital Sign")

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoSOAPIEObjectiveQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoSOAPIEObjectiveQueryResults.Get]