from __future__ import annotations
from enum import StrEnum
from pydantic import Field
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.assessment import MaleoSOAPIEAssessmentGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.diagnosis import MaleoSOAPIEDiagnosisGeneralTransfers

class MaleoSOAPIEDiagnosisGeneralParameters:
    class UniqueIdentifiers(StrEnum):
        ID = "id"
        UUID = "uuid"

    class GetSingle(BaseGeneralParameters.GetSingle):
        identifier:MaleoSOAPIEDiagnosisGeneralParameters.UniqueIdentifiers = Field(..., description="Identifier")

    class CreateOrUpdate(
        MaleoSOAPIEDiagnosisGeneralTransfers.Base,
        MaleoSOAPIEAssessmentGeneralTransfers.AssessmentID
    ): pass