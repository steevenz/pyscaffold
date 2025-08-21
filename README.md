# 🚀 PyScaffold - Ultimate Python Project Boilerplate Generator

> **Stop the boilerplate madness!** Generate professional Python projects in seconds, not hours.

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-black?style=for-the-badge)](https://github.com/psf/black)

<div align="center">
  <img src="https://media.giphy.com/media/LMt9638dO8dftAjtco/giphy.gif" width="400" alt="Coding Fire">
</div>

## ✨ What's This?

PyScaffold is your ultimate companion for kickstarting Python projects without the repetitive setup hassle. Generate full-featured project structures with:

- 🎯 **Multiple project types** (Data Science, Web API, CLI Tools, Automation)
- 📁 **Smart template system** (bring your own templates)
- ⚡ **Lightning fast setup** (we hate waiting too)
- 🔥 **Professional structure** (because you're not an amateur)
- 🐳 **Docker ready** (containerization included)
- 🧪 **Testing setup** (pytest configured)
- 📝 **Type hints** (mypy compatible)

## 🚀 Quick Start

### Prerequisites

```bash
# Make sure you have Python 3.8+
python --version
```

### Installation

```bash
# Clone the repository
git clone https://github.com/steevenz/pyscaffold.git
cd pyscaffold

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Launch the interactive CLI
python run.py --cli

# Or run directly
python run.py
```

## 🎯 What You Get

### Project Structure (Auto-Generated)

```
my_awesome_project/
├── src/                    # Your source code
│   ├── core/              # Core functionality
│   ├── services/          # Business logic
│   ├── helpers/           # Utility functions
│   ├── clients/           # API clients
│   └── ai/                # AI components (optional)
├── tester/                 # Test cases
├── trainer/                # Training scripts (optional)
├── datasets/               # Data files
├── outputs/                # Results and exports
├── logs/                   # Log files
├── caches/                 # Cache files
├── config/                 # Configuration files
├── bin/                    # Setup scripts
├── docker-compose.yml      # Docker orchestration
├── Dockerfile             # Container definition
├── pyproject.toml         # Project metadata
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
└── run.py                 # Entry point
```

### Built-In Project Types

We've got templates for every need:

- **📊 Standard Python Project** - Clean, professional structure
- **🔬 Data Science Powerhouse** - With pandas, sklearn, notebooks
- **🌐 Web API Beast** - FastAPI, SQLAlchemy, the whole stack
- **⚡ CLI Tool Masterpiece** - Click, Rich, Typer ready
- **🤖 Automation Ninja** - Schedule, requests, BeautifulSoup
- **🎨 Custom Boilerplate** - Use your own templates

## ⚙️ Advanced Features

### Custom Boilerplates

Create your own boilerplates in the `datasets/boilerplates/` directory:

```
datasets/boilerplates/
├── my_custom_boilerplate/
│   ├── src/
│   ├── config/
│   └── boilerplate-config.json
└── data_science_plus/
    ├── notebooks/
    ├── models/
    └── special_setup.py
```

### License Options

Choose your license:

- **MIT** - Open source friendly
- **Apache-2.0** - Enterprise ready
- **GPL-3.0** - Copyleft power
- **BSD-3-Clause** - Flexible
- **Commercial** - Proprietary projects
- **Private** - Internal use

### Auto Setup Scripts

Every project comes with setup scripts:

```bash
# Linux/macOS
./bin/setup.sh

# Windows (PowerShell)
.\bin\setup.ps1

# Windows (Batch)
.\bin\setup.bat
```

These scripts automatically:
- Create virtual environment
- Install dependencies
- Set up development tools
- Configure pre-commit hooks

## 🚀 Production Ready Features

- ✅ **Docker Support** - Full containerization setup
- ✅ **Logging Config** - Professional logging out of the box
- ✅ **Type Hints** - Full mypy compatibility
- ✅ **Testing Setup** - pytest configured and ready
- ✅ **Environment Management** - dotenv support
- ✅ **CI/CD Ready** - Structure optimized for automation
- ✅ **Code Quality** - Black, isort, mypy configured

## 🎨 Customization

### Modify Project Types

Edit the `ProjectType` enum in `src/core/generators.py`:

```python
class ProjectType(Enum):
    STANDARD = "Standard Python Project"
    DATA_SCIENCE = "Data Science Project"
    WEB_API = "Web API Project"
    CLI_TOOL = "CLI Tool"
    AUTOMATION = "Automation Script"
    # Add your own here!
    MY_CUSTOM_TYPE = "My Awesome Project Type"
```

### Configuration

Customize default settings in `config/config.yml`:

```yaml
# Author information
author:
  name: "Your Name"
  email: "your.email@example.com"

# Default project settings
defaults:
  project_type: "STANDARD"
  license: "MIT"
  include_ai: false
  include_trainer: false
```

## 📚 Documentation

### Command Line Options

```bash
# Show version
python run.py --version

# Show configuration info
python run.py --config-info

# Enable debug mode
python run.py --debug

# Set log level
python run.py --log-level DEBUG
```

### Project Structure Explained

- **`src/`** - Main source code directory
- **`tester/`** - Test files and test utilities
- **`trainer/`** - ML training scripts (for data science projects)
- **`datasets/`** - Data files and datasets
- **`outputs/`** - Generated files, reports, models
- **`logs/`** - Application logs
- **`caches/`** - Temporary cache files
- **`config/`** - Configuration files
- **`bin/`** - Executable scripts and utilities

## 🤝 Contributing

Want to make PyScaffold even better? Here's how:

1. **Fork** the repository
2. **Create** your feature branch (`git checkout -b feature/amazing-stuff`)
3. **Commit** your changes (`git commit -m 'Add some amazing stuff'`)
4. **Push** to the branch (`git push origin feature/amazing-stuff`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/pyscaffold.git
cd pyscaffold

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .[dev]

# Run tests
python -m pytest

# Format code
python -m black src tester
python -m isort src tester

# Type checking
python -m mypy src
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Authors

- **Steeve Andrian Salim** - *Initial work* - [steevenz](https://github.com/steevenz)

## 🙏 Acknowledgments

- **[Click](https://click.palletsprojects.com/)** - For command line interfaces
- **[Rich](https://rich.readthedocs.io/)** - For beautiful terminal output
- **[Jinja2](https://jinja.palletsprojects.com/)** - For template rendering
- **[PyYAML](https://pyyaml.org/)** - For configuration management
- **You** - For being awesome enough to use this tool!

## 🔗 Links

- **Repository**: [https://github.com/steevenz/pyscaffold](https://github.com/steevenz/pyscaffold)
- **Issues**: [https://github.com/steevenz/pyscaffold/issues](https://github.com/steevenz/pyscaffold/issues)
- **Documentation**: [https://github.com/steevenz/pyscaffold#readme](https://github.com/steevenz/pyscaffold#readme)

---

<div align="center">
  <p><strong>⭐ Star this repo if it saved your sanity!</strong></p>
  <p>Built with ❤️ and too much coffee ☕</p>
</div>