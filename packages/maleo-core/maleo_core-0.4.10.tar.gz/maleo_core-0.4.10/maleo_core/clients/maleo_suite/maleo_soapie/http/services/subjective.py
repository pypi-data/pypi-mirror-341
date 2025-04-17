from typing import Union
from maleo_core.clients.maleo_suite.maleo_soapie.http.controllers.subjective import MaleoSOAPIESubjectiveHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.client.subjective import MaleoSOAPIESubjectiveClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.subjective import MaleoSOAPIESubjectiveGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.client.http.services.subjective import MaleoSOAPIEHTTPClientSubjectiveServiceResults

class MaleoSOAPIESubjectiveHTTPService:
    @staticmethod
    async def get_subjectives(
        parameters:MaleoSOAPIESubjectiveClientParameters.Get
    ) -> Union[
        MaleoSOAPIEHTTPClientSubjectiveServiceResults.Fail,
        MaleoSOAPIEHTTPClientSubjectiveServiceResults.MultipleData
    ]:
        """Fetch subjectives from maleo-soapie"""
        result = await MaleoSOAPIESubjectiveHTTPController.get_subjectives(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientSubjectiveServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientSubjectiveServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_subjective(
        parameters:MaleoSOAPIESubjectiveGeneralParameters.GetSingle
    ) -> Union[
        MaleoSOAPIEHTTPClientSubjectiveServiceResults.Fail,
        MaleoSOAPIEHTTPClientSubjectiveServiceResults.SingleData
    ]:
        """Fetch subjective from maleo-soapie"""
        result = await MaleoSOAPIESubjectiveHTTPController.get_subjective(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientSubjectiveServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientSubjectiveServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoSOAPIESubjectiveGeneralParameters.CreateOrUpdate) -> Union[
        MaleoSOAPIEHTTPClientSubjectiveServiceResults.Fail,
        MaleoSOAPIEHTTPClientSubjectiveServiceResults.SingleData
    ]:
        """Create new subjective"""
        result = await MaleoSOAPIESubjectiveHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientSubjectiveServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientSubjectiveServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        subjective_id:int,
        parameters:MaleoSOAPIESubjectiveGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientSubjectiveServiceResults.Fail,
        MaleoSOAPIEHTTPClientSubjectiveServiceResults.SingleData
    ]:
        """Update subjective's data"""
        result = await MaleoSOAPIESubjectiveHTTPController.update(subjective_id=subjective_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientSubjectiveServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientSubjectiveServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        subjective_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientSubjectiveServiceResults.Fail,
        MaleoSOAPIEHTTPClientSubjectiveServiceResults.SingleData
    ]:
        """Update subjective's status"""
        result = await MaleoSOAPIESubjectiveHTTPController.status_update(subjective_id=subjective_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientSubjectiveServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientSubjectiveServiceResults.SingleData.model_validate(result.content)