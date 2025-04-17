from maleo_core.clients.maleo_suite.maleo_soapie.http.manager import MaleoSOAPIEHTTPClientManager
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.client.plan import MaleoSOAPIEPlanClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.plan import MaleoSOAPIEPlanGeneralParameters

class MaleoSOAPIEPlanHTTPController:
    @staticmethod
    async def get_plans(
        parameters:MaleoSOAPIEPlanClientParameters.Get
    ) -> BaseHTTPClientControllerResults:
        """Fetch plans from maleo-soapie"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/plans/"

            query_parameters = MaleoSOAPIEPlanClientParameters.GetQuery.model_validate(parameters.model_dump())
            params = query_parameters.to_query_params()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def get_plan(
        parameters:MaleoSOAPIEPlanGeneralParameters.GetSingle
    ) -> BaseHTTPClientControllerResults:
        """Fetch plan from maleo-soapie"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/plans/"
            if parameters.identifier == MaleoSOAPIEPlanGeneralParameters.UniqueIdentifiers.ID:
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
    async def create(parameters:MaleoSOAPIEPlanGeneralParameters.CreateOrUpdate) -> BaseHTTPClientControllerResults:
        """Create new plan"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/plans/"

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
        plan_id:int,
        parameters:MaleoSOAPIEPlanGeneralParameters.CreateOrUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update plan's data"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/plans/{plan_id}"

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
        plan_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update plan's status"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/plans/{plan_id}/status"

            #* Construct query parameters
            params = parameters.model_dump() if parameters else {}

            #* Get Response
            response = await client.patch(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)