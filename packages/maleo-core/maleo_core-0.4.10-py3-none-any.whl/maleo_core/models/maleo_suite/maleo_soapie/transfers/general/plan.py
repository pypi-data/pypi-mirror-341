from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class MaleoSOAPIEPlanGeneralTransfers:
    class Base(BaseModel):
        overall:str = Field(..., description="Overall plan")
        other_information:Optional[str] = Field(None, description="Other information")