from __future__ import annotations
from fastapi import status
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.base.schemas.responses.service import BaseServiceResponsesSchemas
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.objective import MaleoSOAPIEObjectiveQueryResults

class MaleoSOAPIEObjectiveServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class NotFoundResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SPE-OBJ-001"
        message:str = "No objective(s) found"
        description:str = "External error: No objective(s) found in database acording to given parameter(s)"
        other:str = "Ensure parameter(s) are correct"

    class GetMultipleResponse(BaseServiceResponsesSchemas.MultipleData):
        code:str = "SPE-OBJ-002"
        message:str = "Objectives found"
        description:str = "Requested objectives found in database"
        data:list[MaleoSOAPIEObjectiveQueryResults.Get]

    class GetSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-OBJ-003"
        message:str = "Objective found"
        description:str = "Requested objective found in database"
        data:MaleoSOAPIEObjectiveQueryResults.Get

    class StatusUpdateResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-OBJ-004"

    class CreateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SPE-OBJ-005"
        message:str = "Failed creating objective"

    class CreateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-OBJ-006"
        message:str = "Succesfully created new objective"
        description:str = "A new objective is created with data provided on request"
        data:MaleoSOAPIEObjectiveQueryResults.Get

    class UpdateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SPE-OBJ-007"
        message:str = "Failed updating objective"

    class UpdateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-OBJ-008"
        message:str = "Succesfully updated objective"
        data:MaleoSOAPIEObjectiveQueryResults.Get

    #* ----- ----- Responses Class ----- ----- *#
    not_found_responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "No objective(s) found Response",
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