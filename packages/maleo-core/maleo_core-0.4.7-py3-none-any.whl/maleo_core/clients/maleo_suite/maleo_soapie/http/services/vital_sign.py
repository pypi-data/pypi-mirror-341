from typing import Union
from maleo_core.clients.maleo_suite.maleo_soapie.http.controllers.vital_sign import MaleoSOAPIEVitalSignHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.client.vital_sign import MaleoSOAPIEVitalSignClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.vital_sign import MaleoSOAPIEVitalSignGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.client.http.services.vital_sign import MaleoSOAPIEHTTPClientVitalSignServiceResults

class MaleoSOAPIEVitalSignHTTPService:
    @staticmethod
    async def get_vital_signs(
        parameters:MaleoSOAPIEVitalSignClientParameters.Get
    ) -> Union[
        MaleoSOAPIEHTTPClientVitalSignServiceResults.Fail,
        MaleoSOAPIEHTTPClientVitalSignServiceResults.MultipleData
    ]:
        """Fetch vital signs from maleo-soapie"""
        result = await MaleoSOAPIEVitalSignHTTPController.get_vital_signs(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientVitalSignServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientVitalSignServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_vital_sign(
        parameters:MaleoSOAPIEVitalSignGeneralParameters.GetSingle
    ) -> Union[
        MaleoSOAPIEHTTPClientVitalSignServiceResults.Fail,
        MaleoSOAPIEHTTPClientVitalSignServiceResults.SingleData
    ]:
        """Fetch vital sign from maleo-soapie"""
        result = await MaleoSOAPIEVitalSignHTTPController.get_vital_sign(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientVitalSignServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientVitalSignServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoSOAPIEVitalSignGeneralParameters.CreateOrUpdate) -> Union[
        MaleoSOAPIEHTTPClientVitalSignServiceResults.Fail,
        MaleoSOAPIEHTTPClientVitalSignServiceResults.SingleData
    ]:
        """Create new vital sign"""
        result = await MaleoSOAPIEVitalSignHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientVitalSignServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientVitalSignServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        vital_sign_id:int,
        parameters:MaleoSOAPIEVitalSignGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientVitalSignServiceResults.Fail,
        MaleoSOAPIEHTTPClientVitalSignServiceResults.SingleData
    ]:
        """Update vital sign's data"""
        result = await MaleoSOAPIEVitalSignHTTPController.update(vital_sign_id=vital_sign_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientVitalSignServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientVitalSignServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        vital_sign_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientVitalSignServiceResults.Fail,
        MaleoSOAPIEHTTPClientVitalSignServiceResults.SingleData
    ]:
        """Update vital sign's status"""
        result = await MaleoSOAPIEVitalSignHTTPController.status_update(vital_sign_id=vital_sign_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientVitalSignServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientVitalSignServiceResults.SingleData.model_validate(result.content)