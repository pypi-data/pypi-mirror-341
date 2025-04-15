# This file serves all MaleoSOAPIE's Cient Parameters

from __future__ import annotations
from .subjective import MaleoSOAPIESubjectiveClientParameters
from .objective import MaleoSOAPIEObjectiveClientParameters
from .vital_sign import MaleoSOAPIEVitalSignClientParameters
from .assessment import MaleoSOAPIEAssessmentClientParameters
from .diagnosis import MaleoSOAPIEDiagnosisClientParameters
from .plan import MaleoSOAPIEPlanClientParameters
from .intervention import MaleoSOAPIEInterventionClientParameters
from .evaluation import MaleoSOAPIEEvaluationClientParameters
from .soapie import MaleoSOAPIESOAPIEClientParameters

class MaleoSOAPIEClientParameters:
    Subjective = MaleoSOAPIESubjectiveClientParameters
    VitalSign = MaleoSOAPIEVitalSignClientParameters
    Objective = MaleoSOAPIEObjectiveClientParameters
    Diagnosis = MaleoSOAPIEDiagnosisClientParameters
    Assessment = MaleoSOAPIEAssessmentClientParameters
    Plan = MaleoSOAPIEPlanClientParameters
    Intervention = MaleoSOAPIEInterventionClientParameters
    Evaluation = MaleoSOAPIEEvaluationClientParameters
    SOAPIE = MaleoSOAPIESOAPIEClientParameters

__all__ = [
    "MaleoSOAPIEClientParameters",
    "MaleoSOAPIESubjectiveClientParameters",
    "MaleoSOAPIEVitalSignClientParameters",
    "MaleoSOAPIEObjectiveClientParameters",
    "MaleoSOAPIEDiagnosisClientParameters",
    "MaleoSOAPIEAssessmentClientParameters",
    "MaleoSOAPIEPlanClientParameters",
    "MaleoSOAPIEInterventionClientParameters",
    "MaleoSOAPIEEvaluationClientParameters",
    "MaleoSOAPIESOAPIEClientParameters"
]