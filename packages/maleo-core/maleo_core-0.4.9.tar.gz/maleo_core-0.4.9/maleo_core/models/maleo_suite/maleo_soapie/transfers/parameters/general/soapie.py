from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel, Field
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.soapie import MaleoSOAPIESOAPIEGeneralTransfers

class MaleoSOAPIESOAPIEGeneralParameters:
    class ExpandableFields(StrEnum):
        SUBJECTIVE = "subjective"
        OBJECTIVE = "objective"
        VITAL_SIGN = "objective.vital_sign"
        ASSESSMENT = "assessment"
        DIAGNOSES = "assessment.diagnoses"
        PLAN = "plan"
        INTERVENTION = "intervention"
        EVALUATION = "evaluation"

    class Expand(BaseModel):
        expand:list[MaleoSOAPIESOAPIEGeneralTransfers.ExpandableFields] = Field([], description="Expanded field(s)")

    class UniqueIdentifiers(StrEnum):
        ID = "id"
        UUID = "uuid"

    class GetSingle(Expand, BaseGeneralParameters.GetSingle):
        identifier:MaleoSOAPIESOAPIEGeneralParameters.UniqueIdentifiers = Field(..., description="Identifier")

    class GetSingleQuery(Expand, BaseGeneralParameters.GetSingleQuery): pass

    class BaseCreateOrUpdate(MaleoSOAPIESOAPIEGeneralTransfers.Base): pass

    class CreateOrUpdate(Expand, BaseCreateOrUpdate): pass