# This file serves all MaleoSOAPIE's models

from __future__ import annotations
from .schemas import MaleoSOAPIESchemas
from .transfers import MaleoSOAPIETransfers

class MaleoSOAPIEModels:
    Schemas = MaleoSOAPIESchemas
    Transfers = MaleoSOAPIETransfers

__all__ = ["MaleoSOAPIEModels", "MaleoSOAPIESchemas", "MaleoSOAPIETransfers"]