from typing import Union
from maleo_core.clients.maleo_suite.maleo_soapie.http.controllers.soapie import MaleoSOAPIESOAPIEHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.client.soapie import MaleoSOAPIESOAPIEClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.soapie import MaleoSOAPIESOAPIEGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.client.http.services.soapie import MaleoSOAPIEHTTPClientSOAPIEServiceResults

class MaleoSOAPIESOAPIEHTTPService:
    @staticmethod
    async def get_soapies(
        parameters:MaleoSOAPIESOAPIEClientParameters.Get
    ) -> Union[
        MaleoSOAPIEHTTPClientSOAPIEServiceResults.Fail,
        MaleoSOAPIEHTTPClientSOAPIEServiceResults.MultipleData
    ]:
        """Fetch soapies from maleo-soapie"""
        result = await MaleoSOAPIESOAPIEHTTPController.get_soapies(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientSOAPIEServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientSOAPIEServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_soapie(
        parameters:MaleoSOAPIESOAPIEGeneralParameters.GetSingle
    ) -> Union[
        MaleoSOAPIEHTTPClientSOAPIEServiceResults.Fail,
        MaleoSOAPIEHTTPClientSOAPIEServiceResults.SingleData
    ]:
        """Fetch soapie from maleo-soapie"""
        result = await MaleoSOAPIESOAPIEHTTPController.get_soapie(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientSOAPIEServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientSOAPIEServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoSOAPIESOAPIEGeneralParameters.CreateOrUpdate) -> Union[
        MaleoSOAPIEHTTPClientSOAPIEServiceResults.Fail,
        MaleoSOAPIEHTTPClientSOAPIEServiceResults.SingleData
    ]:
        """Create new soapie"""
        result = await MaleoSOAPIESOAPIEHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientSOAPIEServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientSOAPIEServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        soapie_id:int,
        parameters:MaleoSOAPIESOAPIEGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientSOAPIEServiceResults.Fail,
        MaleoSOAPIEHTTPClientSOAPIEServiceResults.SingleData
    ]:
        """Update soapie's data"""
        result = await MaleoSOAPIESOAPIEHTTPController.update(soapie_id=soapie_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientSOAPIEServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientSOAPIEServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        soapie_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientSOAPIEServiceResults.Fail,
        MaleoSOAPIEHTTPClientSOAPIEServiceResults.SingleData
    ]:
        """Update soapie's status"""
        result = await MaleoSOAPIESOAPIEHTTPController.status_update(soapie_id=soapie_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientSOAPIEServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientSOAPIEServiceResults.SingleData.model_validate(result.content)