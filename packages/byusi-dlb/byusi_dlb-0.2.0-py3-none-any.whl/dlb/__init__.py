"""
DLB - Advanced Download Library

Copyright (c) 2025 ByUsi
Licensed under MIT License
"""

__version__ = "0.2.0"
__author__ = "ByUsi"

from .core import download_manager
from .config import load_config, save_config

__all__ = [
    "download_manager",
    "load_config",
    "save_config",
    "__version__",
    "__author__"
]

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())