"""
MontyCloud DAY2 SDK for Python.

This package provides a Pythonic interface to the MontyCloud DAY2 API.
"""

# Also import from montycloud for backward compatibility
import sys

# Import from the current package for the new structure
from day2._version import __version__
from day2.session import Session

sys.modules["montycloud"] = sys.modules[__name__]

__all__ = ["Session", "__version__"]
