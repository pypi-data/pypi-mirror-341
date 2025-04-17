# This file serves all MaleoSOAPIE's General Transfers

from __future__ import annotations
from .subjective import MaleoSOAPIESubjectiveGeneralTransfers
from .vital_sign import MaleoSOAPIEVitalSignGeneralTransfers
from .objective import MaleoSOAPIEObjectiveGeneralTransfers
from .diagnosis import MaleoSOAPIEDiagnosisGeneralTransfers
from .assessment import MaleoSOAPIEAssessmentGeneralTransfers
from .plan import MaleoSOAPIEPlanGeneralTransfers
from .intervention import MaleoSOAPIEInterventionGeneralTransfers
from .evaluation import MaleoSOAPIEEvaluationGeneralTransfers
from .soapie import MaleoSOAPIESOAPIEGeneralTransfers

class MaleoSOAPIEGeneralTransfers:
    Subjective = MaleoSOAPIESubjectiveGeneralTransfers
    VitalSign = MaleoSOAPIEVitalSignGeneralTransfers
    Objective = MaleoSOAPIEObjectiveGeneralTransfers
    Diagnosis = MaleoSOAPIEDiagnosisGeneralTransfers
    Assessment = MaleoSOAPIEAssessmentGeneralTransfers
    Plan = MaleoSOAPIEPlanGeneralTransfers
    Intervention = MaleoSOAPIEInterventionGeneralTransfers
    Evaluation = MaleoSOAPIEEvaluationGeneralTransfers
    SOAPIE = MaleoSOAPIESOAPIEGeneralTransfers

__all__ = [
    "MaleoSOAPIEGeneralTransfers",
    "MaleoSOAPIESubjectiveGeneralTransfers",
    "MaleoSOAPIEVitalSignGeneralTransfers",
    "MaleoSOAPIEObjectiveGeneralTransfers",
    "MaleoSOAPIEDiagnosisGeneralTransfers",
    "MaleoSOAPIEAssessmentGeneralTransfers",
    "MaleoSOAPIEPlanGeneralTransfers",
    "MaleoSOAPIEInterventionGeneralTransfers",
    "MaleoSOAPIEEvaluationGeneralTransfers",
    "MaleoSOAPIESOAPIEGeneralTransfers"
]