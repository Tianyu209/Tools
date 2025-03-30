@echo off
echo Starting Converter application...
python main.py
if %ERRORLEVEL% neq 0 (
    echo An error occurred while running the script.
    pause
) else (
    echo Converter completed successfully.
)
pause