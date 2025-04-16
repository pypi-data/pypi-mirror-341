# This file serves all MaleoSOAPIE's Parameters

from __future__ import annotations
from .general import MaleoSOAPIEGeneralParameters
from .service import MaleoSOAPIEServiceParameters
from .client import MaleoSOAPIEClientParameters

class MaleoSOAPIEParameters:
    General = MaleoSOAPIEGeneralParameters
    Service = MaleoSOAPIEServiceParameters
    Client = MaleoSOAPIEClientParameters

__all__ = [
    "MaleoSOAPIEParameters",
    "MaleoSOAPIEGeneralParameters",
    "MaleoSOAPIEServiceParameters",
    "MaleoSOAPIEClientParameters"
]