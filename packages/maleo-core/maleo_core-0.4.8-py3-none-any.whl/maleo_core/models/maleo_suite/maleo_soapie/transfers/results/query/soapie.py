from __future__ import annotations
from pydantic import Field
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.subjective import MaleoSOAPIESubjectiveQueryResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.objective import MaleoSOAPIEObjectiveQueryResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.assessment import MaleoSOAPIEAssessmentQueryResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.plan import MaleoSOAPIEPlanQueryResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.intervention import MaleoSOAPIEInterventionQueryResults
from maleo_core.models.maleo_suite.maleo_soapie.transfers.results.query.evaluation import MaleoSOAPIEEvaluationQueryResults

class MaleoSOAPIESOAPIEQueryResults:
    class Get(BaseServiceQueryResults.Get):
        subjective:Optional[MaleoSOAPIESubjectiveQueryResults.Get] = Field(..., description="Subjective")
        objective:Optional[MaleoSOAPIEObjectiveQueryResults.Get] = Field(..., description="Objective")
        assessment:Optional[MaleoSOAPIEAssessmentQueryResults.Get] = Field(..., description="Assessment")
        plan:Optional[MaleoSOAPIEPlanQueryResults.Get] = Field(..., description="Plan")
        intervention:Optional[MaleoSOAPIEInterventionQueryResults.Get] = Field(..., description="Intervention")
        evaluation:Optional[MaleoSOAPIEEvaluationQueryResults.Get] = Field(..., description="Evaluation")

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoSOAPIESOAPIEQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoSOAPIESOAPIEQueryResults.Get]