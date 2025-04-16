from maleo_core.clients.maleo_suite.maleo_soapie.http.manager import MaleoSOAPIEHTTPClientManager
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.client.assessment import MaleoSOAPIEAssessmentClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.assessment import MaleoSOAPIEAssessmentGeneralParameters

class MaleoSOAPIEAssessmentHTTPController:
    @staticmethod
    async def get_assessments(
        parameters:MaleoSOAPIEAssessmentClientParameters.Get
    ) -> BaseHTTPClientControllerResults:
        """Fetch assessments from maleo-soapie"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/assessments/"

            query_parameters = MaleoSOAPIEAssessmentClientParameters.GetQuery.model_validate(parameters.model_dump())
            params = query_parameters.to_query_params()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def get_assessment(
        parameters:MaleoSOAPIEAssessmentGeneralParameters.GetSingle
    ) -> BaseHTTPClientControllerResults:
        """Fetch assessment from maleo-soapie"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/assessments/"
            if parameters.identifier == MaleoSOAPIEAssessmentGeneralParameters.UniqueIdentifiers.ID:
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
    async def create(parameters:MaleoSOAPIEAssessmentGeneralParameters.CreateOrUpdate) -> BaseHTTPClientControllerResults:
        """Create new assessment"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/assessments/"

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
        assessment_id:int,
        parameters:MaleoSOAPIEAssessmentGeneralParameters.CreateOrUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update assessment's data"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/assessments/{assessment_id}"

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
        assessment_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update assessment's status"""
        async with MaleoSOAPIEHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSOAPIEHTTPClientManager._base_url}/v1/assessments/{assessment_id}/status"

            #* Construct query parameters
            params = parameters.model_dump() if parameters else {}

            #* Get Response
            response = await client.patch(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)