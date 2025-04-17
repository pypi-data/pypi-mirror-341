from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.soapie import MaleoSOAPIESOAPIEGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.assessment import MaleoSOAPIEAssessmentGeneralParameters

class MaleoSOAPIEAssessmentClientParameters:
    class Get(
        MaleoSOAPIEAssessmentGeneralParameters.Expand,
        MaleoSOAPIESOAPIEGeneralTransfers.SOAPIEIDs,
        BaseClientParameters.Get,
        BaseGeneralParameters.IDs
    ): pass

    class GetQuery(
        MaleoSOAPIEAssessmentGeneralParameters.Expand,
        MaleoSOAPIESOAPIEGeneralTransfers.SOAPIEIDs,
        BaseClientParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass