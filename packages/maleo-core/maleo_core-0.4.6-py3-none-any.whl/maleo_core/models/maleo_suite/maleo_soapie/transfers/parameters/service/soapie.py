from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.service import BaseServiceParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.soapie import MaleoSOAPIESOAPIEGeneralParameters

class MaleoSOAPIESOAPIEServiceParameters:
    class GetQuery(
        MaleoSOAPIESOAPIEGeneralParameters.Expand,
        BaseServiceParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass

    class Get(
        MaleoSOAPIESOAPIEGeneralParameters.Expand,
        BaseServiceParameters.Get,
        BaseGeneralParameters.IDs
    ): pass