"""Data layer package — mock providers for market data."""

import sys
import os

_package_root = os.path.dirname(os.path.abspath(__file__))
_parent = os.path.dirname(_package_root)
if _parent not in sys.path:
    sys.path.insert(0, _parent)

from elo import ELOProvider
from fifa import FIFAProvider
from odds import OddsProvider
from asian import AsianHandicapProvider
from over_under import OverUnderProvider
from form import FormProvider
from h2h import H2HProvider

__all__ = [
    "ELOProvider",
    "FIFAProvider",
    "OddsProvider",
    "AsianHandicapProvider",
    "OverUnderProvider",
    "FormProvider",
    "H2HProvider",
]
