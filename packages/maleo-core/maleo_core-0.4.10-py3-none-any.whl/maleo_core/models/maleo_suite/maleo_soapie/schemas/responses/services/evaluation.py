from __future__ import annotations
from fastapi import status
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.base.schemas.responses.service import BaseServiceResponsesSchemas
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.evaluation import MaleoSOAPIEEvaluationQueryResults

class MaleoSOAPIEEvaluationServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class NotFoundResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SPE-EVL-001"
        message:str = "No evaluation(s) found"
        description:str = "External error: No evaluation(s) found in database acording to given parameter(s)"
        other:str = "Ensure parameter(s) are correct"

    class GetMultipleResponse(BaseServiceResponsesSchemas.MultipleData):
        code:str = "SPE-EVL-002"
        message:str = "Evaluations found"
        description:str = "Requested evaluations found in database"
        data:list[MaleoSOAPIEEvaluationQueryResults.Get]

    class GetSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-EVL-003"
        message:str = "Evaluation found"
        description:str = "Requested evaluation found in database"
        data:MaleoSOAPIEEvaluationQueryResults.Get

    class StatusUpdateResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-EVL-004"

    class CreateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SPE-EVL-005"
        message:str = "Failed creating evaluation"

    class CreateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-EVL-006"
        message:str = "Succesfully created new evaluation"
        description:str = "A new evaluation is created with data provided on request"
        data:MaleoSOAPIEEvaluationQueryResults.Get

    class UpdateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SPE-EVL-007"
        message:str = "Failed updating evaluation"

    class UpdateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SPE-EVL-008"
        message:str = "Succesfully updated evaluation"
        data:MaleoSOAPIEEvaluationQueryResults.Get

    #* ----- ----- Responses Class ----- ----- *#
    not_found_responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "No evaluation(s) found Response",
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