@echo off
echo Building Windows-compatible Docker containers for QT.AI Trading Bot

REM Check if Docker Desktop is installed and running
docker info > nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not running or not installed.
    echo Please install Docker Desktop for Windows and enable Windows containers.
    echo Visit: https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)

REM Switch to Windows containers if not already
docker info | findstr "windows" > nul
if %errorlevel% neq 0 (
    echo Switching to Windows containers...
    echo This may take a moment...
    echo If prompted by Docker Desktop, please allow the switch to Windows containers.
    pause
    exit /b 1
)

REM Build and start the containers
echo Building and starting containers...
docker-compose -f docker-compose.windows.yml up -d

if %errorlevel% equ 0 (
    echo.
    echo QT.AI Trading Bot is now running!
    echo.
    echo Frontend: http://localhost
    echo Backend API: http://localhost:8000
    echo.
    echo To stop the containers, run: docker-compose -f docker-compose.windows.yml down
) else (
    echo.
    echo Failed to build or start containers.
    echo Please check the error messages above.
)

pause
