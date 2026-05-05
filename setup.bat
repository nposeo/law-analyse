@echo off
REM Setup script for Law Analyse MVP (Windows)

echo.
echo Law Analyse MVP - Setup Script
echo ==================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found
    exit /b 1
)

REM Check Node.js version
echo.
echo Checking Node.js version...
node --version
if %ERRORLEVEL% NEQ 0 (
    echo Error: Node.js not found
    exit /b 1
)

REM Setup Backend
echo.
echo Setting up Backend...
cd backend

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -q -r requirements.txt

if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo Please edit backend\.env with your DATABASE_URL and OPENAI_API_KEY
)

cd ..

REM Setup Frontend
echo.
echo Setting up Frontend...
cd frontend

if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call npm install
)

if not exist ".env" (
    echo Creating .env file...
    echo PUBLIC_API_URL=http://localhost:8000 > .env
)

cd ..

REM Check Docker
echo.
echo Checking Docker...
docker --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Docker installed
    echo.
    echo To start PostgreSQL:
    echo docker run --name law-analyse-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=law_analyse -p 5432:5432 -d postgres:15
) else (
    echo Docker not found. Install Docker or use external PostgreSQL
)

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit backend\.env with your credentials
echo 2. Start PostgreSQL (Docker or external)
echo 3. Run migrations: cd backend ^&^& alembic upgrade head
echo 4. Start backend: cd backend ^&^& uvicorn app.main:app --reload
echo 5. Start frontend: cd frontend ^&^& npm run dev
echo.
echo See QUICKSTART.md for detailed instructions

pause
