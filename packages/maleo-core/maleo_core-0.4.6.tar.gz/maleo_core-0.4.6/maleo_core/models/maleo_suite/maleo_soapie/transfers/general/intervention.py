from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class MaleoSOAPIEInterventionGeneralTransfers:
    class Base(BaseModel):
        overall:str = Field(..., description="Overall intervention")
        other_information:Optional[str] = Field(None, description="Other information")