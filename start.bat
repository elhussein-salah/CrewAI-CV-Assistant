@echo off
echo CrewAI CV Assistant - Startup Script
echo =====================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if requirements.txt is newer than last install
if not exist ".install_marker" (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo. > .install_marker
) else (
    for %%i in (requirements.txt) do set req_time=%%~ti
    for %%i in (.install_marker) do set marker_time=%%~ti
    REM Simple check - you might want to improve this
    echo Dependencies already installed. Use 'pip install -r requirements.txt' to update.
)

REM Check Ollama status
echo Checking Ollama status...
curl -s http://localhost:11434/api/version >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: Ollama is not running or not installed
    echo Please start Ollama or install it from https://ollama.ai/
    echo.
    echo Continuing anyway - you can start Ollama later...
    timeout /t 3 >nul
)

REM Start the application
echo Starting CrewAI CV Assistant...
echo Open your browser and go to: http://localhost:8501
echo Press Ctrl+C to stop the application
echo.

streamlit run app.py

REM Deactivate virtual environment
deactivate

echo Application stopped.
pause
