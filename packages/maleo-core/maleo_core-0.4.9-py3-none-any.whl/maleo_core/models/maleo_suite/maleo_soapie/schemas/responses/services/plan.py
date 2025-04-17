from __future__ import annotations
from fastapi import status
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.base.schemas.responses.service import BaseServiceResponsesSchemas
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.plan import MaleoSOAPIEPlanQueryResults

class MaleoSOAPIEPlanServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class NotFoundResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SPE-PLA-001"
        message:str = "No plan(s) found"
        description:str = "External error: No plan(s) found in database acording to given parameter(s)"
        other:str = "Ensure parameter(s) are correct"

    class GetMultipleResponse(BaseServiceResponsesSchemas.MultipleData):
        code:str = "SPE-PLA-002"
        message:str = "Plans found"
        description:str = "Requested plans found in database"
        data:list[MaleoSOAPIEPlanQueryResults.Get]

    class GetSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-PLA-003"
        message:str = "Plan found"
        description:str = "Requested plan found in database"
        data:MaleoSOAPIEPlanQueryResults.Get

    class StatusUpdateResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-PLA-004"

    class CreateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SPE-PLA-005"
        message:str = "Failed creating plan"

    class CreateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-PLA-006"
        message:str = "Succesfully created new plan"
        description:str = "A new plan is created with data provided on request"
        data:MaleoSOAPIEPlanQueryResults.Get

    class UpdateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SPE-PLA-007"
        message:str = "Failed updating plan"

    class UpdateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-PLA-008"
        message:str = "Succesfully updated plan"
        data:MaleoSOAPIEPlanQueryResults.Get

    #* ----- ----- Responses Class ----- ----- *#
    not_found_responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "No plan(s) found Response",
            "model": NotFoundResponse
        }
    }

    get_responses={
        **not_found_responses,
        **BaseGeneralResponsesSchemas.other_responses
    }

    create_responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Create failed response",
            "model": CreateFailedResponse
        },
        **BaseGeneralResponsesSchemas.other_responses
    }

    update_responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Update failed response",
            "model": UpdateFailedResponse
        },
        **not_found_responses,
        **BaseGeneralResponsesSchemas.other_responses
    }