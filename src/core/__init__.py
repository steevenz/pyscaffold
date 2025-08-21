#!/usr/bin/env python3
# src/core/__init__.py
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
src/core/__init__.py
Core functionality for PyScaffold
"""

from .scaffold import scaffold, license_content, main_py_content, create_test_files
from .config import get_config, get_config_manager, PyScaffoldConfig
from .generators import (
    gitignore, env_boilerplate, pyproject, readme, requirements,
    dockerfile, docker_compose, setup_sh, setup_bat, setup_ps1,
    copy_boilerplate
)

__all__ = [
    "scaffold",
    "get_config",
    "get_config_manager",
    "PyScaffoldConfig",
    "gitignore",
    "env_boilerplate",
    "pyproject",
    "readme",
    "requirements",
    "dockerfile",
    "docker_compose",
    "setup_sh",
    "setup_bat",
    "setup_ps1",
    "copy_boilerplate",
    "license_content",
    "main_py_content",
    "create_test_files"
]