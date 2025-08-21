@echo off
REM PyScaffold Setup Script for Windows
REM This script sets up the development environment for PyScaffold

echo 🚀 Setting up PyScaffold development environment...
echo.

REM Check if Python is installed
echo 📋 Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found
echo.

REM Create virtual environment if it doesn't exist
echo 🔧 Setting up virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated
echo.

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ⚠️  Failed to upgrade pip, continuing...
) else (
    echo ✅ Pip upgraded
)
echo.

REM Install dependencies
echo 📚 Installing dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed from requirements.txt
) else (
    echo ⚠️  requirements.txt not found, installing basic dependencies...
    pip install textual rich pyyaml
    if %errorlevel% neq 0 (
        echo ❌ Failed to install basic dependencies
        pause
        exit /b 1
    )
)
echo.

REM Install development dependencies if available
if exist "requirements-dev.txt" (
    echo 🛠️  Installing development dependencies...
    pip install -r requirements-dev.txt
    if %errorlevel% neq 0 (
        echo ⚠️  Failed to install development dependencies, continuing...
    ) else (
        echo ✅ Development dependencies installed
    )
    echo.
)

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist "logs" mkdir logs
if not exist "outputs" mkdir outputs
if not exist "caches" mkdir caches
echo ✅ Directories created
echo.

echo 🎉 Setup completed successfully!
echo.
echo To get started:
echo   1. Activate the virtual environment: venv\Scripts\activate.bat
echo   2. Run PyScaffold: python run.py
echo   3. Or use CLI mode: python run.py --cli

echo.
echo Happy coding! 🐍✨
echo.
pause