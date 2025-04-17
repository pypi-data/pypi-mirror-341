from __future__ import annotations
from fastapi import status, Response
from typing import Any
from pydantic import BaseModel, Field, model_validator
from .response_class import BaseServiceRESTControllerResponseClass

class BaseServiceRESTControllerResults(BaseModel):
    success:bool = Field(..., description="REST Controller's success status")
    response_class:BaseServiceRESTControllerResponseClass = Field(BaseServiceRESTControllerResponseClass.JSON, description="REST Controller's response class")
    content:Any = Field(..., description="REST Controller's response content")
    status_code:int = Field(status.HTTP_200_OK, description="REST Controller's response status code")
    response:Response = Field(Response(), description="REST Controller's Response")

    class Config:
        arbitrary_types_allowed=True

    @model_validator(mode="after")
    def process_response(self):
        """Dynamically creates a response based on response_class."""
        response_cls = self.response_class.get_response_class()
        self.response = response_cls(content=self.content, status_code=self.status_code)
        return self

    def to_response(self) -> Response:
        return self.response