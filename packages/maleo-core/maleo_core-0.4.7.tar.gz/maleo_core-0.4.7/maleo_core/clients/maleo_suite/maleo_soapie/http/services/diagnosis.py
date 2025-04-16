from typing import Union
from maleo_core.clients.maleo_suite.maleo_soapie.http.controllers.diagnosis import MaleoSOAPIEDiagnosisHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.client.diagnosis import MaleoSOAPIEDiagnosisClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.diagnosis import MaleoSOAPIEDiagnosisGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.client.http.services.diagnosis import MaleoSOAPIEHTTPClientDiagnosisServiceResults

class MaleoSOAPIEDiagnosisHTTPService:
    @staticmethod
    async def get_diagnoses(
        parameters:MaleoSOAPIEDiagnosisClientParameters.Get
    ) -> Union[
        MaleoSOAPIEHTTPClientDiagnosisServiceResults.Fail,
        MaleoSOAPIEHTTPClientDiagnosisServiceResults.MultipleData
    ]:
        """Fetch diagnoses from maleo-soapie"""
        result = await MaleoSOAPIEDiagnosisHTTPController.get_diagnoses(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientDiagnosisServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientDiagnosisServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_diagnosis(
        parameters:MaleoSOAPIEDiagnosisGeneralParameters.GetSingle
    ) -> Union[
        MaleoSOAPIEHTTPClientDiagnosisServiceResults.Fail,
        MaleoSOAPIEHTTPClientDiagnosisServiceResults.SingleData
    ]:
        """Fetch diagnosis from maleo-soapie"""
        result = await MaleoSOAPIEDiagnosisHTTPController.get_diagnosis(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientDiagnosisServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientDiagnosisServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoSOAPIEDiagnosisGeneralParameters.CreateOrUpdate) -> Union[
        MaleoSOAPIEHTTPClientDiagnosisServiceResults.Fail,
        MaleoSOAPIEHTTPClientDiagnosisServiceResults.SingleData
    ]:
        """Create new diagnosis"""
        result = await MaleoSOAPIEDiagnosisHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientDiagnosisServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientDiagnosisServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        diagnosis_id:int,
        parameters:MaleoSOAPIEDiagnosisGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientDiagnosisServiceResults.Fail,
        MaleoSOAPIEHTTPClientDiagnosisServiceResults.SingleData
    ]:
        """Update diagnosis's data"""
        result = await MaleoSOAPIEDiagnosisHTTPController.update(diagnosis_id=diagnosis_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientDiagnosisServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientDiagnosisServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        diagnosis_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientDiagnosisServiceResults.Fail,
        MaleoSOAPIEHTTPClientDiagnosisServiceResults.SingleData
    ]:
        """Update diagnosis's status"""
        result = await MaleoSOAPIEDiagnosisHTTPController.status_update(diagnosis_id=diagnosis_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientDiagnosisServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientDiagnosisServiceResults.SingleData.model_validate(result.content)