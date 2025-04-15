# This file serves all MaleoSOAPIE's HTTP Client Services Results

from __future__ import annotations
from .subjective import MaleoSOAPIEHTTPClientSubjectiveServiceResults
from .vital_sign import MaleoSOAPIEHTTPClientVitalSignServiceResults
from .objective import MaleoSOAPIEHTTPClientObjectiveServiceResults
from .diagnosis import MaleoSOAPIEHTTPClientDiagnosisServiceResults
from .assessment import MaleoSOAPIEHTTPClientAssessmentServiceResults
from .plan import MaleoSOAPIEHTTPClientPlanServiceResults
from .intervention import MaleoSOAPIEHTTPClientInterventionServiceResults
from .evaluation import MaleoSOAPIEHTTPClientEvaluationServiceResults
from .soapie import MaleoSOAPIEHTTPClientSOAPIEServiceResults

class MaleoSOAPIEHTTPClientServicesResults:
    Subjective = MaleoSOAPIEHTTPClientSubjectiveServiceResults
    VitalSign = MaleoSOAPIEHTTPClientVitalSignServiceResults
    Objective = MaleoSOAPIEHTTPClientObjectiveServiceResults
    Diagnosis = MaleoSOAPIEHTTPClientDiagnosisServiceResults
    Assessment = MaleoSOAPIEHTTPClientAssessmentServiceResults
    Plan = MaleoSOAPIEHTTPClientPlanServiceResults
    Intervention = MaleoSOAPIEHTTPClientInterventionServiceResults
    Evaluation = MaleoSOAPIEHTTPClientEvaluationServiceResults
    SOAPIE = MaleoSOAPIEHTTPClientSOAPIEServiceResults

__all__ = [
    "MaleoSOAPIEHTTPClientServicesResults",
    "MaleoSOAPIEHTTPClientSubjectiveServiceResults",
    "MaleoSOAPIEHTTPClientVitalSignServiceResults",
    "MaleoSOAPIEHTTPClientObjectiveServiceResults",
    "MaleoSOAPIEHTTPClientDiagnosisServiceResults",
    "MaleoSOAPIEHTTPClientAssessmentServiceResults",
    "MaleoSOAPIEHTTPClientPlanServiceResults",
    "MaleoSOAPIEHTTPClientInterventionServiceResults",
    "MaleoSOAPIEHTTPClientEvaluationServiceResults",
    "MaleoSOAPIEHTTPClientSOAPIEServiceResults"
]