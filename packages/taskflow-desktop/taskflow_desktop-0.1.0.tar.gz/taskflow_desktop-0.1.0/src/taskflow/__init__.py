"""
TaskFlow: A comprehensive task management application.

This package provides tools and utilities for task tracking and management.
"""

from typing import TYPE_CHECKING

__version__ = "0.1.0"
__author__ = "Erton Miranda"
__email__ = "erton.miranda@quatto.com.br"

# Import key modules for easy access
from . import models
from . import utils
from . import cli
from . import config
from . import security
from . import reports

# Type checking imports
if TYPE_CHECKING:
    from .models import Task, User, Project
    from .utils import validate_input, format_datetime
    from .cli import main
    from .config import Settings
    from .security import authenticate
    from .reports import generate_report

# Optional: Define what gets imported with `from taskflow import *`
__all__ = [
    'models',
    'utils',
    'cli',
    'config',
    'security',
    'reports',
    '__version__',
    '__author__'
]

# Optional: Expose key classes and functions at package level
from .models import Task, User, Project
from .utils import validate_input, format_datetime
from .cli import main
from .config import Settings
from .security import authenticate
from .reports import generate_report

# Add these to __all__ if you want them directly importable
__all__ += [
    'Task', 'User', 'Project',
    'validate_input', 'format_datetime',
    'main', 'Settings',
    'authenticate', 'generate_report'
]
