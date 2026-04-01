@echo off
REM NeuroPath AI Backend - Quick Start Script for Windows

echo 🚀 NeuroPath AI - Backend Setup
echo ==================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 is not installed or not in PATH
    pause
    exit /b 1
)

echo ✓ Python 3 found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Run the server
echo.
echo ✨ Starting FastAPI server...
echo 🌐 API will be available at: http://localhost:8000
echo 📚 Documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
