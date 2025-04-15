# This file serves all MaleoAccess's Results

from __future__ import annotations
from .client import MaleoAccessClientResults
from .service import MaleoAccessServiceResults
from .query import MaleoAccessQueryResults
from .general import MaleoAccessGeneralResults

class MaleoAccessResults:
    Client = MaleoAccessClientResults
    Service = MaleoAccessServiceResults
    Query = MaleoAccessQueryResults
    General = MaleoAccessGeneralResults

__all__ = [
    "MaleoAccessResults",
    "MaleoAccessClientResults",
    "MaleoAccessServiceResults",
    "MaleoAccessQueryResults",
    "MaleoAccessGeneralResults"
]