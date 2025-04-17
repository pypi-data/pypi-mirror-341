from typing import Union
from maleo_core.clients.maleo_suite.maleo_soapie.http.controllers.plan import MaleoSOAPIEPlanHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.client.plan import MaleoSOAPIEPlanClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.plan import MaleoSOAPIEPlanGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.client.http.services.plan import MaleoSOAPIEHTTPClientPlanServiceResults

class MaleoSOAPIEPlanHTTPService:
    @staticmethod
    async def get_plans(
        parameters:MaleoSOAPIEPlanClientParameters.Get
    ) -> Union[
        MaleoSOAPIEHTTPClientPlanServiceResults.Fail,
        MaleoSOAPIEHTTPClientPlanServiceResults.MultipleData
    ]:
        """Fetch plans from maleo-soapie"""
        result = await MaleoSOAPIEPlanHTTPController.get_plans(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientPlanServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientPlanServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_plan(
        parameters:MaleoSOAPIEPlanGeneralParameters.GetSingle
    ) -> Union[
        MaleoSOAPIEHTTPClientPlanServiceResults.Fail,
        MaleoSOAPIEHTTPClientPlanServiceResults.SingleData
    ]:
        """Fetch plan from maleo-soapie"""
        result = await MaleoSOAPIEPlanHTTPController.get_plan(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientPlanServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientPlanServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoSOAPIEPlanGeneralParameters.CreateOrUpdate) -> Union[
        MaleoSOAPIEHTTPClientPlanServiceResults.Fail,
        MaleoSOAPIEHTTPClientPlanServiceResults.SingleData
    ]:
        """Create new plan"""
        result = await MaleoSOAPIEPlanHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientPlanServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientPlanServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        plan_id:int,
        parameters:MaleoSOAPIEPlanGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientPlanServiceResults.Fail,
        MaleoSOAPIEHTTPClientPlanServiceResults.SingleData
    ]:
        """Update plan's data"""
        result = await MaleoSOAPIEPlanHTTPController.update(plan_id=plan_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientPlanServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientPlanServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        plan_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientPlanServiceResults.Fail,
        MaleoSOAPIEHTTPClientPlanServiceResults.SingleData
    ]:
        """Update plan's status"""
        result = await MaleoSOAPIEPlanHTTPController.status_update(plan_id=plan_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientPlanServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientPlanServiceResults.SingleData.model_validate(result.content)