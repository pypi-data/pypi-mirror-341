from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.service import BaseServiceParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.soapie import MaleoSOAPIESOAPIEGeneralTransfers

class MaleoSOAPIEInterventionServiceParameters:
    class GetQuery(
        MaleoSOAPIESOAPIEGeneralTransfers.SOAPIEIDs,
        BaseServiceParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass

    class Get(
        MaleoSOAPIESOAPIEGeneralTransfers.SOAPIEIDs,
        BaseServiceParameters.Get,
        BaseGeneralParameters.IDs
    ): pass