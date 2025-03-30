@echo off
cd /d "%~dp0"
echo Starting Converter application...
for /F "tokens=*" %%A in ('type .env ^| findstr /v "^#" ^| findstr /v "^$"') do (
    set %%A
)
set ANACONDA_PYTHON=%ANACONDA_PATH%\python.exe
if exist "%ANACONDA_PYTHON%" (
    echo Using Anaconda Python...
    "%ANACONDA_PYTHON%" %PYTHON_SCRIPT%
) else (
    echo Anaconda Python not found, using system Python...
    python main.py
)

if %ERRORLEVEL% neq 0 (
    echo An error occurred while running the script.
    pause
) else (
    echo Converter completed successfully.
)
pause