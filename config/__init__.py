"""Config package for the Betting Structure Engine."""

import sys
import os

_package_root = os.path.dirname(os.path.abspath(__file__))
_parent = os.path.dirname(_package_root)
if _parent not in sys.path:
    sys.path.insert(0, _parent)

from settings import Settings

__all__ = ["Settings"]
