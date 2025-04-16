"""
Compatibility layer for omniagents -> agn transition.
This module re-exports everything from agn to maintain backward compatibility.
"""

import sys
import importlib

# Import all modules from agn and make them available under omniagents
from agn import *

def __getattr__(name):
    """
    Redirect imports from omniagents.X to agn.X
    """
    try:
        # Try to import the attribute from agn
        return importlib.import_module(f"agn.{name}")
    except ImportError:
        raise AttributeError(f"module 'omniagents' has no attribute '{name}'")

# Handle submodule imports like "from omniagents.core import X"
class _LazyImportModule:
    def __init__(self, name):
        self.name = name
        
    def __getattr__(self, attr):
        # Import the actual module from agn
        mod = importlib.import_module(f"agn.{self.name}")
        return getattr(mod, attr)

# Add all submodules to sys.modules to handle direct imports
for submodule in ["core", "models", "utils", "agents", "protocols", "launchers"]:
    sys.modules[f"omniagents.{submodule}"] = _LazyImportModule(submodule) 