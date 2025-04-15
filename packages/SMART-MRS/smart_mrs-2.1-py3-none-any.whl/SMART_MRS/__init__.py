# init file for SMART_MRS package

# module import declaration
from . import applied
from . import artifacts
from . import IO
from . import support

# Wildcard (*) import declaration
__all__ = ["applied", "artifacts", "IO", "support"]

# variable declaration
VERSION = "2.1"
LAST_UPDATED = "2025_04_14"
AUTHORS = "Bugler et al."
