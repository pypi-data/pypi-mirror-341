from __future__ import annotations
from fastapi import status
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.maleo_suite.maleo_access.transfers.results.service.authorization import MaleoAccessAuthorizationServiceResults

class MaleoAccessAuthorizationServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class FailResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "ACC-ATH-001"
        message:str = "Authorization Failed"
        description:str = "External error: Authorization failed"
        other:str = "Ensure parameter(s) are correct"

    class LoginResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-ATH-002"
        message:str = "Login Successful"
        description:str = "Login attempt is successful"
        data:MaleoAccessAuthorizationServiceResults.LoginData

    class LogoutResponse(BaseGeneralResponsesSchemas.NoData):
        code:str = "ACC-ATH-003"
        message:str = "Login Failed"
        description:str = "Logout attempt is successful"
        data:None = None

    #* ----- ----- Responses Class ----- ----- *#
    other_responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Fail Response",
            "model": FailResponse
        },
        **BaseGeneralResponsesSchemas.other_responses
    }