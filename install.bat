@echo off
setlocal enabledelayedexpansion

echo.
echo [96m  Installing Webby...[0m
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [91m  Error: Python is not installed or not in PATH[0m
    echo.
    echo   Please install Python from https://python.org
    echo   Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

:: Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"

:: Create Webby directory in user's local app data
set "INSTALL_DIR=%LOCALAPPDATA%\Webby"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Copy the Python script
copy /y "%SCRIPT_DIR%webby.py" "%INSTALL_DIR%\webby.py" >nul

:: Create a batch wrapper for easy command-line access
(
echo @echo off
echo python "%INSTALL_DIR%\webby.py" %%*
) > "%INSTALL_DIR%\webby.bat"

:: Add to user PATH if not already there
set "PATH_CHECK=0"
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USER_PATH=%%b"

echo !USER_PATH! | find /i "%INSTALL_DIR%" >nul
if errorlevel 1 (
    :: Add to PATH
    if defined USER_PATH (
        setx PATH "%USER_PATH%;%INSTALL_DIR%" >nul 2>&1
    ) else (
        setx PATH "%INSTALL_DIR%" >nul 2>&1
    )
    echo [92m  ✓[0m  Added Webby to your PATH
    echo.
    echo [93m  Note: You may need to restart your terminal for PATH changes[0m
) else (
    echo [92m  ✓[0m  Webby is already in your PATH
)

echo.
echo [92m  ✓[0m  Installed to %INSTALL_DIR%
echo.
echo   Run '[96mwebby[0m' from Command Prompt or PowerShell!
echo.
pause

