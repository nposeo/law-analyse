#!/bin/bash
# Development server startup script

set -e

echo "🚀 Starting Law Analyse Development Servers"
echo "==========================================="
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "❌ Error: backend/.env not found"
    echo "   Run ./setup.sh first"
    exit 1
fi

# Start Backend
echo "🔧 Starting Backend (FastAPI)..."
cd backend
source .venv/bin/activate || .venv\\Scripts\\activate
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

echo "   Backend PID: $BACKEND_PID"
echo "   Backend URL: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"

# Wait for backend to start
sleep 3

# Start Frontend
echo ""
echo "🎨 Starting Frontend (Astro)..."
cd frontend
npm run dev -- --port 4321 &
FRONTEND_PID=$!
cd ..

echo "   Frontend PID: $FRONTEND_PID"
echo "   Frontend URL: http://localhost:4321"

echo ""
echo "✅ Both servers running!"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID
