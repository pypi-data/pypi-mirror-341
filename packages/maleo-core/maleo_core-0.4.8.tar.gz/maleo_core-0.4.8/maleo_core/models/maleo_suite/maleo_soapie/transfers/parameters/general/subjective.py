from __future__ import annotations
from enum import StrEnum
from pydantic import Field
from typing import Optional
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.soapie import MaleoSOAPIESOAPIEGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.subjective import MaleoSOAPIESubjectiveGeneralTransfers

class MaleoSOAPIESubjectiveGeneralParameters:
    class UniqueIdentifiers(StrEnum):
        ID = "id"
        UUID = "uuid"
        SOAPIE_ID = "soapie_id"

    class GetSingle(BaseGeneralParameters.GetSingle):
        identifier:MaleoSOAPIESubjectiveGeneralParameters.UniqueIdentifiers = Field(..., description="Identifier")

    class CreateOrUpdate(
        MaleoSOAPIESubjectiveGeneralTransfers.Base,
        MaleoSOAPIESOAPIEGeneralTransfers.SOAPIEID
    ): pass

    class UniqueFields(StrEnum):
        SOAPIE_ID = "soapie_id"

    unique_field_nullability:dict[
        MaleoSOAPIESubjectiveGeneralParameters.UniqueFields,
        bool
    ] = {
        UniqueFields.SOAPIE_ID: False
    }

    class UniqueFieldCheck(BaseGeneralParameters.UniqueFieldCheck):
        field:MaleoSOAPIESubjectiveGeneralParameters.UniqueFields = Field(..., description="Field to be checked")

    UniqueFieldChecks = list[UniqueFieldCheck]

    @staticmethod
    def generate_unique_field_checks(
        operation:BaseGeneralParameters.OperationType,
        new_parameters:CreateOrUpdate,
        old_parameters:Optional[CreateOrUpdate]
    ) -> UniqueFieldChecks:
        update_unique_field_checks = [
            MaleoSOAPIESubjectiveGeneralParameters.UniqueFieldCheck(
                operation=operation,
                field=field,
                new_value=getattr(new_parameters, field.value),
                old_value=getattr(old_parameters, field.value) if operation == BaseGeneralParameters.OperationType.UPDATE else None,
                nullable=MaleoSOAPIESubjectiveGeneralParameters.unique_field_nullability.get(field),
                suggestion=f"Select other {field} value{"" if not MaleoSOAPIESubjectiveGeneralParameters.unique_field_nullability.get(field) else ", or set it to null"}."
            )
            for field in MaleoSOAPIESubjectiveGeneralParameters.UniqueFields
        ]
        return update_unique_field_checks