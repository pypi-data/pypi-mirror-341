from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.objective import MaleoSOAPIEObjectiveGeneralTransfers

class MaleoSOAPIEVitalSignClientParameters:
    class Get(
        MaleoSOAPIEObjectiveGeneralTransfers.ObjectiveIDs,
        BaseClientParameters.Get,
        BaseGeneralParameters.IDs
    ): pass

    class GetQuery(
        MaleoSOAPIEObjectiveGeneralTransfers.ObjectiveIDs,
        BaseClientParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass