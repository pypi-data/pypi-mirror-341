# This file serves all MaleoSOAPIE's services responses schemas

from __future__ import annotations
from .subjective import MaleoSOAPIESubjectiveServiceResponsesSchemas
from .vital_sign import MaleoSOAPIEVitalSignServiceResponsesSchemas
from .objective import MaleoSOAPIEObjectiveServiceResponsesSchemas
from .diagnosis import MaleoSOAPIEDiagnosisServiceResponsesSchemas
from .assessment import MaleoSOAPIEAssessmentServiceResponsesSchemas
from .plan import MaleoSOAPIEPlanServiceResponsesSchemas
from .intervention import MaleoSOAPIEInterventionServiceResponsesSchemas
from .evaluation import MaleoSOAPIEEvaluationServiceResponsesSchemas
from .soapie import MaleoSOAPIESOAPIEServiceResponsesSchemas

class MaleoSOAPIEServicesResponsesSchemas:
    Subjective = MaleoSOAPIESubjectiveServiceResponsesSchemas
    VitalSign = MaleoSOAPIEVitalSignServiceResponsesSchemas
    Objective = MaleoSOAPIEObjectiveServiceResponsesSchemas
    Diagnosis = MaleoSOAPIEDiagnosisServiceResponsesSchemas
    Assessment = MaleoSOAPIEAssessmentServiceResponsesSchemas
    Plan = MaleoSOAPIEPlanServiceResponsesSchemas
    Intervention = MaleoSOAPIEInterventionServiceResponsesSchemas
    Evaluation = MaleoSOAPIEEvaluationServiceResponsesSchemas
    SOAPIE = MaleoSOAPIESOAPIEServiceResponsesSchemas

__all__ = [
    "MaleoSOAPIEServicesResponsesSchemas",
    "MaleoSOAPIESubjectiveServiceResponsesSchemas",
    "MaleoSOAPIEVitalSignServiceResponsesSchemas",
    "MaleoSOAPIEObjectiveServiceResponsesSchemas",
    "MaleoSOAPIEDiagnosisServiceResponsesSchemas",
    "MaleoSOAPIEAssessmentServiceResponsesSchemas",
    "MaleoSOAPIEPlanServiceResponsesSchemas",
    "MaleoSOAPIEInterventionServiceResponsesSchemas",
    "MaleoSOAPIEEvaluationServiceResponsesSchemas",
    "MaleoSOAPIESOAPIEServiceResponsesSchemas"
]