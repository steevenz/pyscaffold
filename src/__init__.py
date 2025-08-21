#!/usr/bin/env python3
# src/__init__.py
#
# This file is part of the PyScaffold package.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
# @author         Steeve Andrian Salim
# @copyright      Copyright (c) Steeve Andrian Salim
#
"""
src/__init__.py
PyScaffold main package
"""

__version__ = "2.0.0"
__author__ = "PyScaffold Team"
__description__ = "Ultimate Python Project Boilerplate Generator"

# Import main functionality
from .core.scaffold import scaffold
from .core.config import get_config, get_config_manager
from .helpers.utils import validate_project_name, get_git_user
from .services.cli import run_cli

__all__ = [
    "scaffold",
    "get_config",
    "get_config_manager",
    "validate_project_name",
    "get_git_user",
    "run_cli",
    "__version__",
    "__author__",
    "__description__"
]