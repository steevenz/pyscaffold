#!/usr/bin/env python3
# src/core/scaffold.py
#
# This file is part of the PyScaffold package.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
# @author         Steeve Andrian Salim
# @copyright      Copyright (c) Steeve Andrian Salim
#
"""src/core/scaffold.py
Main scaffolding functions for PyScaffold - Ultimate Python Project Boilerplate Generator
"""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Optional
from datetime import datetime
import logging

from .generators import (
    ProjectType, gitignore, env_boilerplate, pyproject, requirements,
    readme, docker_compose, dockerfile, setup_sh, setup_bat, setup_ps1,
    copy_boilerplate
)
from ..helpers.utils import write, banner
from .config import get_config

logger = logging.getLogger(__name__)

def license_content(license_name: str, author: str, year: int) -> str:
    """Generate license content based on license type."""
    if license_name == "MIT":
        return textwrap.dedent(f"""
            MIT License

            Copyright (c) {year} {author}

            Permission is hereby granted, free of charge, to any person obtaining a copy
            of this software and associated documentation files (the "Software"), to deal
            in the Software without restriction, including without limitation the rights
            to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
            copies of the Software, and to permit persons to whom the Software is
            furnished to do so, subject to the following conditions:

            The above copyright notice and this permission notice shall be included in all
            copies or substantial portions of the Software.

            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
            IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
            FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
            AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
            LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
            OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
            SOFTWARE.
        """).lstrip()
    elif license_name == "Apache-2.0":
        return textwrap.dedent(f"""
            Apache License
            Version 2.0, January 2004
            http://www.apache.org/licenses/

            Copyright {year} {author}

            Licensed under the Apache License, Version 2.0 (the "License");
            you may not use this file except in compliance with the License.
            You may obtain a copy of the License at

                http://www.apache.org/licenses/LICENSE-2.0

            Unless required by applicable law or agreed to in writing, software
            distributed under the License is distributed on an "AS IS" BASIS,
            WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
            See the License for the specific language governing permissions and
            limitations under the License.
        """).lstrip()
    else:
        return f"Copyright (c) {year} {author}. All rights reserved."

def main_py_content(project_name: str, author: str, project_type: ProjectType) -> str:
    """Generate main.py content based on project type."""
    base_content = textwrap.dedent(f'''
        """
        {project_name}/src/main.py
        Author: {author}
        Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        Description: Main entry point for {project_name}
        """

        import sys
        from pathlib import Path
        import logging
        from dotenv import load_dotenv

        # Load environment variables
        load_dotenv()

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('logs/app.log')
            ]
        )
        logger = logging.getLogger(__name__)

        def cli():
            """Main CLI entry point."""
            logger.info("Starting {project_name}...")
            print("Hello from src.main")
            logger.info("{project_name} completed successfully")
    ''')
    
    if project_type == ProjectType.DATA_SCIENCE:
        base_content += textwrap.dedent('''
            # Data Science specific imports
            import pandas as pd
            import numpy as np
            
            def load_data(data_path: str) -> pd.DataFrame:
                """Load dataset from path."""
                print(f"Loading data from {data_path}")
                # Implementation here
                return pd.DataFrame()
                
            if __name__ == "__main__":
                cli()
        ''')
    elif project_type == ProjectType.WEB_API:
        base_content += textwrap.dedent('''
            # Web API specific imports
            from fastapi import FastAPI
            import uvicorn
            
            app = FastAPI(title=f"{project_name}")
            
            @app.get("/")
            async def root():
                return {"message": "Hello World"}
                
            if __name__ == "__main__":
                uvicorn.run(app, host="0.0.0.0", port=8000)
        ''')
    elif project_type == ProjectType.CLI_TOOL:
        base_content += textwrap.dedent('''
            # CLI specific imports
            import click
            
            @click.group()
            def cli():
                """{project_name} CLI tool."""
                pass
                
            @cli.command()
            def hello():
                """Say hello."""
                click.echo("Hello World!")
                
            if __name__ == "__main__":
                cli()
        ''')
    else:
        base_content += textwrap.dedent('''
            if __name__ == "__main__":
                cli()
        ''')
    
    return base_content

def create_test_files(project_path: Path, author: str, project_name: str, project_type: ProjectType, progress_callback=None) -> None:
    """Create test files based on project type."""
    test_init = project_path / "tester" / "__init__.py"
    write(test_init, banner(test_init, author, "__init__.py", project_name), progress_callback)
    
    test_main = project_path / "tester" / "test_main.py"
    test_content = textwrap.dedent(f'''
        """
        {project_name}/tester/test_main.py
        Author: {author}
        Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        Description: Tests for {project_name} project
        """

        import pytest
        from src.main import cli

        def test_cli(capsys):
            """Test CLI command."""
            cli()
            captured = capsys.readouterr()
            assert "Hello from src.main" in captured.out
    ''')
    write(test_main, test_content, progress_callback)

