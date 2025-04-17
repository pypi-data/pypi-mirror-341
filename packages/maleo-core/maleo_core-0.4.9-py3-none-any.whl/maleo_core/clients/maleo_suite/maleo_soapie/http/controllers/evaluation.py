from maleo_core.clients.maleo_suite.maleo_soapie.http.manager import MaleoSOAPIEHTTPClientManager
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.client.evaluation import MaleoSOAPIEEvaluationClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.evaluation import MaleoSOAPIEEvaluationGeneralParameters

class MaleoSOAPIEEvaluationHTTPController:
    @staticmethod
    async def get_evaluations(
        parameters:MaleoSOAPIEEvaluationClientParameters.Get
    ) -> BaseHTTPClientControllerResults:
        """Fetch evaluations from maleo-soapie"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/evaluations/"

            query_parameters = MaleoSOAPIEEvaluationClientParameters.GetQuery.model_validate(parameters.model_dump())
            params = query_parameters.to_query_params()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def get_evaluation(
        parameters:MaleoSOAPIEEvaluationGeneralParameters.GetSingle
    ) -> BaseHTTPClientControllerResults:
        """Fetch evaluation from maleo-soapie"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/evaluations/"
            if parameters.identifier == MaleoSOAPIEEvaluationGeneralParameters.UniqueIdentifiers.ID:
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
    async def create(parameters:MaleoSOAPIEEvaluationGeneralParameters.CreateOrUpdate) -> BaseHTTPClientControllerResults:
        """Create new evaluation"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/evaluations/"

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
        evaluation_id:int,
        parameters:MaleoSOAPIEEvaluationGeneralParameters.CreateOrUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update evaluation's data"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/evaluations/{evaluation_id}"

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
        evaluation_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update evaluation's status"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/evaluations/{evaluation_id}/status"

            #* Construct query parameters
            params = parameters.model_dump() if parameters else {}

            #* Get Response
            response = await client.patch(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)