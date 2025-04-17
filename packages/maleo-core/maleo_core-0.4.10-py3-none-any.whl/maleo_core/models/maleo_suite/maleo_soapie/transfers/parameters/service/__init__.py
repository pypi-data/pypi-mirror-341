# This file serves all MaleoSOAPIE's Service Parameters

from __future__ import annotations
from .subjective import MaleoSOAPIESubjectiveServiceParameters
from .vital_sign import MaleoSOAPIEVitalSignServiceParameters
from .objective import MaleoSOAPIEObjectiveServiceParameters
from .diagnosis import MaleoSOAPIEDiagnosisServiceParameters
from .assessment import MaleoSOAPIEAssessmentServiceParameters
from .plan import MaleoSOAPIEPlanServiceParameters
from .intervention import MaleoSOAPIEInterventionServiceParameters
from .evaluation import MaleoSOAPIEEvaluationServiceParameters
from .soapie import MaleoSOAPIESOAPIEServiceParameters

class MaleoSOAPIEServiceParameters:
    Subjective = MaleoSOAPIESubjectiveServiceParameters
    VitalSign = MaleoSOAPIEVitalSignServiceParameters
    Objective = MaleoSOAPIEObjectiveServiceParameters
    Diagnosis = MaleoSOAPIEDiagnosisServiceParameters
    Assessment = MaleoSOAPIEAssessmentServiceParameters
    Plan = MaleoSOAPIEPlanServiceParameters
    Intervention = MaleoSOAPIEInterventionServiceParameters
    Evaluation = MaleoSOAPIEEvaluationServiceParameters
    SOAPIE = MaleoSOAPIESOAPIEServiceParameters

__all__ = [
    "MaleoSOAPIEServiceParameters",
    "MaleoSOAPIESubjectiveServiceParameters",
    "MaleoSOAPIEVitalSignServiceParameters",
    "MaleoSOAPIEObjectiveServiceParameters",
    "MaleoSOAPIEDiagnosisServiceParameters",
    "MaleoSOAPIEAssessmentServiceParameters",
    "MaleoSOAPIEPlanServiceParameters",
    "MaleoSOAPIEInterventionServiceParameters",
    "MaleoSOAPIEEvaluationServiceParameters",
    "MaleoSOAPIESOAPIEServiceParameters"
]