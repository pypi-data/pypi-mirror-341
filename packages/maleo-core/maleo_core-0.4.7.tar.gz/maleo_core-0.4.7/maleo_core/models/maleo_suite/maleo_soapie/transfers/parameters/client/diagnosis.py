from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.assessment import MaleoSOAPIEAssessmentGeneralTransfers

class MaleoSOAPIEDiagnosisClientParameters:
    class Get(
        MaleoSOAPIEAssessmentGeneralTransfers.AssessmentIDs,
        BaseClientParameters.Get,
        BaseGeneralParameters.IDs
    ): pass

    class GetQuery(
        MaleoSOAPIEAssessmentGeneralTransfers.AssessmentIDs,
        BaseClientParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass