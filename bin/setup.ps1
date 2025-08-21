# PyScaffold Setup Script for PowerShell
# This script sets up the development environment for PyScaffold

param(
    [switch]$Clean,
    [switch]$Help
)

$ErrorActionPreference = "Stop"

if ($Help) {
    Write-Host "PyScaffold Setup Script" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage: .\bin\setup.ps1 [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Cyan
    Write-Host "  --clean    Clean setup: remove existing venv, clear pip cache, force reinstall" -ForegroundColor White
    Write-Host "  --help     Show this help message" -ForegroundColor White
    Write-Host ""
    exit 0
}

if ($Clean) {
    Write-Host "🧹 Clean setup mode enabled" -ForegroundColor Yellow
    Write-Host "Setting up PyScaffold development environment (CLEAN MODE)..." -ForegroundColor Green
} else {
    Write-Host "Setting up PyScaffold development environment..." -ForegroundColor Green
}
Write-Host ""

try {
    # Check if Python is installed
    Write-Host "Checking Python version..." -ForegroundColor Yellow
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python is not installed or not in PATH. Please install Python 3.8 or higher." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    Write-Host "$pythonVersion found" -ForegroundColor Green
    Write-Host ""
    
    # Handle clean setup - remove existing venv and clear cache
    if ($Clean) {
        Write-Host "🧹 Cleaning up existing environment..." -ForegroundColor Yellow
        if (Test-Path "venv") {
            Write-Host "Removing existing virtual environment..."
            Remove-Item -Recurse -Force "venv"
            Write-Host "Existing virtual environment removed" -ForegroundColor Green
        }
        
        Write-Host "Clearing pip cache..."
        python -m pip cache purge 2>$null
        Write-Host "Pip cache cleared" -ForegroundColor Green
        Write-Host ""
    }
    
    # Create virtual environment
    Write-Host "Setting up virtual environment..." -ForegroundColor Yellow
    if (-not (Test-Path "venv")) {
        Write-Host "Creating virtual environment..."
        python -m venv venv
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create virtual environment"
        }
        Write-Host "Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "Virtual environment already exists" -ForegroundColor Green
    }
    Write-Host ""
    
    # Activate virtual environment
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to activate virtual environment"
    }
    Write-Host "Virtual environment activated" -ForegroundColor Green
    Write-Host ""
    
    # Upgrade pip
    Write-Host "Upgrading pip..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Pip upgraded" -ForegroundColor Green
    } else {
        Write-Host "Failed to upgrade pip, continuing..." -ForegroundColor Yellow
    }
    Write-Host ""
    
    # Install dependencies
    $installFlags = ""
    if ($Clean) {
        $installFlags = "--force-reinstall --no-cache-dir"
        Write-Host "Installing dependencies (clean mode: force reinstall, no cache)..." -ForegroundColor Yellow
    } else {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
    }
    
    if (Test-Path "requirements.txt") {
        $command = "pip install -r requirements.txt $installFlags".Trim()
        Invoke-Expression $command
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install dependencies"
        }
        Write-Host "Dependencies installed from requirements.txt" -ForegroundColor Green
    } else {
        Write-Host "requirements.txt not found, installing basic dependencies..." -ForegroundColor Yellow
        $command = "pip install textual rich pyyaml $installFlags".Trim()
        Invoke-Expression $command
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install basic dependencies"
        }
    }
    Write-Host ""
    
    # Install development dependencies if available
    if (Test-Path "requirements-dev.txt") {
        Write-Host "Installing development dependencies..." -ForegroundColor Yellow
        pip install -r requirements-dev.txt
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Development dependencies installed" -ForegroundColor Green
        } else {
            Write-Host "Failed to install development dependencies, continuing..." -ForegroundColor Yellow
        }
        Write-Host ""
    }
    
    # Create necessary directories
    Write-Host "Creating necessary directories..." -ForegroundColor Yellow
    @("logs", "outputs", "caches") | ForEach-Object {
        if (-not (Test-Path $_)) {
            New-Item -ItemType Directory -Path $_ -Force | Out-Null
        }
    }
    Write-Host "Directories created" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Setup completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To get started:" -ForegroundColor Cyan
    Write-Host "  1. Activate the virtual environment: .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  2. Run PyScaffold: python run.py" -ForegroundColor White
    Write-Host "  3. Or use CLI mode: python run.py --cli" -ForegroundColor White

    Write-Host ""
    Write-Host "Happy coding!" -ForegroundColor Magenta
    
} catch {
    Write-Host "Setup failed: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Read-Host "Press Enter to exit"