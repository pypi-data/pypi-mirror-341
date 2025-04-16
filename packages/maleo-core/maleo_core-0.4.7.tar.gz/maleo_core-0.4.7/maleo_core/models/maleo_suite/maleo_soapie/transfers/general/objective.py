from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Optional
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.vital_sign import MaleoSOAPIEVitalSignGeneralTransfers

class MaleoSOAPIEObjectiveGeneralTransfers:
    class ExpandableFields(StrEnum):
        VITAL_SIGN = "vital_sign"

    class ObjectiveID(BaseModel):
        objective_id:int = Field(..., ge=1, description="Objective's id")

    class ObjectiveIDs(BaseModel):
        objective_ids:Optional[list[int]] = Field(None, description="Specific Objective IDs")

    class Base(BaseModel):
        overall:str = Field(..., description="Overall objective")
        vital_sign:Optional[MaleoSOAPIEVitalSignGeneralTransfers.Base] = Field(None, description="Vital Sign")
        other_information:Optional[str] = Field(None, description="Other information")