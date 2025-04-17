# This file serves all MaleoSOAPIE's General Parameters

from __future__ import annotations
from .subjective import MaleoSOAPIESubjectiveGeneralParameters
from .vital_sign import MaleoSOAPIEVitalSignGeneralParameters
from .objective import MaleoSOAPIEObjectiveGeneralParameters
from .diagnosis import  MaleoSOAPIEDiagnosisGeneralParameters
from .assessment import MaleoSOAPIEAssessmentGeneralParameters
from .plan import MaleoSOAPIEPlanGeneralParameters
from .intervention import MaleoSOAPIEInterventionGeneralParameters
from .evaluation import MaleoSOAPIEEvaluationGeneralParameters
from .soapie import MaleoSOAPIESOAPIEGeneralParameters

class MaleoSOAPIEGeneralParameters:
    Subjective = MaleoSOAPIESubjectiveGeneralParameters
    VitalSign = MaleoSOAPIEVitalSignGeneralParameters
    Objective = MaleoSOAPIEObjectiveGeneralParameters
    Diagnosis = MaleoSOAPIEDiagnosisGeneralParameters
    Assessment = MaleoSOAPIEAssessmentGeneralParameters
    Plan = MaleoSOAPIEPlanGeneralParameters
    Intervention = MaleoSOAPIEInterventionGeneralParameters
    Evaluation = MaleoSOAPIEEvaluationGeneralParameters
    SOAPIE = MaleoSOAPIESOAPIEGeneralParameters

__all__ = [
    "MaleoSOAPIEGeneralParameters",
    "MaleoSOAPIESubjectiveGeneralParameters",
    "MaleoSOAPIEObjectiveGeneralParameters",
    "MaleoSOAPIEVitalSignGeneralParameters",
    "MaleoSOAPIEAssessmentGeneralParameters",
    "MaleoSOAPIEDiagnosisGeneralParameters",
    "MaleoSOAPIEPlanGeneralParameters",
    "MaleoSOAPIEInterventionGeneralParameters",
    "MaleoSOAPIEEvaluationGeneralParameters",
    "MaleoSOAPIESOAPIEGeneralParameters"
]