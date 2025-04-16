from maleo_core.clients.maleo_suite.maleo_soapie.http.manager import MaleoSOAPIEHTTPClientManager
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.client.objective import MaleoSOAPIEObjectiveClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.objective import MaleoSOAPIEObjectiveGeneralParameters

class MaleoSOAPIEObjectiveHTTPController:
    @staticmethod
    async def get_objectives(
        parameters:MaleoSOAPIEObjectiveClientParameters.Get
    ) -> BaseHTTPClientControllerResults:
        """Fetch objectives from maleo-soapie"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/objectives/"

            query_parameters = MaleoSOAPIEObjectiveClientParameters.GetQuery.model_validate(parameters.model_dump())
            params = query_parameters.to_query_params()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def get_objective(
        parameters:MaleoSOAPIEObjectiveGeneralParameters.GetSingle
    ) -> BaseHTTPClientControllerResults:
        """Fetch objective from maleo-soapie"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/objectives/"
            if parameters.identifier == MaleoSOAPIEObjectiveGeneralParameters.UniqueIdentifiers.ID:
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
    async def create(parameters:MaleoSOAPIEObjectiveGeneralParameters.CreateOrUpdate) -> BaseHTTPClientControllerResults:
        """Create new objective"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/objectives/"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct query
            params = parameters.model_dump(include={"expand"})

            #* Construct body
            json = parameters.model_dump(exclude={"expand"})

            #* Get Response
            response = await client.post(url=url, json=json, params=params, headers=headers)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def update(
        objective_id:int,
        parameters:MaleoSOAPIEObjectiveGeneralParameters.CreateOrUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update objective's data"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/objectives/{objective_id}"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct query
            params = parameters.model_dump(include={"expand"})

            #* Construct body
            json = parameters.model_dump(exclude={"expand"})

            #* Get Response
            response = await client.put(url=url, json=json, params=params, headers=headers)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def status_update(
        objective_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update objective's status"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/objectives/{objective_id}/status"

            #* Construct query parameters
            params = parameters.model_dump() if parameters else {}

            #* Get Response
            response = await client.patch(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)