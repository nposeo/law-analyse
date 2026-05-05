#!/bin/bash
# Setup script for Law Analyse MVP

set -e

echo "🚀 Law Analyse MVP - Setup Script"
echo "=================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"

if ! python -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "❌ Error: Python 3.11+ required"
    exit 1
fi

# Check Node.js version
echo ""
echo "📋 Checking Node.js version..."
node_version=$(node --version 2>&1)
echo "   Node.js version: $node_version"

# Setup Backend
echo ""
echo "🔧 Setting up Backend..."
cd backend

if [ ! -d ".venv" ]; then
    echo "   Creating virtual environment..."
    python -m venv .venv
fi

echo "   Activating virtual environment..."
source .venv/bin/activate || .venv\\Scripts\\activate

echo "   Installing Python dependencies..."
pip install -q -r requirements.txt

if [ ! -f ".env" ]; then
    echo "   Creating .env file..."
    cp .env.example .env
    echo "   ⚠️  Please edit backend/.env with your DATABASE_URL and OPENAI_API_KEY"
fi

cd ..

# Setup Frontend
echo ""
echo "🔧 Setting up Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "   Installing Node.js dependencies..."
    npm install
fi

if [ ! -f ".env" ]; then
    echo "   Creating .env file..."
    echo "PUBLIC_API_URL=http://localhost:8000" > .env
fi

cd ..

# Check Docker
echo ""
echo "📋 Checking Docker..."
if command -v docker &> /dev/null; then
    echo "   ✅ Docker installed"
    echo ""
    echo "   To start PostgreSQL:"
    echo "   docker run --name law-analyse-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=law_analyse -p 5432:5432 -d postgres:15"
else
    echo "   ⚠️  Docker not found. Install Docker or use external PostgreSQL"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your credentials"
echo "2. Start PostgreSQL (Docker or external)"
echo "3. Run migrations: cd backend && alembic upgrade head"
echo "4. Start backend: cd backend && uvicorn app.main:app --reload"
echo "5. Start frontend: cd frontend && npm run dev"
echo ""
echo "See QUICKSTART.md for detailed instructions"
