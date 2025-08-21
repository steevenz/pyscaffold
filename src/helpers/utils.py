#!/usr/bin/env python3
# src/helpers/utils.py
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
src/helpers/utils.py
Utility functions for PyScaffold
"""

from __future__ import annotations

import subprocess
import sys
import importlib
from pathlib import Path
from typing import Dict, Any
import textwrap
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def install_dependencies():
    """Install required dependencies for this script."""
    dependencies = []
    
    
    # Check for tqdm
    try:
        import tqdm
    except ImportError:
        dependencies.append("tqdm>=4.66.0")
    
    # Check for rich
    try:
        import rich
    except ImportError:
        dependencies.append("rich>=13.0.0")
    
    if dependencies:
        logger.info("Installing required dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + dependencies)
            logger.info("Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False
    return True

def write(path: Path, text: str, progress_callback=None) -> None:
    """Write text to file, creating parent dirs if necessary."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    if progress_callback:
        progress_callback(f"Created file: {path}")

def banner(path: Path, author: str, filename: str, project_name: str) -> str:
    """Return a standard header comment."""
    rel = f"{project_name}/{path.relative_to(path.anchor)}" if path.is_absolute() else f"{project_name}/{path}"
    creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return textwrap.dedent(f'''"""\n    {rel}\n    Author: {author}\n    Created: {creation_date}\n    Description: Part of {project_name} project\n    """''').strip()

def validate_project_name(name: str) -> bool:
    """Check if project name is valid."""
    if not name:
        return False
    if not name.replace("_", "").isidentifier():
        return False
    if name in ("test", "src", "lib", "module", "package"):
        return False
    return True

def get_git_user() -> Dict[str, str]:
    """Try to get git user info."""
    try:
        name = subprocess.check_output(["git", "config", "user.name"], text=True).strip()
        email = subprocess.check_output(["git", "config", "user.email"], text=True).strip()
        return {name: {"email": email}}
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}

def find_available_boilerplates() -> Dict[str, Path]:
    """Find available boilerplates in the boilerplates directory."""
    boilerplates = {}
    boilerplates_dir = Path("boilerplates")
    
    if boilerplates_dir.exists():
        for boilerplate_dir in boilerplates_dir.iterdir():
            if boilerplate_dir.is_dir():
                boilerplates[boilerplate_dir.name] = boilerplate_dir
                
    return boilerplates