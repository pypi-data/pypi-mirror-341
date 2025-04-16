from typing import Union
from maleo_core.clients.maleo_suite.maleo_soapie.http.controllers.objective import MaleoSOAPIEObjectiveHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.client.objective import MaleoSOAPIEObjectiveClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.objective import MaleoSOAPIEObjectiveGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.client.http.services.objective import MaleoSOAPIEHTTPClientObjectiveServiceResults

class MaleoSOAPIEObjectiveHTTPService:
    @staticmethod
    async def get_objectives(
        parameters:MaleoSOAPIEObjectiveClientParameters.Get
    ) -> Union[
        MaleoSOAPIEHTTPClientObjectiveServiceResults.Fail,
        MaleoSOAPIEHTTPClientObjectiveServiceResults.MultipleData
    ]:
        """Fetch objectives from maleo-soapie"""
        result = await MaleoSOAPIEObjectiveHTTPController.get_objectives(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientObjectiveServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientObjectiveServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_objective(
        parameters:MaleoSOAPIEObjectiveGeneralParameters.GetSingle
    ) -> Union[
        MaleoSOAPIEHTTPClientObjectiveServiceResults.Fail,
        MaleoSOAPIEHTTPClientObjectiveServiceResults.SingleData
    ]:
        """Fetch objective from maleo-soapie"""
        result = await MaleoSOAPIEObjectiveHTTPController.get_objective(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientObjectiveServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientObjectiveServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoSOAPIEObjectiveGeneralParameters.CreateOrUpdate) -> Union[
        MaleoSOAPIEHTTPClientObjectiveServiceResults.Fail,
        MaleoSOAPIEHTTPClientObjectiveServiceResults.SingleData
    ]:
        """Create new objective"""
        result = await MaleoSOAPIEObjectiveHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientObjectiveServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientObjectiveServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        objective_id:int,
        parameters:MaleoSOAPIEObjectiveGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientObjectiveServiceResults.Fail,
        MaleoSOAPIEHTTPClientObjectiveServiceResults.SingleData
    ]:
        """Update objective's data"""
        result = await MaleoSOAPIEObjectiveHTTPController.update(objective_id=objective_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientObjectiveServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientObjectiveServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        objective_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientObjectiveServiceResults.Fail,
        MaleoSOAPIEHTTPClientObjectiveServiceResults.SingleData
    ]:
        """Update objective's status"""
        result = await MaleoSOAPIEObjectiveHTTPController.status_update(objective_id=objective_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientObjectiveServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientObjectiveServiceResults.SingleData.model_validate(result.content)