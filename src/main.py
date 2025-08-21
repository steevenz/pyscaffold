#!/usr/bin/env python3
# src/main.py
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
Main entry point untuk PyScaffold - Ultimate Python Project Boilerplate Generator
"""

import sys
import logging
from pathlib import Path
from typing import Optional

from .core.config import get_config_manager
from .services.cli import run_cli

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pyscaffold.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)





def run_cli_mode():
    """Menjalankan mode CLI yang sederhana dan interaktif."""
    logger.info("Starting CLI mode...")
    
    try:
        run_cli()
        return True
    except Exception as e:
        logger.error(f"CLI error: {e}")
        print(f"❌ Error: {e}")
        return False





def main(ui_mode: Optional[str] = None):
    """Main function untuk menjalankan PyScaffold."""
    logger.info("Starting PyScaffold...")
    
    # Always run CLI mode
    logger.info("Using CLI mode")
    return run_cli_mode()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)