def scaffold(project_path, author: str, email: str, project_type: ProjectType, 
             license_name: str, include_ai: bool, include_trainer: bool, 
             use_boilerplate: bool = False, boilerplate_path: Optional[Path] = None,
             progress_callback=None, project_name: str = None, project_code: str = None) -> bool:
    """Create all folders & files with updated structure."""
    # Convert to Path object if string is provided
    if isinstance(project_path, str):
        project_path = Path(project_path)
    
    # Use provided project_name (Title Case) or fallback to directory name
    if project_name is None:
        project_name = project_path.name
    
    year = datetime.now().year

    # Load configuration
    from .config import get_config_manager
    config_manager = get_config_manager()
    config = config_manager.load_config()

    # Use boilerplate if specified
    if use_boilerplate and boilerplate_path:
        if progress_callback:
            progress_callback(f"Using boilerplate: {boilerplate_path}")
        return copy_boilerplate(boilerplate_path, project_path, progress_callback)

    # Standard scaffolding with updated structure
    if progress_callback:
        progress_callback("Creating project structure...")

    # Get folder structure from config
    folders = config_manager.get_folders_for_project_type(project_type.value, include_ai, include_trainer)
    
    # Fallback to default structure if config doesn't provide folders
    if not folders:
        folders = [
            "bin",
            "caches", 
            "config",
            "datasets",
            "logs",
            "outputs",
            "src",
            "src/core",
            "src/clients", 
            "src/services",
            "src/helpers",
            "tester",
            "venv",  # Will be created by setup scripts
        ]
        
        if include_ai:
            folders.append("src/ai")
        if include_trainer:
            folders.append("trainer")
        if project_type == ProjectType.WEB_API:
            folders.extend(["src/api", "src/routers", "src/database"])
        if project_type == ProjectType.DATA_SCIENCE:
            folders.extend(["notebooks", "models", "src/features", "src/visualization"])

    # Create folders with progress
    for folder in folders:
        if folder == "venv":  # Skip venv folder creation
            continue
        folder_path = project_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        if progress_callback:
            progress_callback(f"Created directory: {folder}")

    # Files -----------------------------------------------------------
    if progress_callback:
        progress_callback("Creating project files...")
    
    write(project_path / ".gitignore", gitignore(project_type), progress_callback)
    write(project_path / ".env", env_boilerplate(project_type), progress_callback)
    write(project_path / "pyproject.toml", pyproject(author, email, project_name, project_type, project_path.name), progress_callback)
    write(project_path / "requirements.txt", requirements(project_type), progress_callback)
    write(project_path / "README.md", readme(project_name, author, email, project_type, license_name), progress_callback)
    write(project_path / "docker-compose.yml", docker_compose(project_type), progress_callback)
    write(project_path / "Dockerfile", dockerfile(project_type), progress_callback)
    
    # Add license file if specified
    if license_name != "None":
        write(project_path / "LICENSE", license_content(license_name, author, year), progress_callback)

    # Setup scripts in bin/
    write(project_path / "bin/setup.sh", setup_sh(project_name, author), progress_callback)
    (project_path / "bin/setup.sh").chmod(0o755)

    write(project_path / "bin/setup.bat", setup_bat(project_name, author), progress_callback)
    write(project_path / "bin/setup.ps1", setup_ps1(project_name, author), progress_callback)

    # __init__.py files for all modules
    init_packages = [
        "src", "src/core", "src/clients", "src/services", "src/helpers", "tester"
    ]
    
    if include_ai:
        init_packages.append("src/ai")
    
    if project_type == ProjectType.WEB_API:
        init_packages.extend(["src/api", "src/routers", "src/database"])
    
    if project_type == ProjectType.DATA_SCIENCE:
        init_packages.extend(["src/features", "src/visualization"])

    for pkg in init_packages:
        write(project_path / pkg / "__init__.py", 
              banner(Path(pkg) / "__init__.py", author, "__init__.py", project_name), 
              progress_callback)

    # main.py
    main_py = project_path / "src/main.py"
    write(main_py, main_py_content(project_name, author, project_type), progress_callback)

    # run.py - alternative entry point
    run_py = project_path / "run.py"
    write(run_py,
         banner(run_py, author, "run.py", project_name) + "\n\n" +
         textwrap.dedent("""
            import subprocess
            import sys
            from pathlib import Path

            if __name__ == "__main__":
                # Run the main module
                subprocess.run([sys.executable, "-m", "src.main"] + sys.argv[1:])
         """).lstrip(),
         progress_callback)

    # Create test files
    create_test_files(project_path, author, project_name, project_type, progress_callback)
    
    # Create example datasets README
    datasets_readme = project_path / "datasets" / "README.md"
    datasets_content = textwrap.dedent(f"""
        # Datasets

        This folder contains datasets for the {project_name} project.

        ## Structure
        ```
        datasets/
        ├── raw/           # Raw, unprocessed data
        ├── processed/     # Cleaned and processed data
        ├── external/      # External datasets
        └── interim/       # Intermediate data transformations
        ```

        ## Usage
        - Place raw data files in `raw/`
        - Store processed data in `processed/`
        - Keep external datasets in `external/`
        - Use `interim/` for temporary processing steps

        ## Data Formats
        Supported formats: CSV, JSON, Parquet, HDF5, Excel

        ## Example
        ```python
        import pandas as pd
        
        # Load raw data
        df = pd.read_csv('datasets/raw/data.csv')
        
        # Process data
        processed_df = df.dropna()
        
        # Save processed data
        processed_df.to_parquet('datasets/processed/clean_data.parquet')
        ```
    """).lstrip()
    write(datasets_readme, datasets_content, progress_callback)

    if progress_callback:
        progress_callback(f"✅ Project '{project_name}' created successfully!")
    
    return True