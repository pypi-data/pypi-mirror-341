from __future__ import annotations
from enum import StrEnum
from pydantic import Field
from typing import Optional
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.objective import MaleoSOAPIEObjectiveGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.vital_sign import MaleoSOAPIEVitalSignGeneralTransfers

class MaleoSOAPIEVitalSignGeneralParameters:
    class UniqueIdentifiers(StrEnum):
        ID = "id"
        UUID = "uuid"
        OBJECTIVE_ID = "objective_id"

    class GetSingle(BaseGeneralParameters.GetSingle):
        identifier:MaleoSOAPIEVitalSignGeneralParameters.UniqueIdentifiers = Field(..., description="Identifier")

    class CreateOrUpdate(
        MaleoSOAPIEVitalSignGeneralTransfers.Base,
        MaleoSOAPIEObjectiveGeneralTransfers.ObjectiveID
    ): pass

    class UniqueFields(StrEnum):
        OBJECTIVE_ID = "objective_id"

    unique_field_nullability:dict[
        MaleoSOAPIEVitalSignGeneralParameters.UniqueFields,
        bool
    ] = {
        UniqueFields.OBJECTIVE_ID: False
    }

    class UniqueFieldCheck(BaseGeneralParameters.UniqueFieldCheck):
        field:MaleoSOAPIEVitalSignGeneralParameters.UniqueFields = Field(..., description="Field to be checked")

    UniqueFieldChecks = list[UniqueFieldCheck]

    @staticmethod
    def generate_unique_field_checks(
        operation:BaseGeneralParameters.OperationType,
        new_parameters:CreateOrUpdate,
        old_parameters:Optional[CreateOrUpdate]
    ) -> UniqueFieldChecks:
        update_unique_field_checks = [
            MaleoSOAPIEVitalSignGeneralParameters.UniqueFieldCheck(
                operation=operation,
                field=field,
                new_value=getattr(new_parameters, field.value),
                old_value=getattr(old_parameters, field.value) if operation == BaseGeneralParameters.OperationType.UPDATE else None,
                nullable=MaleoSOAPIEVitalSignGeneralParameters.unique_field_nullability.get(field),
                suggestion=f"Select other {field} value{"" if not MaleoSOAPIEVitalSignGeneralParameters.unique_field_nullability.get(field) else ", or set it to null"}."
            )
            for field in MaleoSOAPIEVitalSignGeneralParameters.UniqueFields
        ]
        return update_unique_field_checks