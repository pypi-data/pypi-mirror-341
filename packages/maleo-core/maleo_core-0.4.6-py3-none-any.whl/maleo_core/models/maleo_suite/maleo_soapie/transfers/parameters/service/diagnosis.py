from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.service import BaseServiceParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.assessment import MaleoSOAPIEAssessmentGeneralTransfers

class MaleoSOAPIEDiagnosisServiceParameters:
    class GetQuery(
        MaleoSOAPIEAssessmentGeneralTransfers.AssessmentIDs,
        BaseServiceParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass

    class Get(
        MaleoSOAPIEAssessmentGeneralTransfers.AssessmentIDs,
        BaseServiceParameters.Get,
        BaseGeneralParameters.IDs
    ): pass