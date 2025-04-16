from __future__ import annotations
from fastapi import status
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.base.schemas.responses.service import BaseServiceResponsesSchemas
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.soapie import MaleoSOAPIESOAPIEQueryResults

class MaleoSOAPIESOAPIEServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class NotFoundResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SPE-SPE-001"
        message:str = "No soapie(s) found"
        description:str = "External error: No soapie(s) found in database acording to given parameter(s)"
        other:str = "Ensure parameter(s) are correct"

    class GetMultipleResponse(BaseServiceResponsesSchemas.MultipleData):
        code:str = "SPE-SPE-002"
        message:str = "SOAPIEs found"
        description:str = "Requested soapies found in database"
        data:list[MaleoSOAPIESOAPIEQueryResults.Get]

    class GetSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-SPE-003"
        message:str = "SOAPIE found"
        description:str = "Requested soapie found in database"
        data:MaleoSOAPIESOAPIEQueryResults.Get

    class StatusUpdateResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-SPE-004"

    class CreateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SPE-SPE-005"
        message:str = "Failed creating soapie"

    class CreateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-SPE-006"
        message:str = "Succesfully created new soapie"
        description:str = "A new soapie is created with data provided on request"
        data:MaleoSOAPIESOAPIEQueryResults.Get

    class UpdateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SPE-SPE-007"
        message:str = "Failed updating soapie"

    class UpdateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-SPE-008"
        message:str = "Succesfully updated soapie"
        data:MaleoSOAPIESOAPIEQueryResults.Get

    #* ----- ----- Responses Class ----- ----- *#
    not_found_responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "No soapie(s) found Response",
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