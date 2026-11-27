@echo off
REM Launch the Daily Technology Intelligence app.
cd /d "%~dp0"

if not exist ".env" (
    echo.
    echo   No .env file found.
    echo   Copy .env.example to .env and add your GROQ_API_KEY and TAVILY_API_KEY.
    echo.
    pause
    exit /b 1
)

python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    python -m pip install -r requirements.txt
)

echo Starting Daily Technology Intelligence...
python -m streamlit run app.py
