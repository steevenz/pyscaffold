#!/usr/bin/env python3
# src/services/cli.py
#
# This file is part of the PyScaffold package.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
# @author         Steeve Andrian Salim
# @copyright      Copyright (c) Steeve Andrian Salim
#
"""CLI Service untuk PyScaffold - Ultimate Python Project Boilerplate Generator
Menyediakan interface command line yang sederhana dan interaktif seperti Laravel Artisan
"""

import os
import sys
from typing import Optional, Dict, Any

from ..core.generators import ProjectType
from ..core.scaffold import scaffold
from ..core.config import get_config_manager


class CLIService:
    """Service untuk menangani CLI interface yang sederhana dan interaktif."""
    
    def __init__(self):
        self.config_manager = get_config_manager()
        
    def show_welcome(self):
        """Menampilkan welcome message yang menarik."""
        print("="*70)
        print("🚀 PyScaffold - Ultimate Python Project Boilerplate Generator")
        print("="*70)
        print()
        print("Stop the boilerplate madness! Generate professional Python projects in seconds, not hours.")
        print()
        print("Created by: Steeven Andrian (https://github.com/steevenz)")
        print("="*70)
        print()
        
    def show_project_types(self):
        """Menampilkan tabel project types yang tersedia."""
        print("📋 Available Project Types")
        print("-" * 70)
        print(f"{'No':<4} {'Type':<15} {'Description'}")
        print("-" * 70)
        
        project_types = [
            ("1", "STANDARD", "Standard Python project with basic structure"),
            ("2", "DATA_SCIENCE", "Data science project with Jupyter, pandas, etc."),
            ("3", "WEB_API", "Web API project with FastAPI framework"),
            ("4", "CLI_TOOL", "Command line tool with Click framework"),
            ("5", "AUTOMATION", "Automation scripts with scheduling support"),
            ("6", "CUSTOM", "Custom project with user-defined structure")
        ]
        
        for num, ptype, desc in project_types:
            print(f"{num:<4} {ptype:<15} {desc}")
            
        print("-" * 70)
        print()
        
    def get_project_type(self) -> ProjectType:
        """Meminta user memilih project type."""
        while True:
            choice = input("Select project type (1-6) [default: 1]: ").strip() or "1"
            
            if choice not in ["1", "2", "3", "4", "5", "6"]:
                 print("Invalid choice. Please select 1-6.")
                 continue
            
            type_mapping = {
                "1": ProjectType.STANDARD,
                "2": ProjectType.DATA_SCIENCE,
                "3": ProjectType.WEB_API,
                "4": ProjectType.CLI_TOOL,
                "5": ProjectType.AUTOMATION,
                "6": ProjectType.CUSTOM
            }
            
            return type_mapping[choice]
            
    def get_project_info(self) -> Dict[str, Any]:
        """Mengumpulkan informasi project dari user."""
        print("📝 Project Information")
        print()
        
        # Project name (Title Case)
        project_name_input = input("Project Name [default: My Project]: ").strip() or "My Project"
        # Auto-correct to Title Case
        project_name = project_name_input.title()
        if project_name != project_name_input:
            print(f"→ Auto-corrected to Title Case: {project_name}")
        
        # Generate project directory (snake_case) from project name
        import re
        project_directory = re.sub(r'[^a-zA-Z0-9\s-]', '', project_name.lower())
        project_directory = re.sub(r'[\s-]+', '_', project_directory.strip())
        
        # Allow user to edit project directory manually
        project_directory = input(f"Project Directory (folder name) [default: {project_directory}]: ").strip() or project_directory
        
        # Validate project directory
        while True:
            if self._is_valid_project_directory(project_directory):
                break
            else:
                print("❌ Invalid project directory. Use lowercase letters, numbers, and underscores only.")
                project_directory = input("Project Directory (folder name) [default: my_project]: ").strip() or "my_project"
        
        # Optional project code (free format)
        project_code = input("Project Code (optional alias, any format): ").strip()
        if not project_code:
            project_code = None
        
        # Project target directory
        default_target = f"outputs/projects/{project_directory}"
        target_directory = input(f"Project Target Directory (where to create project) [default: {default_target}]: ").strip() or default_target
        
        # Author name
        author = input("Author Name [default: Your Name]: ").strip() or "Your Name"
        
        # Email
        email = input("Email [default: your.email@example.com]: ").strip() or "your.email@example.com"
        
        # Project type
        self.show_project_types()
        project_type = self.get_project_type()
        
        # License selection
        print("\n📄 License Selection")
        print("\nChoose a license for your project:")
        print("1. MIT License")
        print("2. Apache 2.0 License")
        print("3. GPL 3.0 License")
        print("4. BSD 3-Clause License")
        print("5. Company Based Commercial License")
        print("6. Personal Based Commercial License")
        print("7. Company Private License")
        print("8. Personal Private License")
        print("9. No License")
        
        while True:
            license_choice = input("Select License Type (1-9) [default: 1]: ").strip() or "1"
            if license_choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                break
            print("Invalid choice. Please select 1-9.")
        
        license_mapping = {
            "1": "MIT",
            "2": "Apache-2.0",
            "3": "GPL-3.0",
            "4": "BSD-3-Clause",
            "5": "Commercial-Company",
            "6": "Commercial-Personal",
            "7": "Private-Company",
            "8": "Private-Personal",
            "9": None
        }
        
        license_name = license_mapping[license_choice]
        
        # Optional features
        print()
        print("🔧 Optional Features")
        
        include_ai_input = input("Include AI/ML Modules? (y/N) [default: N]: ").strip().lower()
        include_ai = include_ai_input in ['y', 'yes']
        
        include_trainer_input = input("Include Training/Testing Utilities? (y/N) [default: N]: ").strip().lower()
        include_trainer = include_trainer_input in ['y', 'yes']
        
        return {
            'project_name': project_name,
            'project_directory': project_directory,
            'project_code': project_code,
            'target_directory': target_directory,
            'author': author,
            'email': email,
            'project_type': project_type,
            'license_name': license_name if license_name != "None" else None,
            'include_ai': include_ai,
            'include_trainer': include_trainer
        }
        
    def _is_valid_project_directory(self, name: str) -> bool:
        """Validasi project directory name."""
        import re
        pattern = r'^[a-z0-9][a-z0-9_]*[a-z0-9]$|^[a-z0-9]$'
        return bool(re.match(pattern, name)) and len(name) >= 1
        
    def show_summary(self, project_info: Dict[str, Any]):
        """Menampilkan ringkasan project yang akan dibuat."""
        print()
        
        project_code_text = f" ({project_info['project_code']})" if project_info['project_code'] else ""
        
        print("📋 Project Summary")
        print("=" * 50)
        print(f"Project Name: {project_info['project_name']}{project_code_text}")
        print(f"Project Directory: {project_info['project_directory']}")
        print(f"Target Directory: {project_info['target_directory']}")
        print(f"Author: {project_info['author']}")
        print(f"Email: {project_info['email']}")
        print(f"Type: {project_info['project_type'].value}")
        print(f"License: {project_info['license_name'] or 'None'}")
        print(f"AI Modules: {'Yes' if project_info['include_ai'] else 'No'}")
        print(f"Training Utils: {'Yes' if project_info['include_trainer'] else 'No'}")
        print("=" * 50)
        print()
        
    def create_project(self, project_info: Dict[str, Any]) -> bool:
        """Membuat project dengan progress indicator."""
        print("🚀 Creating project...")
        print()
        
        def progress_callback(message: str):
            print(f"  → {message}")
            
        try:
            # Use target_directory directly as the full path
            target_path = project_info['target_directory']
            
            success = scaffold(
                project_path=target_path,
                author=project_info['author'],
                email=project_info['email'],
                project_type=project_info['project_type'],
                license_name=project_info['license_name'],
                include_ai=project_info['include_ai'],
                include_trainer=project_info['include_trainer'],
                progress_callback=progress_callback,
                project_name=project_info['project_name'],
                project_code=project_info['project_code']
            )
            
            if success:
                self.show_success(project_info['project_directory'], target_path)
                return True
            else:
                print("❌ Failed to create project")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
            
    def show_success(self, project_directory: str, target_path: str):
        """Menampilkan pesan sukses dan next steps."""
        import platform
        
        print()
        
        # Detect OS for appropriate setup script
        is_windows = platform.system().lower() == 'windows'
        setup_script = ".\\bin\\setup.ps1" if is_windows else "./bin/setup.sh"
        
        print("🎉 Success")
        print("=" * 60)
        print(f"✅ Project '{project_directory}' created successfully!")
        print(f"📁 Location: {target_path}")
        print()
        print("Next steps:")
        print(f"  1. cd {target_path}")
        print(f"  2. {setup_script}")
        print("     • This script automatically creates venv, activates it, and installs dependencies")
        print(f"     • Use {setup_script} --clean for clean setup (removes existing venv, clears cache)")
        print()
        print("The setup script handles everything for you! 🚀✨")
        print("=" * 60)
        
    def run(self):
        """Menjalankan CLI interface utama."""
        try:
            # Welcome
            self.show_welcome()
            
            # Collect project info
            project_info = self.get_project_info()
            
            # Show summary
            self.show_summary(project_info)
            
            # Confirm creation
            while True:
                confirm = input("Create this project? (Y/n): ").strip().lower()
                if confirm in ['', 'y', 'yes']:
                    success = self.create_project(project_info)
                    if not success:
                        sys.exit(1)
                    break
                elif confirm in ['n', 'no']:
                    print("Project creation cancelled.")
                    break
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")
            sys.exit(1)


def run_cli():
    """Entry point untuk CLI mode."""
    cli = CLIService()
    cli.run()