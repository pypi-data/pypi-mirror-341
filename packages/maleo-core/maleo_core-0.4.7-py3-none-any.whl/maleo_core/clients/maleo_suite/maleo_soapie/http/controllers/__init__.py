from .subjective import MaleoSOAPIESubjectiveHTTPController
from .vital_sign import MaleoSOAPIEVitalSignHTTPController
from .objective import MaleoSOAPIEObjectiveHTTPController
from .diagnosis import MaleoSOAPIEDiagnosisHTTPController
from .assessment import MaleoSOAPIEAssessmentHTTPController
from .plan import MaleoSOAPIEPlanHTTPController
from .intervention import MaleoSOAPIEInterventionHTTPController
from .evaluation import MaleoSOAPIEEvaluationHTTPController
from .soapie import MaleoSOAPIESOAPIEHTTPController

class MaleoSOAPIEHTTPControllers:
    Subjective = MaleoSOAPIESubjectiveHTTPController
    VitalSign = MaleoSOAPIEVitalSignHTTPController
    Objective = MaleoSOAPIEObjectiveHTTPController
    Diagnosis = MaleoSOAPIEDiagnosisHTTPController
    Assessment = MaleoSOAPIEAssessmentHTTPController
    Plan = MaleoSOAPIEPlanHTTPController
    Intervention = MaleoSOAPIEInterventionHTTPController
    Evaluation = MaleoSOAPIEEvaluationHTTPController
    SOAPIE = MaleoSOAPIESOAPIEHTTPController