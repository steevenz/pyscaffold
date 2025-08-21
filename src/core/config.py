#!/usr/bin/env python3
# src/core/config.py
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
src/core/config.py
Configuration management for PyScaffold
"""

from __future__ import annotations

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)

@dataclass
class AuthorConfig:
    """Author configuration."""
    name: str = ""
    email: str = ""

@dataclass
class DefaultsConfig:
    """Default project settings."""
    project_type: str = "general"
    license: str = "MIT"
    include_ai: bool = False
    include_trainer: bool = False
    use_boilerplate: bool = False

@dataclass
class StructureConfig:
    """Project structure configuration."""
    base_folders: list[str] = field(default_factory=list)
    conditional_folders: Dict[str, list[str]] = field(default_factory=dict)

@dataclass
class TemplatesConfig:
    """File templates configuration."""
    base_files: list[str] = field(default_factory=list)
    setup_scripts: list[str] = field(default_factory=list)

@dataclass
class UIConfig:
    """UI configuration."""
    default_mode: str = "cli"
    cli: Dict[str, bool] = field(default_factory=dict)

@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: str = "logs/pyscaffold.log"

@dataclass
class BoilerplateConfig:
    """Boilerplate configuration."""
    templates_dir: str = "templates"
    available: list[str] = field(default_factory=list)

@dataclass
class GitConfig:
    """Git configuration."""
    auto_init: bool = True
    ignore_patterns: list[str] = field(default_factory=list)

@dataclass
class DockerConfig:
    """Docker configuration."""
    python_version: str = "3.11"
    base_image: str = "python:3.11-slim"
    workdir: str = "/app"
    port: int = 8000

@dataclass
class TestingConfig:
    """Testing configuration."""
    framework: str = "pytest"
    structure: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)

@dataclass
class PyScaffoldConfig:
    """Main PyScaffold configuration."""
    defaults: DefaultsConfig = field(default_factory=DefaultsConfig)
    author: AuthorConfig = field(default_factory=AuthorConfig)
    structure: StructureConfig = field(default_factory=StructureConfig)
    templates: TemplatesConfig = field(default_factory=TemplatesConfig)
    dependencies: Dict[str, list[str]] = field(default_factory=dict)
    ui: UIConfig = field(default_factory=UIConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    boilerplate: BoilerplateConfig = field(default_factory=BoilerplateConfig)
    git: GitConfig = field(default_factory=GitConfig)
    docker: DockerConfig = field(default_factory=DockerConfig)
    testing: TestingConfig = field(default_factory=TestingConfig)

class ConfigManager:
    """Configuration manager for PyScaffold."""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or self._get_default_config_path()
        self._config: Optional[PyScaffoldConfig] = None
    
    def _get_default_config_path(self) -> Path:
        """Get default configuration file path."""
        # Try to find config relative to this file
        current_dir = Path(__file__).parent.parent.parent
        config_file = current_dir / "config" / "config.yml"
        
        if config_file.exists():
            return config_file
        
        # Fallback to current working directory
        fallback_config = Path.cwd() / "config" / "config.yml"
        return fallback_config
    
    def load_config(self) -> PyScaffoldConfig:
        """Load configuration from YAML file."""
        if self._config is not None:
            return self._config
        
        if not self.config_path.exists():
            logger.warning(f"Config file not found: {self.config_path}. Using defaults.")
            self._config = PyScaffoldConfig()
            return self._config
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            self._config = self._parse_config(config_data)
            logger.info(f"Configuration loaded from: {self.config_path}")
            return self._config
            
        except Exception as e:
            logger.error(f"Error loading config file {self.config_path}: {e}")
            logger.info("Using default configuration")
            self._config = PyScaffoldConfig()
            return self._config
    
    def _parse_config(self, config_data: Dict[str, Any]) -> PyScaffoldConfig:
        """Parse configuration data into PyScaffoldConfig object."""
        config = PyScaffoldConfig()
        
        # Parse defaults
        if 'defaults' in config_data:
            defaults_data = config_data['defaults']
            config.defaults = DefaultsConfig(
                project_type=defaults_data.get('project_type', 'general'),
                license=defaults_data.get('license', 'MIT'),
                include_ai=defaults_data.get('include_ai', False),
                include_trainer=defaults_data.get('include_trainer', False),
                use_boilerplate=defaults_data.get('use_boilerplate', False)
            )
        
        # Parse author
        if 'author' in config_data:
            author_data = config_data['author']
            config.author = AuthorConfig(
                name=author_data.get('name', ''),
                email=author_data.get('email', '')
            )
        
        # Parse structure
        if 'structure' in config_data:
            structure_data = config_data['structure']
            config.structure = StructureConfig(
                base_folders=structure_data.get('base_folders', []),
                conditional_folders=structure_data.get('conditional_folders', {})
            )
        
        # Parse templates
        if 'templates' in config_data:
            templates_data = config_data['templates']
            config.templates = TemplatesConfig(
                base_files=templates_data.get('base_files', []),
                setup_scripts=templates_data.get('setup_scripts', [])
            )
        
        # Parse dependencies
        config.dependencies = config_data.get('dependencies', {})
        
        # Parse UI
        if 'ui' in config_data:
            ui_data = config_data['ui']
            config.ui = UIConfig(
                default_mode=ui_data.get('default_mode', 'cli'),
                cli=ui_data.get('cli', {})
            )
        
        # Parse logging
        if 'logging' in config_data:
            logging_data = config_data['logging']
            config.logging = LoggingConfig(
                level=logging_data.get('level', 'INFO'),
                format=logging_data.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
                file=logging_data.get('file', 'logs/pyscaffold.log')
            )
        
        # Parse boilerplate
        if 'boilerplate' in config_data:
            boilerplate_data = config_data['boilerplate']
            config.boilerplate = BoilerplateConfig(
                templates_dir=boilerplate_data.get('templates_dir', 'templates'),
                available=boilerplate_data.get('available', [])
            )
        
        # Parse git
        if 'git' in config_data:
            git_data = config_data['git']
            config.git = GitConfig(
                auto_init=git_data.get('auto_init', True),
                ignore_patterns=git_data.get('ignore_patterns', [])
            )
        
        # Parse docker
        if 'docker' in config_data:
            docker_data = config_data['docker']
            config.docker = DockerConfig(
                python_version=docker_data.get('python_version', '3.11'),
                base_image=docker_data.get('base_image', 'python:3.11-slim'),
                workdir=docker_data.get('workdir', '/app'),
                port=docker_data.get('port', 8000)
            )
        
        # Parse testing
        if 'testing' in config_data:
            testing_data = config_data['testing']
            config.testing = TestingConfig(
                framework=testing_data.get('framework', 'pytest'),
                structure=testing_data.get('structure', []),
                dependencies=testing_data.get('dependencies', [])
            )
        
        return config
    
    def get_dependencies_for_project_type(self, project_type: str) -> list[str]:
        """Get dependencies for a specific project type."""
        config = self.load_config()
        return config.dependencies.get(project_type, config.dependencies.get('general', []))
    
    def get_folders_for_project_type(self, project_type: str, include_ai: bool = False, include_trainer: bool = False) -> list[str]:
        """Get folders for a specific project type."""
        config = self.load_config()
        folders = config.structure.base_folders.copy()
        
        # Add conditional folders based on project type
        if project_type in config.structure.conditional_folders:
            folders.extend(config.structure.conditional_folders[project_type])
        
        # Add AI folder if requested
        if include_ai and 'ai' in config.structure.conditional_folders:
            folders.extend(config.structure.conditional_folders['ai'])
        
        # Add trainer folder if requested
        if include_trainer and 'trainer' in config.structure.conditional_folders:
            folders.extend(config.structure.conditional_folders['trainer'])
        
        return folders
    
    def save_config(self, config: PyScaffoldConfig) -> None:
        """Save configuration to YAML file."""
        try:
            # Ensure config directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert config to dict
            config_dict = self._config_to_dict(config)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
            
            logger.info(f"Configuration saved to: {self.config_path}")
            
        except Exception as e:
            logger.error(f"Error saving config file {self.config_path}: {e}")
    
    def _config_to_dict(self, config: PyScaffoldConfig) -> Dict[str, Any]:
        """Convert PyScaffoldConfig to dictionary."""
        # This is a simplified conversion - you might want to use a library like dataclasses-json
        # for more robust serialization
        return {
            'defaults': {
                'project_type': config.defaults.project_type,
                'license': config.defaults.license,
                'include_ai': config.defaults.include_ai,
                'include_trainer': config.defaults.include_trainer,
                'use_boilerplate': config.defaults.use_boilerplate
            },
            'author': {
                'name': config.author.name,
                'email': config.author.email
            },
            'structure': {
                'base_folders': config.structure.base_folders,
                'conditional_folders': config.structure.conditional_folders
            },
            'templates': {
                'base_files': config.templates.base_files,
                'setup_scripts': config.templates.setup_scripts
            },
            'dependencies': config.dependencies,
            'ui': {
                'default_mode': config.ui.default_mode,
                'cli': config.ui.cli
            },
            'logging': {
                'level': config.logging.level,
                'format': config.logging.format,
                'file': config.logging.file
            },
            'boilerplate': {
                'templates_dir': config.boilerplate.templates_dir,
                'available': config.boilerplate.available
            },
            'git': {
                'auto_init': config.git.auto_init,
                'ignore_patterns': config.git.ignore_patterns
            },
            'docker': {
                'python_version': config.docker.python_version,
                'base_image': config.docker.base_image,
                'workdir': config.docker.workdir,
                'port': config.docker.port
            },
            'testing': {
                'framework': config.testing.framework,
                'structure': config.testing.structure,
                'dependencies': config.testing.dependencies
            }
        }

# Global config manager instance
_config_manager: Optional[ConfigManager] = None

def get_config_manager() -> ConfigManager:
    """Get global config manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager

def get_config() -> PyScaffoldConfig:
    """Get current configuration."""
    return get_config_manager().load_config()