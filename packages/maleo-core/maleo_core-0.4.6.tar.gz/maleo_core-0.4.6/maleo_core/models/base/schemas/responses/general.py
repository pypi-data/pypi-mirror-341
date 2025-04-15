from __future__ import annotations
from fastapi import status
from pydantic import BaseModel, Field, field_serializer, model_validator, FieldSerializationInfo
from typing import Literal, Optional, Any
from maleo_core.models.base.general import BaseGeneralModels
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.utils.serializer import BaseSerializer

class BaseGeneralResponsesSchemas:
    #* ----- ----- ----- Base ----- ----- ----- *#
    class Base(BaseModel):
        success:bool = Field(..., description="Response's success status")
        code:str = Field(..., description="Response's code")
        message:str = Field(..., description="Response's message")
        description:str = Field(..., description="Response's description")

    #* ----- ----- ----- Derived ----- ----- ----- *#
    class Fail(Base):
        success:Literal[False] = Field(False, description="Success status")
        other:Optional[Any] = Field(None, description="Response's other information")

    class ServerError(Fail):
        code:str = "MAL-EXC-001"
        message:str = "Unexpected Server Error"
        description:str = "An unexpected error occurred. Please try again later or contact administrator."

    class ValidationError(Fail):
        code:str = "MAL-EXC-002"
        message:str = "Validation Error"
        description:str = "Request validation failed due to missing or invalid fields. Check other for more info."

    class NotFoundError(Fail):
        code:str = "MAL-EXC-003"
        message:str = "Not Found Error"
        description:str = "The resource you requested can not be found. Ensure your request is correct."

    class RateLimitExceeded(Fail):
        code:str = "MAL-RTL-001"
        message:str = "Rate Limit Exceeded"
        description:str = "This resource is requested too many times. Please try again later."

    class Unauthorized(Fail):
        code:str = "MAL-ATH-001"
        message:str = "Unauthorized Request"

    class Forbidden(Fail):
        code:str = "MAL-ATH-002"
        message:str = "Forbidden Request"

    class NoData(Base):
        success:Literal[True] = Field(True, description="Success status")
        data:None = Field(None, description="Fetched data")
        other:Optional[Any] = Field(None, description="Response's other information")

    class SingleData(Base):
        success:Literal[True] = Field(True, description="Success status")
        data:BaseServiceQueryResults.Get = Field(..., description="Fetched data")
        other:Optional[Any] = Field(None, description="Response's other information")

        @field_serializer("data", when_used="always")
        def serialize_data(self, data:BaseServiceQueryResults.Get, info:FieldSerializationInfo) -> dict[str, Any]:
            context = dict(info.context) if info.context is not None else {}
            expandable_fields = set(context.get("expandable_fields", []))
            expand = set(context.get("expand", []))

            expand_map = BaseSerializer.build_nested_expand_structure(expand=expand)
            serialized = data.model_dump()
            return BaseSerializer.recursive_prune(obj=serialized, expand_map=expand_map, expandable_fields=expandable_fields)

    class MultipleData(Base):
        page:int = Field(..., ge=1, description="Page number, must be >= 1.", exclude=True)
        limit:int = Field(..., ge=1, le=100, description="Page size, must be 1 <= limit <= 100.", exclude=True)
        total_data:int = Field(..., description="Total data count", exclude=True)
        success:Literal[True] = Field(True, description="Success status")
        data:list[BaseServiceQueryResults.Get] = Field(..., description="Paginated data")
        pagination:BaseGeneralModels.ExtendedPagination = Field(..., description="Pagination metadata")
        other:Optional[Any] = Field(None, description="Optional other information")

        @model_validator(mode="before")
        @classmethod
        def calculate_pagination_component(cls, values: dict) -> dict:
            """Extracts pagination components (page, limit, total_data) before validation."""
            pagination = values.get("pagination")

            if isinstance(pagination, BaseGeneralModels.ExtendedPagination):
                page = values.get("page")
                if page is None:
                    values["page"] = pagination.page
                
                limit = values.get("limit")
                if limit is None:
                    values["limit"] = pagination.limit
                
                total_data = values.get("total_data")
                if total_data is None:
                    values["total_data"] = pagination.total_data

            return values

        @field_serializer("data", when_used="always")
        def serialize_data(self, data:list[BaseServiceQueryResults.Get], info:FieldSerializationInfo) -> list[dict[str, Any]]:
            context = dict(info.context) if info.context is not None else {}
            expandable_fields = set(context.get("expandable_fields", []))
            expand = set(context.get("expand", []))

            expand_map = BaseSerializer.build_nested_expand_structure(expand=expand)
            return [BaseSerializer.recursive_prune(obj=item.model_dump(), expand_map=expand_map, expandable_fields=expandable_fields) for item in data]

    #* ----- ----- Responses Class ----- ----- *#
    other_responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized Response",
            "model": Unauthorized
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden Response",
            "model": Forbidden
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation Error Response",
            "model": ValidationError
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error Response",
            "model": ServerError
        }
    }