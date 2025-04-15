# This file serves all MaleoSOAPIE's Results

from __future__ import annotations
from .query import MaleoSOAPIEQueryResults
from .service import MaleoSOAPIEServiceResults
from .client import MaleoSOAPIEClientResults

class MaleoSOAPIEResults:
    Query = MaleoSOAPIEQueryResults
    Service = MaleoSOAPIEServiceResults
    Client = MaleoSOAPIEClientResults

__all__ = [
    "MaleoSOAPIEResults",
    "MaleoSOAPIEQueryResults",
    "MaleoSOAPIEServiceResults",
    "MaleoSOAPIEClientResults"
]