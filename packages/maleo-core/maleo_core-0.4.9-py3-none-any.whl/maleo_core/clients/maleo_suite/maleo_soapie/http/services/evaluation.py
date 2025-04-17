from typing import Union
from maleo_core.clients.maleo_suite.maleo_soapie.http.controllers.evaluation import MaleoSOAPIEEvaluationHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.client.evaluation import MaleoSOAPIEEvaluationClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.evaluation import MaleoSOAPIEEvaluationGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.client.http.services.evaluation import MaleoSOAPIEHTTPClientEvaluationServiceResults

class MaleoSOAPIEEvaluationHTTPService:
    @staticmethod
    async def get_evaluations(
        parameters:MaleoSOAPIEEvaluationClientParameters.Get
    ) -> Union[
        MaleoSOAPIEHTTPClientEvaluationServiceResults.Fail,
        MaleoSOAPIEHTTPClientEvaluationServiceResults.MultipleData
    ]:
        """Fetch evaluations from maleo-soapie"""
        result = await MaleoSOAPIEEvaluationHTTPController.get_evaluations(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientEvaluationServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientEvaluationServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_evaluation(
        parameters:MaleoSOAPIEEvaluationGeneralParameters.GetSingle
    ) -> Union[
        MaleoSOAPIEHTTPClientEvaluationServiceResults.Fail,
        MaleoSOAPIEHTTPClientEvaluationServiceResults.SingleData
    ]:
        """Fetch evaluation from maleo-soapie"""
        result = await MaleoSOAPIEEvaluationHTTPController.get_evaluation(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientEvaluationServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientEvaluationServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoSOAPIEEvaluationGeneralParameters.CreateOrUpdate) -> Union[
        MaleoSOAPIEHTTPClientEvaluationServiceResults.Fail,
        MaleoSOAPIEHTTPClientEvaluationServiceResults.SingleData
    ]:
        """Create new evaluation"""
        result = await MaleoSOAPIEEvaluationHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientEvaluationServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientEvaluationServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        evaluation_id:int,
        parameters:MaleoSOAPIEEvaluationGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientEvaluationServiceResults.Fail,
        MaleoSOAPIEHTTPClientEvaluationServiceResults.SingleData
    ]:
        """Update evaluation's data"""
        result = await MaleoSOAPIEEvaluationHTTPController.update(evaluation_id=evaluation_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientEvaluationServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientEvaluationServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        evaluation_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientEvaluationServiceResults.Fail,
        MaleoSOAPIEHTTPClientEvaluationServiceResults.SingleData
    ]:
        """Update evaluation's status"""
        result = await MaleoSOAPIEEvaluationHTTPController.status_update(evaluation_id=evaluation_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientEvaluationServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientEvaluationServiceResults.SingleData.model_validate(result.content)