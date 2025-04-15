from typing import Union
from maleo_core.clients.maleo_suite.maleo_security.http.controllers.token import MaleoSecurityTokenHTTPController
from maleo_core.models.maleo_suite.maleo_security.transfers.parameters.general.token import MaleoSecurityTokenGeneralParameters
from maleo_core.models.maleo_suite.maleo_security.transfers.results.general.token import MaleoSecurityTokenGeneralResults

class MaleoSecurityTokenHTTPService:
    @staticmethod
    async def encode(
        parameters:MaleoSecurityTokenGeneralParameters.Encode
    ) -> Union[
        MaleoSecurityTokenGeneralResults.Fail,
        MaleoSecurityTokenGeneralResults.Encode
    ]:
        """Encode a payload"""
        result = await MaleoSecurityTokenHTTPController.encode(parameters=parameters)
        if not result.success:
            return MaleoSecurityTokenGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityTokenGeneralResults.Encode.model_validate(result.content)

    @staticmethod
    async def decode(
        parameters:MaleoSecurityTokenGeneralParameters.Decode
    ) -> Union[
        MaleoSecurityTokenGeneralResults.Fail,
        MaleoSecurityTokenGeneralResults.Decode
    ]:
        """Decode a token"""
        result = await MaleoSecurityTokenHTTPController.decode(parameters=parameters)
        if not result.success:
            return MaleoSecurityTokenGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityTokenGeneralResults.Decode.model_validate(result.content)