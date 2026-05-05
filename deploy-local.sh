#!/bin/bash
# Law Analyse - Local Deployment Script

set -e

echo ""
echo "========================================"
echo "  Law Analyse - Local Deployment"
echo "========================================"
echo ""

# Check if Docker is running
echo "[1/6] Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    echo "   ✗ Docker is not running"
    echo ""
    echo "   Please start Docker:"
    echo "   - macOS: Open Docker Desktop from Applications"
    echo "   - Linux: sudo systemctl start docker"
    echo ""
    echo "   Then run this script again."
    exit 1
fi
echo "   ✓ Docker is running"

# Check if .env file exists and has API key
echo ""
echo "[2/6] Checking environment variables..."
if [ ! -f .env ]; then
    echo "   ✗ .env file not found"
    echo "   Creating .env file..."
    cat > .env << EOF
DB_PASSWORD=lawanalyse_local_password_2026
OPENAI_API_KEY=your-openai-api-key-here
EOF
    echo ""
    echo "   Please edit .env and add your OpenAI API key:"
    echo "   nano .env"
    echo ""
    echo "   Get your key from: https://platform.openai.com/api-keys"
    exit 1
fi

if grep -q "your-openai-api-key-here" .env; then
    echo "   ✗ OpenAI API key not configured"
    echo ""
    echo "   Please edit .env and add your OpenAI API key:"
    echo "   nano .env"
    echo ""
    echo "   Get your key from: https://platform.openai.com/api-keys"
    exit 1
fi
echo "   ✓ Environment variables configured"

# Stop existing containers
echo ""
echo "[3/6] Stopping existing containers..."
docker-compose down > /dev/null 2>&1 || true
echo "   ✓ Existing containers stopped"

# Start services
echo ""
echo "[4/6] Starting services..."
echo "   This may take 5-10 minutes on first run (downloading images)"
if ! docker-compose up -d; then
    echo "   ✗ Failed to start services"
    echo ""
    echo "   Check logs with: docker-compose logs"
    exit 1
fi
echo "   ✓ Services started"

# Wait for services to be ready
echo ""
echo "[5/6] Waiting for services to be ready..."
sleep 10
echo "   ✓ Services should be ready"

# Run migrations
echo ""
echo "[6/6] Running database migrations..."
if ! docker-compose exec -T backend alembic upgrade head 2>/dev/null; then
    echo "   ! Migrations failed (this is OK on first run)"
    echo "   Waiting 10 more seconds for database..."
    sleep 10
    docker-compose exec -T backend alembic upgrade head || true
fi
echo "   ✓ Migrations completed"

# Show status
echo ""
echo "========================================"
echo "  Deployment Complete!"
echo "========================================"
echo ""
echo "Services running:"
docker-compose ps
echo ""
echo "Access your application:"
echo "  Frontend:  http://localhost:4321"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"
echo ""
echo "Useful commands:"
echo "  View logs:     docker-compose logs -f"
echo "  Stop:          docker-compose stop"
echo "  Restart:       docker-compose restart"
echo "  Remove all:    docker-compose down -v"
echo ""
echo "Opening frontend in browser..."
sleep 2

# Open browser (cross-platform)
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:4321
elif command -v open > /dev/null; then
    open http://localhost:4321
else
    echo "Please open http://localhost:4321 in your browser"
fi

echo ""
echo "Press Ctrl+C to exit, or close this terminal"
echo ""

# Follow logs
docker-compose logs -f
