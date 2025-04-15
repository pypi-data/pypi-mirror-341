from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.soapie import MaleoSOAPIESOAPIEGeneralParameters

class MaleoSOAPIESOAPIEClientParameters:
    class Get(
        MaleoSOAPIESOAPIEGeneralParameters.Expand,
        BaseClientParameters.Get,
        BaseGeneralParameters.IDs
    ): pass

    class GetQuery(
        MaleoSOAPIESOAPIEGeneralParameters.Expand,
        BaseClientParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass