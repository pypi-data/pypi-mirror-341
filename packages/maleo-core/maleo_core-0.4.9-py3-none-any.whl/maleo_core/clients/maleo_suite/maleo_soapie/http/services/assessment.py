from typing import Union
from maleo_core.clients.maleo_suite.maleo_soapie.http.controllers.assessment import MaleoSOAPIEAssessmentHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.client.assessment import MaleoSOAPIEAssessmentClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.assessment import MaleoSOAPIEAssessmentGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.client.http.services.assessment import MaleoSOAPIEHTTPClientAssessmentServiceResults

class MaleoSOAPIEAssessmentHTTPService:
    @staticmethod
    async def get_assessments(
        parameters:MaleoSOAPIEAssessmentClientParameters.Get
    ) -> Union[
        MaleoSOAPIEHTTPClientAssessmentServiceResults.Fail,
        MaleoSOAPIEHTTPClientAssessmentServiceResults.MultipleData
    ]:
        """Fetch assessments from maleo-soapie"""
        result = await MaleoSOAPIEAssessmentHTTPController.get_assessments(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientAssessmentServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientAssessmentServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_assessment(
        parameters:MaleoSOAPIEAssessmentGeneralParameters.GetSingle
    ) -> Union[
        MaleoSOAPIEHTTPClientAssessmentServiceResults.Fail,
        MaleoSOAPIEHTTPClientAssessmentServiceResults.SingleData
    ]:
        """Fetch assessment from maleo-soapie"""
        result = await MaleoSOAPIEAssessmentHTTPController.get_assessment(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientAssessmentServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientAssessmentServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoSOAPIEAssessmentGeneralParameters.CreateOrUpdate) -> Union[
        MaleoSOAPIEHTTPClientAssessmentServiceResults.Fail,
        MaleoSOAPIEHTTPClientAssessmentServiceResults.SingleData
    ]:
        """Create new assessment"""
        result = await MaleoSOAPIEAssessmentHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientAssessmentServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientAssessmentServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        assessment_id:int,
        parameters:MaleoSOAPIEAssessmentGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientAssessmentServiceResults.Fail,
        MaleoSOAPIEHTTPClientAssessmentServiceResults.SingleData
    ]:
        """Update assessment's data"""
        result = await MaleoSOAPIEAssessmentHTTPController.update(assessment_id=assessment_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientAssessmentServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientAssessmentServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        assessment_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientAssessmentServiceResults.Fail,
        MaleoSOAPIEHTTPClientAssessmentServiceResults.SingleData
    ]:
        """Update assessment's status"""
        result = await MaleoSOAPIEAssessmentHTTPController.status_update(assessment_id=assessment_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientAssessmentServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientAssessmentServiceResults.SingleData.model_validate(result.content)