# src/pandas_batcher/__init__.py
"""
pandas‑batcher
==============

Thin wrapper so users can write either ::

    import pandas_batcher
    from pandas_batcher import PandasBatcher

while the implementation remains in :pymod:`pandas_batcher.py`.
"""
from .pandas_batcher import PandasBatcher
from importlib import import_module as _im

# Re‑export the functions/classes defined in pandas_batcher.py
_module = _im("pandas_batcher")           # finds the sibling file
globals().update(_module.__dict__)        # pull its symbols into our namespace

# Optional: expose a clean public surface
__all__ = _module.__all__ if hasattr(_module, "__all__") else sorted(
    k for k in globals() if not k.startswith("_")
)

# Keep version number in one place ‑‑ e.g. inside the file itself
__version__ = getattr(_module, "__version__", "0.1.0")