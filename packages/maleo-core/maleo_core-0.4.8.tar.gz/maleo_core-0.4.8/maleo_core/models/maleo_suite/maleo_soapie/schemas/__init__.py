# This file serves all MaleoSOAPIE's Schemas

from __future__ import annotations
from .responses import MaleoSOAPIEResponsesSchemas

class MaleoSOAPIESchemas:
    Responses = MaleoSOAPIEResponsesSchemas

__all__ = ["MaleoSOAPIESchemas", "MaleoSOAPIEResponsesSchemas"]