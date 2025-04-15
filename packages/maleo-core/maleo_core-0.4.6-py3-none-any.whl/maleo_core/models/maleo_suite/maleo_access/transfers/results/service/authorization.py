from __future__ import annotations
from pydantic import BaseModel
from maleo_core.models.base.transfers.results.services.general import BaseServiceGeneralResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.general.authorization import MaleoAccessAuthorizationGeneralResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user import MaleoAccessUserQueryResults

class MaleoAccessAuthorizationServiceResults:
    Fail = BaseServiceGeneralResults.Fail

    class GenerateLoginTokens(BaseServiceGeneralResults.SingleData):
        data:MaleoAccessAuthorizationGeneralResults.LoginTokens

    class LoginData(BaseModel):
        base:MaleoAccessAuthorizationGeneralResults.BaseLoginData
        user:MaleoAccessUserQueryResults.Get

    class Login(BaseServiceGeneralResults.SingleData):
        data:MaleoAccessAuthorizationServiceResults.LoginData

    class Logout(BaseServiceGeneralResults.SingleData):
        data:None