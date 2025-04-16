# This file serves all MaleoSOAPIE's Client Results

from __future__ import annotations
from .http import MaleoSOAPIEHTTPClientResults

class MaleoSOAPIEClientResults:
    HTTP = MaleoSOAPIEHTTPClientResults

__all__ = ["MaleoSOAPIEClientResults", "MaleoSOAPIEHTTPClientResults"]