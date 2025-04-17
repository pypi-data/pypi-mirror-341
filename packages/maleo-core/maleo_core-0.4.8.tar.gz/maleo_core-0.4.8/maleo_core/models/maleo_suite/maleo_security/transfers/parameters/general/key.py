from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_core.models.base.general import BaseGeneralModels

class MaleoSecurityKeyGeneralParameters:
    class GeneratePairOrPrivate(BaseModel):
        key_size:int = Field(2048, ge=1024, description="Key's size")

    class GeneratePublic(BaseGeneralModels.PrivateKey): pass