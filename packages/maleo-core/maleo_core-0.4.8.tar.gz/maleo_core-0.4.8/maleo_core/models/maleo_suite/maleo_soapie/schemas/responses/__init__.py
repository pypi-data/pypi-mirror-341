# This file serves all MaleoSOAPIE's responses schemas

from __future__ import annotations
from .services import MaleoSOAPIEServicesResponsesSchemas

class MaleoSOAPIEResponsesSchemas:
    Services = MaleoSOAPIEServicesResponsesSchemas

__all__ = ["MaleoSOAPIEResponsesSchemas", "MaleoSOAPIEServicesResponsesSchemas"]