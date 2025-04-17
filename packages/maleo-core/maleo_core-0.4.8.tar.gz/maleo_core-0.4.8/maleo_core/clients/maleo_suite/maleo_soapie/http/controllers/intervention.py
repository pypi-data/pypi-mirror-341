from maleo_core.clients.maleo_suite.maleo_soapie.http.manager import MaleoSOAPIEHTTPClientManager
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.client.intervention import MaleoSOAPIEInterventionClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.intervention import MaleoSOAPIEInterventionGeneralParameters

class MaleoSOAPIEInterventionHTTPController:
    @staticmethod
    async def get_interventions(
        parameters:MaleoSOAPIEInterventionClientParameters.Get
    ) -> BaseHTTPClientControllerResults:
        """Fetch interventions from maleo-soapie"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/interventions/"

            query_parameters = MaleoSOAPIEInterventionClientParameters.GetQuery.model_validate(parameters.model_dump())
            params = query_parameters.to_query_params()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def get_intervention(
        parameters:MaleoSOAPIEInterventionGeneralParameters.GetSingle
    ) -> BaseHTTPClientControllerResults:
        """Fetch intervention from maleo-soapie"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/interventions/"
            if parameters.identifier == MaleoSOAPIEInterventionGeneralParameters.UniqueIdentifiers.ID:
                url += f"{parameters.value}"
            else:
                url += f"{parameters.identifier.value}/{parameters.value}"

            #* Construct query parameters
            query_params = BaseGeneralParameters.GetSingleQuery.model_validate(parameters.model_dump())
            params = query_params.model_dump()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def create(parameters:MaleoSOAPIEInterventionGeneralParameters.CreateOrUpdate) -> BaseHTTPClientControllerResults:
        """Create new intervention"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/interventions/"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, json=json, headers=headers)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def update(
        intervention_id:int,
        parameters:MaleoSOAPIEInterventionGeneralParameters.CreateOrUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update intervention's data"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/interventions/{intervention_id}"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.put(url=url, json=json, headers=headers)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def status_update(
        intervention_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update intervention's status"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/interventions/{intervention_id}/status"

            #* Construct query parameters
            params = parameters.model_dump() if parameters else {}

            #* Get Response
            response = await client.patch(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)