# This file serves all MaleoSOAPIE Services Results

from __future__ import annotations
from .subjective import MaleoSOAPIESubjectiveServiceResults
from .vital_sign import MaleoSOAPIEVitalSignServiceResults
from .objective import MaleoSOAPIEObjectiveServiceResults
from .diagnosis import MaleoSOAPIEDiagnosisServiceResults
from .assessment import MaleoSOAPIEAssessmentServiceResults
from .plan import MaleoSOAPIEPlanServiceResults
from .intervention import MaleoSOAPIEInterventionServiceResults
from .evaluation import MaleoSOAPIEEvaluationServiceResults
from .soapie import MaleoSOAPIESOAPIEServiceResults

class MaleoSOAPIEServiceResults:
    Subjective = MaleoSOAPIESubjectiveServiceResults
    VitalSign = MaleoSOAPIEVitalSignServiceResults
    Objective = MaleoSOAPIEObjectiveServiceResults
    Diagnosis = MaleoSOAPIEDiagnosisServiceResults
    Assessment = MaleoSOAPIEAssessmentServiceResults
    Plan = MaleoSOAPIEPlanServiceResults
    Intervention = MaleoSOAPIEInterventionServiceResults
    Evaluation = MaleoSOAPIEEvaluationServiceResults
    SOAPIE = MaleoSOAPIESOAPIEServiceResults

__all__ = [
    "MaleoSOAPIEServiceResults",
    "MaleoSOAPIESubjectiveServiceResults",
    "MaleoSOAPIEVitalSignServiceResults",
    "MaleoSOAPIEObjectiveServiceResults",
    "MaleoSOAPIEDiagnosisServiceResults",
    "MaleoSOAPIEAssessmentServiceResults",
    "MaleoSOAPIEPlanServiceResults",
    "MaleoSOAPIEInterventionServiceResults",
    "MaleoSOAPIEEvaluationServiceResults",
    "MaleoSOAPIESOAPIEServiceResults"
]