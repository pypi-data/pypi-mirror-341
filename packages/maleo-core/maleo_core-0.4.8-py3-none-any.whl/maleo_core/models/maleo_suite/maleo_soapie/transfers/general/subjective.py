from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class MaleoSOAPIESubjectiveGeneralTransfers:
    class Base(BaseModel):
        chief_complaint:str = Field(..., description="Chief complaint")
        additional_complaint:Optional[str] = Field(None, description="Additional complaint")
        pain_scale:Optional[int] = Field(None, ge=1, le=10, description="Pain scale")
        onset:Optional[str] = Field(None, description="Onset")
        chronology:Optional[str] = Field(None, description="Chronology")
        location:Optional[str] = Field(None, description="Location")
        factor:Optional[str] = Field(None, description="Factor")
        personal_illness_history:Optional[str] = Field(None, description="Personal illness history")
        family_illness_history:Optional[str] = Field(None, description="Family illness history")
        habit_activity_occupation:Optional[str] = Field(None, description="Habit, Activity, and Occupation")
        consumed_medication:Optional[str] = Field(None, description="Consumed medication")
        other_information:Optional[str] = Field(None, description="Other information")