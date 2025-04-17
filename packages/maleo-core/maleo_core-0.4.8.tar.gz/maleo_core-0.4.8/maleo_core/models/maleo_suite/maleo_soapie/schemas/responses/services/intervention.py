from __future__ import annotations
from fastapi import status
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.base.schemas.responses.service import BaseServiceResponsesSchemas
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.intervention import MaleoSOAPIEInterventionQueryResults

class MaleoSOAPIEInterventionServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class NotFoundResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SPE-INT-001"
        message:str = "No intervention(s) found"
        description:str = "External error: No intervention(s) found in database acording to given parameter(s)"
        other:str = "Ensure parameter(s) are correct"

    class GetMultipleResponse(BaseServiceResponsesSchemas.MultipleData):
        code:str = "SPE-INT-002"
        message:str = "Interventions found"
        description:str = "Requested interventions found in database"
        data:list[MaleoSOAPIEInterventionQueryResults.Get]

    class GetSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-INT-003"
        message:str = "Intervention found"
        description:str = "Requested intervention found in database"
        data:MaleoSOAPIEInterventionQueryResults.Get

    class StatusUpdateResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-INT-004"

    class CreateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SPE-INT-005"
        message:str = "Failed creating intervention"

    class CreateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-INT-006"
        message:str = "Succesfully created new intervention"
        description:str = "A new intervention is created with data provided on request"
        data:MaleoSOAPIEInterventionQueryResults.Get

    class UpdateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SPE-INT-007"
        message:str = "Failed updating intervention"

    class UpdateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-INT-008"
        message:str = "Succesfully updated intervention"
        data:MaleoSOAPIEInterventionQueryResults.Get

    #* ----- ----- Responses Class ----- ----- *#
    not_found_responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "No intervention(s) found Response",
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