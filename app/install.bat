@echo off
echo ====================================
echo Satisfactory Production Calculator
echo Installation Script
echo ====================================
echo.

echo Step 1: Activating virtual environment...
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat

echo Step 2: Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Step 3: Checking Graphviz installation...
where dot >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Graphviz is installed
) else (
    echo [WARNING] Graphviz is NOT installed
    echo Please install Graphviz from: https://graphviz.org/download/
    echo Or use: choco install graphviz
)

echo.
echo ====================================
echo Installation complete!
echo ====================================
echo.
echo To start the application, run:
echo   streamlit run streamlit_app.py
echo.
pause
