from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Optional
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.diagnosis import MaleoSOAPIEDiagnosisGeneralTransfers

class MaleoSOAPIEAssessmentGeneralTransfers:
    class ExpandableFields(StrEnum):
        DIAGNOSES = "diagnoses"

    class AssessmentID(BaseModel):
        assessment_id:int = Field(..., ge=1, description="Assessment's id")

    class AssessmentIDs(BaseModel):
        assessment_ids:Optional[list[int]] = Field(None, description="Specific Assessment IDs")

    class Base(BaseModel):
        overall:str = Field(..., description="Overall assessment")
        diagnoses:list[MaleoSOAPIEDiagnosisGeneralTransfers.Base] = Field([], description="Diagnoses")
        other_information:Optional[str] = Field(None, description="Other information")