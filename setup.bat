@echo off
setlocal enabledelayedexpansion

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python...
    
    winget --version >nul 2>&1
    if !errorlevel! equ 0 (
        echo Installing Python using winget...
        winget install Python.Python.3.12 -e --silent
        goto :python_installed
    )
    
    echo Downloading Python installer...
    powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe', 'python_installer.exe')"
    
    echo Installing Python...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    del python_installer.exe
    
    :python_installed
    for /f "delims=" %%i in ('where python') do set "PYTHON_PATH=%%~dpi"
    set "PATH=%PYTHON_PATH%;%PYTHON_PATH%Scripts;%PATH%"
)

pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip is not working properly. Attempting to fix...
    python -m ensurepip --default-pip
    python -m pip install --upgrade pip
)

echo Installing project requirements...
pip install -r requirements.txt

echo Setup completed successfully!
pause