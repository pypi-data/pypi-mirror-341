from maleo_core.clients.maleo_suite.maleo_soapie.http.manager import MaleoSOAPIEHTTPClientManager
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.client.soapie import MaleoSOAPIESOAPIEClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.soapie import MaleoSOAPIESOAPIEGeneralParameters

class MaleoSOAPIESOAPIEHTTPController:
    @staticmethod
    async def get_soapies(
        parameters:MaleoSOAPIESOAPIEClientParameters.Get
    ) -> BaseHTTPClientControllerResults:
        """Fetch soapies from maleo-soapie"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/soapies/"

            query_parameters = MaleoSOAPIESOAPIEClientParameters.GetQuery.model_validate(parameters.model_dump())
            params = query_parameters.to_query_params()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def get_soapie(
        parameters:MaleoSOAPIESOAPIEGeneralParameters.GetSingle
    ) -> BaseHTTPClientControllerResults:
        """Fetch soapie from maleo-soapie"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/soapies/"
            if parameters.identifier == MaleoSOAPIESOAPIEGeneralParameters.UniqueIdentifiers.ID:
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
    async def create(parameters:MaleoSOAPIESOAPIEGeneralParameters.CreateOrUpdate) -> BaseHTTPClientControllerResults:
        """Create new soapie"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/soapies/"

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
        soapie_id:int,
        parameters:MaleoSOAPIESOAPIEGeneralParameters.CreateOrUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update soapie's data"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/soapies/{soapie_id}"

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
        soapie_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update soapie's status"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/soapies/{soapie_id}/status"

            #* Construct query parameters
            params = parameters.model_dump() if parameters else {}

            #* Get Response
            response = await client.patch(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)