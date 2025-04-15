from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.service import BaseServiceParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.objective import MaleoSOAPIEObjectiveGeneralTransfers

class MaleoSOAPIEVitalSignServiceParameters:
    class GetQuery(
        MaleoSOAPIEObjectiveGeneralTransfers.ObjectiveIDs,
        BaseServiceParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass

    class Get(
        MaleoSOAPIEObjectiveGeneralTransfers.ObjectiveIDs,
        BaseServiceParameters.Get,
        BaseGeneralParameters.IDs
    ): pass