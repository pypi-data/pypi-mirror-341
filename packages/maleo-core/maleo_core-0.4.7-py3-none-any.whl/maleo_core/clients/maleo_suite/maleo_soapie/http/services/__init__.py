from .subjective import MaleoSOAPIESubjectiveHTTPService
from .vital_sign import MaleoSOAPIEVitalSignHTTPService
from .objective import MaleoSOAPIEObjectiveHTTPService
from .diagnosis import MaleoSOAPIEDiagnosisHTTPService
from .assessment import MaleoSOAPIEAssessmentHTTPService
from .plan import MaleoSOAPIEPlanHTTPService
from .intervention import MaleoSOAPIEInterventionHTTPService
from .evaluation import MaleoSOAPIEEvaluationHTTPService
from .soapie import MaleoSOAPIESOAPIEHTTPService

class MaleoSOAPIEHTTPServices:
    Subjective = MaleoSOAPIESubjectiveHTTPService
    VitalSign = MaleoSOAPIEVitalSignHTTPService
    Objective = MaleoSOAPIEObjectiveHTTPService
    Diagnosis = MaleoSOAPIEDiagnosisHTTPService
    Assessment = MaleoSOAPIEAssessmentHTTPService
    Plan = MaleoSOAPIEPlanHTTPService
    Intervention = MaleoSOAPIEInterventionHTTPService
    Evaluation = MaleoSOAPIEEvaluationHTTPService
    SOAPIE = MaleoSOAPIESOAPIEHTTPService