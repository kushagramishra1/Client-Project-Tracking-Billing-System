@echo off
echo Starting Client Project Tracking & Billing System...
echo.

REM Try to find Python
where python >nul 2>&1
if %errorlevel% == 0 (
    echo Found Python in PATH
    python start.py
    goto :end
)

where python3 >nul 2>&1
if %errorlevel% == 0 (
    echo Found Python3 in PATH
    python3 start.py
    goto :end
)

where py >nul 2>&1
if %errorlevel% == 0 (
    echo Found py launcher
    py start.py
    goto :end
)

REM Try virtual environment
if exist "venv\Scripts\python.exe" (
    echo Using virtual environment
    venv\Scripts\python.exe start.py
    goto :end
)

echo.
echo ERROR: Python not found!
echo.
echo Please install Python 3.7 or higher from:
echo https://www.python.org/downloads/
echo.
echo Or activate your virtual environment and run:
echo venv\Scripts\python.exe start.py
echo.
pause

:end
