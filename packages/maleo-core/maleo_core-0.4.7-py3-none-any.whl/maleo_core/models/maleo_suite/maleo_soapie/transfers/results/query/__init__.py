# This file serves all MaleoSOAPIE's query results

from __future__ import annotations
from .subjective import MaleoSOAPIESubjectiveQueryResults
from .vital_sign import MaleoSOAPIEVitalSignQueryResults
from .objective import MaleoSOAPIEObjectiveQueryResults
from .diagnosis import MaleoSOAPIEDiagnosisQueryResults
from .assessment import MaleoSOAPIEAssessmentQueryResults
from .plan import MaleoSOAPIEPlanQueryResults
from .intervention import MaleoSOAPIEInterventionQueryResults
from .evaluation import MaleoSOAPIEEvaluationQueryResults
from .soapie import MaleoSOAPIESOAPIEQueryResults

class MaleoSOAPIEQueryResults:
    Subjective = MaleoSOAPIESubjectiveQueryResults
    VitalSign = MaleoSOAPIEVitalSignQueryResults
    Objective = MaleoSOAPIEObjectiveQueryResults
    Diagnosis = MaleoSOAPIEDiagnosisQueryResults
    Assessment = MaleoSOAPIEAssessmentQueryResults
    Plan = MaleoSOAPIEPlanQueryResults
    Intervention = MaleoSOAPIEInterventionQueryResults
    Evaluation = MaleoSOAPIEEvaluationQueryResults
    SOAPIE = MaleoSOAPIESOAPIEQueryResults

__all__ = [
    "MaleoSOAPIEQueryResults",
    "MaleoSOAPIESubjectiveQueryResults",
    "MaleoSOAPIEVitalSignQueryResults",
    "MaleoSOAPIEObjectiveQueryResults",
    "MaleoSOAPIEDiagnosisQueryResults",
    "MaleoSOAPIEAssessmentQueryResults",
    "MaleoSOAPIEPlanQueryResults",
    "MaleoSOAPIEInterventionQueryResults",
    "MaleoSOAPIEEvaluationQueryResults",
    "MaleoSOAPIESOAPIEQueryResults"
]