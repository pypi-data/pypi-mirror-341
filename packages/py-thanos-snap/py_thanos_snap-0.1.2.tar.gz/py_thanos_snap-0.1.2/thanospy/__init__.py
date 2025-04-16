# thanospy/__init__.py
"""
ThanosPy: Perfectly balanced data structures... as all things should be.

Provides a function to randomly remove half the content from various
Python built-in types.
"""

from .core import snap

__version__ = "0.1.2"

__all__ = [
    "snap",
    "__version__",
]
