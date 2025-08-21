#!/usr/bin/env python3
# run.py
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
run.py
Alternative entry point for PyScaffold - Multi runner
Supports different execution modes and environments
"""

from __future__ import annotations

import sys
import os
import argparse
from pathlib import Path
import logging

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from src.core.config import get_config
    from src.main import main as main_entry
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running from the project root directory.")
    sys.exit(1)

def setup_logging():
    """Setup logging configuration."""
    try:
        config = get_config()
        log_level = getattr(logging, config.logging.level.upper(), logging.INFO)
        log_format = config.logging.format
        log_file = config.logging.file
        
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
    except Exception as e:
        # Fallback logging configuration
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        logging.warning(f"Could not load logging config: {e}. Using defaults.")

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="PyScaffold - Python Project Scaffolding Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                    # Run PyScaffold
  python run.py --cli              # Force CLI mode
  python run.py --version          # Show version
  python run.py --config-info      # Show configuration info

For more information, visit: https://github.com/yourusername/pyscaffold
        """
    )
    
    # UI mode options
    parser.add_argument(
        "--cli", 
        action="store_true", 
        help="Force CLI mode"
    )
    
    # Information options
    parser.add_argument(
        "--version", 
        action="store_true", 
        help="Show version information"
    )
    parser.add_argument(
        "--config-info", 
        action="store_true", 
        help="Show configuration information"
    )
    
    # Debug options
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug logging"
    )
    parser.add_argument(
        "--log-level", 
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set logging level"
    )
    
    return parser

def show_version():
    """Show version information."""
    try:
        # Try to read version from pyproject.toml or setup.py
        import tomllib
        pyproject_path = Path(__file__).parent / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
                version = data.get("project", {}).get("version", "unknown")
        else:
            version = "development"
    except Exception:
        version = "unknown"
    
    print(f"PyScaffold v{version}")
    print("Python Project Scaffolding Tool")
    print("")
    print(f"Python: {sys.version}")
    print(f"Platform: {sys.platform}")

def show_config_info():
    """Show configuration information."""
    try:
        config = get_config()
        print("PyScaffold Configuration:")
        print(f"  Default project type: {config.defaults.project_type}")
        print(f"  Default license: {config.defaults.license}")
        print(f"  Include AI by default: {config.defaults.include_ai}")
        print(f"  Include trainer by default: {config.defaults.include_trainer}")
        print(f"  Use boilerplate by default: {config.defaults.use_boilerplate}")
        print(f"  UI mode: {config.ui.default_mode}")
        print(f"  Log level: {config.logging.level}")
        print(f"  Log file: {config.logging.file}")
        
        # Show available project types from dependencies
        if config.dependencies:
            print("  Available project types:")
            for proj_type in config.dependencies.keys():
                print(f"    - {proj_type}")
        
    except Exception as e:
        print(f"Error loading configuration: {e}")

def determine_ui_mode(args) -> str:
    """Determine UI mode based on arguments and configuration."""
    if args.cli:
        return "cli"
    else:
        # Default to auto mode
        return "auto"

def main():
    """Main entry point for run.py."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle information requests
    if args.version:
        show_version()
        return 0
    
    if args.config_info:
        show_config_info()
        return 0
    
    # Setup logging
    setup_logging()
    
    # Override log level if specified
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.log_level:
        logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    logger = logging.getLogger(__name__)
    logger.info("Starting PyScaffold...")
    
    try:
        # Determine UI mode
        ui_mode = determine_ui_mode(args)
        logger.info(f"Using UI mode: {ui_mode}")
        
        # Prepare arguments for main entry point
        main_args = ["pyscaffold"]
        if ui_mode == "cli":
            main_args.append("--cli")
        
        # Override sys.argv for main entry point
        original_argv = sys.argv
        sys.argv = main_args
        
        try:
            # Call main entry point
            result = main_entry()
            return result if result is not None else 0
        finally:
            # Restore original argv
            sys.argv = original_argv
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())