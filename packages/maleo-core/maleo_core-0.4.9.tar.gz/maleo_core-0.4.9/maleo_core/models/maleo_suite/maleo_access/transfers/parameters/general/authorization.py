from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Optional

class MaleoAccessAuthorizationGeneralParameters:
    class IdentifierType(StrEnum):
        USERNAME = "username"
        EMAIL = "email"
        PHONE = "phone"

    class Login(BaseModel):
        system_role_id:int = Field(..., description="System role's ID")
        organization_key:Optional[str] = Field(..., description="Organization's Key")
        identifier_type:MaleoAccessAuthorizationGeneralParameters.IdentifierType = Field(..., description="Identifier")
        identifier:str = Field(..., description="Identifier")
        password:str = Field(..., description="Password")