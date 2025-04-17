from typing import Union
from maleo_core.clients.maleo_suite.maleo_soapie.http.controllers.intervention import MaleoSOAPIEInterventionHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.client.intervention import MaleoSOAPIEInterventionClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.intervention import MaleoSOAPIEInterventionGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.client.http.services.intervention import MaleoSOAPIEHTTPClientInterventionServiceResults

class MaleoSOAPIEInterventionHTTPService:
    @staticmethod
    async def get_interventions(
        parameters:MaleoSOAPIEInterventionClientParameters.Get
    ) -> Union[
        MaleoSOAPIEHTTPClientInterventionServiceResults.Fail,
        MaleoSOAPIEHTTPClientInterventionServiceResults.MultipleData
    ]:
        """Fetch interventions from maleo-soapie"""
        result = await MaleoSOAPIEInterventionHTTPController.get_interventions(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientInterventionServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientInterventionServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_intervention(
        parameters:MaleoSOAPIEInterventionGeneralParameters.GetSingle
    ) -> Union[
        MaleoSOAPIEHTTPClientInterventionServiceResults.Fail,
        MaleoSOAPIEHTTPClientInterventionServiceResults.SingleData
    ]:
        """Fetch intervention from maleo-soapie"""
        result = await MaleoSOAPIEInterventionHTTPController.get_intervention(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientInterventionServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientInterventionServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoSOAPIEInterventionGeneralParameters.CreateOrUpdate) -> Union[
        MaleoSOAPIEHTTPClientInterventionServiceResults.Fail,
        MaleoSOAPIEHTTPClientInterventionServiceResults.SingleData
    ]:
        """Create new intervention"""
        result = await MaleoSOAPIEInterventionHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientInterventionServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientInterventionServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        intervention_id:int,
        parameters:MaleoSOAPIEInterventionGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientInterventionServiceResults.Fail,
        MaleoSOAPIEHTTPClientInterventionServiceResults.SingleData
    ]:
        """Update intervention's data"""
        result = await MaleoSOAPIEInterventionHTTPController.update(intervention_id=intervention_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientInterventionServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientInterventionServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        intervention_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoSOAPIEHTTPClientInterventionServiceResults.Fail,
        MaleoSOAPIEHTTPClientInterventionServiceResults.SingleData
    ]:
        """Update intervention's status"""
        result = await MaleoSOAPIEInterventionHTTPController.status_update(intervention_id=intervention_id, parameters=parameters)
        if not result.success:
            return MaleoSOAPIEHTTPClientInterventionServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSOAPIEHTTPClientInterventionServiceResults.SingleData.model_validate(result.content)