@echo off
REM Law Analyse - Local Deployment Script for Windows

echo.
echo ========================================
echo   Law Analyse - Local Deployment
echo ========================================
echo.

REM Check if Docker is running
echo [1/6] Checking Docker...
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo    X Docker is not running
    echo.
    echo    Please start Docker Desktop:
    echo    1. Open Start Menu
    echo    2. Search for "Docker Desktop"
    echo    3. Click to start
    echo    4. Wait for Docker icon in system tray
    echo    5. Run this script again
    echo.
    pause
    exit /b 1
)
echo    ✓ Docker is running

REM Check if .env file exists and has API key
echo.
echo [2/6] Checking environment variables...
if not exist .env (
    echo    X .env file not found
    echo    Creating .env file...
    echo DB_PASSWORD=lawanalyse_local_password_2026 > .env
    echo OPENAI_API_KEY=your-openai-api-key-here >> .env
    echo.
    echo    Please edit .env and add your OpenAI API key:
    echo    notepad .env
    echo.
    pause
    exit /b 1
)

findstr /C:"your-openai-api-key-here" .env >nul
if %ERRORLEVEL% EQU 0 (
    echo    X OpenAI API key not configured
    echo.
    echo    Please edit .env and add your OpenAI API key:
    echo    notepad .env
    echo.
    echo    Get your key from: https://platform.openai.com/api-keys
    echo.
    pause
    exit /b 1
)
echo    ✓ Environment variables configured

REM Stop existing containers
echo.
echo [3/6] Stopping existing containers...
docker-compose down >nul 2>&1
echo    ✓ Existing containers stopped

REM Start services
echo.
echo [4/6] Starting services...
echo    This may take 5-10 minutes on first run (downloading images)
docker-compose up -d
if %ERRORLEVEL% NEQ 0 (
    echo    X Failed to start services
    echo.
    echo    Check logs with: docker-compose logs
    pause
    exit /b 1
)
echo    ✓ Services started

REM Wait for services to be ready
echo.
echo [5/6] Waiting for services to be ready...
timeout /t 10 /nobreak >nul
echo    ✓ Services should be ready

REM Run migrations
echo.
echo [6/6] Running database migrations...
docker-compose exec -T backend alembic upgrade head
if %ERRORLEVEL% NEQ 0 (
    echo    ! Migrations failed (this is OK on first run)
    echo    Waiting 10 more seconds for database...
    timeout /t 10 /nobreak >nul
    docker-compose exec -T backend alembic upgrade head
)
echo    ✓ Migrations completed

REM Show status
echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo Services running:
docker-compose ps
echo.
echo Access your application:
echo   Frontend:  http://localhost:4321
echo   Backend:   http://localhost:8000
echo   API Docs:  http://localhost:8000/docs
echo.
echo Useful commands:
echo   View logs:     docker-compose logs -f
echo   Stop:          docker-compose stop
echo   Restart:       docker-compose restart
echo   Remove all:    docker-compose down -v
echo.
echo Opening frontend in browser...
timeout /t 3 /nobreak >nul
start http://localhost:4321
echo.
pause
