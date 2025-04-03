@echo off
REM Script to run multiple instances of the Flask application with different ports

setlocal EnableDelayedExpansion

REM Default ports
set DEV_PORT=5000
set TEST_PORT=5001
set CUSTOM_PORT=5002

REM Parse command line arguments
set DEV_ONLY=
set TEST_ONLY=
set CUSTOM_ONLY=

:parse_args
if "%~1"=="" goto :end_parse_args

if "%~1"=="--dev-port" (
    set DEV_PORT=%~2
    shift
    shift
    goto :parse_args
)

if "%~1"=="--test-port" (
    set TEST_PORT=%~2
    shift
    shift
    goto :parse_args
)

if "%~1"=="--custom-port" (
    set CUSTOM_PORT=%~2
    shift
    shift
    goto :parse_args
)

if "%~1"=="--dev-only" (
    set DEV_ONLY=true
    shift
    goto :parse_args
)

if "%~1"=="--test-only" (
    set TEST_ONLY=true
    shift
    goto :parse_args
)

if "%~1"=="--custom-only" (
    set CUSTOM_ONLY=true
    shift
    goto :parse_args
)

if "%~1"=="--help" (
    echo Usage: %0 [options]
    echo Options:
    echo   --dev-port PORT    Set development instance port (default: 5000)
    echo   --test-port PORT   Set test instance port (default: 5001)
    echo   --custom-port PORT Set custom instance port (default: 5002)
    echo   --dev-only         Start only the development instance
    echo   --test-only        Start only the test instance
    echo   --custom-only      Start only the custom instance
    echo   --help             Show this help message
    exit /b 0
)

echo Unknown option: %~1
echo Use --help for usage information
exit /b 1

:end_parse_args

REM Function to start an instance
:start_instance
set config=%~1
set port=%~2
set name=%~3

echo Starting %name% instance on port %port%...
start cmd /k "set FLASK_APP=run.py && set FLASK_ENV=development && set FLASK_CONFIG=%config% && set FLASK_INSTANCE=%name% && set SERVER_PORT=%port% && python run.py"
echo Instance started. Access at: http://localhost:%port%
echo.
goto :eof

REM Start instances based on flags
if defined DEV_ONLY (
    call :start_instance development !DEV_PORT! dev
) else if defined TEST_ONLY (
    call :start_instance testing !TEST_PORT! test
) else if defined CUSTOM_ONLY (
    call :start_instance development !CUSTOM_PORT! custom
) else (
    REM Start all instances by default
    call :start_instance development !DEV_PORT! dev
    call :start_instance testing !TEST_PORT! test
)

echo All requested instances are running.
echo Press Ctrl+C in the instance windows to terminate them individually.

endlocal
