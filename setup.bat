@echo off
setlocal enabledelayedexpansion

echo Checking Python installation...
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
)

:python_installed
echo Refreshing environment variables...
for /f "delims=" %%i in ('where python') do set "PYTHON_PATH=%%~dpi"
set "PATH=%PYTHON_PATH%;%PYTHON_PATH%Scripts;%PATH%"

echo Checking pip installation...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip is not working properly. Installing pip...
    python -m ensurepip --default-pip
    python -m pip install --upgrade pip
)

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing project requirements...
python -m pip install --upgrade pip

echo Installing required packages...
pip install Flask==3.1.0
pip install pandas==2.2.3
pip install pdf2docx==0.5.8
pip install pywin32==307

echo Verifying installations...
python -c "import flask; import pandas; import pdf2docx; import win32com.client" >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Some packages failed to install correctly.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo Setup completed successfully!
pause