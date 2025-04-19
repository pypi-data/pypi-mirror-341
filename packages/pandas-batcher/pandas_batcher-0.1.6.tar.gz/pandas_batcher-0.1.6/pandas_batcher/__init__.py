# src/pandas_batcher/__init__.py
"""
pandas‑batcher
==============

Thin wrapper so users can write either ::

    import pandas_batcher
    from pandas_batcher import PandasBatcher

while the implementation remains in :pymod:`pandas_batcher.py`.
"""
from .pandas_batcher import *
from importlib import import_module as _im

# Keep version number in one place ‑‑ e.g. inside the file itself
__version__ = getattr(_module, "__version__", "0.1.0")