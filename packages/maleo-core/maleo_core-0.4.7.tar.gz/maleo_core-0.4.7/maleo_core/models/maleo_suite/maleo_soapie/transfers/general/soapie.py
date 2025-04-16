from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Optional
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.subjective import MaleoSOAPIESubjectiveGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.objective import MaleoSOAPIEObjectiveGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.assessment import MaleoSOAPIEAssessmentGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.plan import MaleoSOAPIEPlanGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.intervention import MaleoSOAPIEInterventionGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.evaluation import MaleoSOAPIEEvaluationGeneralTransfers

class MaleoSOAPIESOAPIEGeneralTransfers:
    class SOAPIEID (BaseModel):
        soapie_id:int = Field(..., ge=1, description="SOAPIE's id")

    class SOAPIEIDs(BaseModel):
        soapie_ids:Optional[list[int]] = Field(None, description="Specific SOAPIE IDs")

    class ExpandableFields(StrEnum):
        SUBJECTIVE = "subjective"
        OBJECTIVE = "objective"
        VITAL_SIGN = "objective.vital_sign"
        ASSESSMENT = "assessment"
        DIAGNOSES = "assessment.diagnoses"
        PLAN = "plan"
        INTERVENTION = "intervention"
        EVALUATION = "evaluation"

    class Base(BaseModel):
        subjective:Optional[MaleoSOAPIESubjectiveGeneralTransfers.Base] = Field(None, description="Subjective")
        objective:Optional[MaleoSOAPIEObjectiveGeneralTransfers.Base] = Field(None, description="Objective")
        assessment:Optional[MaleoSOAPIEAssessmentGeneralTransfers.Base] = Field(None, description="Assessment")
        plan:Optional[MaleoSOAPIEPlanGeneralTransfers.Base] = Field(None, description="Plan")
        intervention:Optional[MaleoSOAPIEInterventionGeneralTransfers.Base] = Field(None, description="Intervention")
        evaluation:Optional[MaleoSOAPIEEvaluationGeneralTransfers.Base] = Field(None, description="Evaluation")