from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_core.models.base.general import BaseGeneralModels

class MaleoSecurityTokenGeneralTransfers:
    class Payload(BaseModel):
        payload:BaseGeneralModels.TokenPayload = Field(..., description="Token payload")

    class Token(BaseModel):
        token:str = Field(..., description="Token string")