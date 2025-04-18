"""
This module is part of the LOGS-Py Solutions library.

It provides pre-built solutions, examples, and utilities to simplify 
interactions with the LOGS public API programmatically via Python scripts. 
This library is designed to extend the functionality of the logs-py package 
and address common challenges in scientific data management workflows.
"""

import os
import glob

# Dynamically import all Python modules from the Library subfolder
module_files = glob.glob(os.path.join(os.path.dirname(__file__), "Library", "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in module_files if os.path.isfile(f) and not f.endswith("__init__.py")]

for module in __all__:
    __import__(f"logs_py_solutions.Library.{module}")