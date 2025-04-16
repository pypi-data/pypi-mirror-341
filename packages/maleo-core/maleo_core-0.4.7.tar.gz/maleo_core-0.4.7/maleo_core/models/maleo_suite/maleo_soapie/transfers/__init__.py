# This file serves all MaleoSOAPIE's Transfers

from __future__ import annotations
from .general import MaleoSOAPIEGeneralTransfers
from .parameters import MaleoSOAPIEParameters
from .results import MaleoSOAPIEResults

class MaleoSOAPIETransfers:
    General = MaleoSOAPIEGeneralTransfers
    Parameters = MaleoSOAPIEParameters
    Results = MaleoSOAPIEResults

__all__ = [
    "MaleoSOAPIETransfers",
    "MaleoSOAPIEGeneralTransfers",
    "MaleoSOAPIEParameters",
    "MaleoSOAPIEResults"
]