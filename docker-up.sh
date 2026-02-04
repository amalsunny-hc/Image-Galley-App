#!/bin/bash
# Docker startup script for Image Gallery with MySQL

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Image Gallery - Docker Compose Setup                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Please install Docker from: https://www.docker.com"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    echo "Please install Docker Compose"
    exit 1
fi

echo "✓ Docker and Docker Compose found"
echo ""

# Check if containers are already running
if docker-compose ps | grep -q "Up"; then
    echo "⚠️  Services already running"
    echo ""
    echo "Services Status:"
    docker-compose ps
    echo ""
    echo "Access the application:"
    echo "  📱 Gallery: http://localhost:5000"
    echo "  🗄️  phpMyAdmin: http://localhost:8080"
    echo ""
    echo "Run 'docker-compose logs -f' to view logs"
    exit 0
fi

# Build and start services
echo "Building and starting services..."
echo ""

docker-compose up -d

# Wait for MySQL to be healthy
echo "Waiting for MySQL to be ready..."
sleep 10

# Check if services started successfully
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  ✅ Docker services started successfully!                 ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🎉 Services running:"
    docker-compose ps
    echo ""
    echo "📍 Access the application:"
    echo "   📱 Image Gallery: http://localhost:5000"
    echo "   🗄️  phpMyAdmin: http://localhost:8080"
    echo ""
    echo "🔑 Default Credentials:"
    echo "   Username: admin"
    echo "   Password: admin123"
    echo ""
    echo "📊 Services:"
    echo "   • Flask Application (Port 5000)"
    echo "   • MySQL Database (Port 3306)"
    echo "   • phpMyAdmin (Port 8080)"
    echo ""
    echo "💡 Useful Commands:"
    echo "   View logs:     docker-compose logs -f"
    echo "   Stop services: docker-compose stop"
    echo "   Restart:       docker-compose restart"
    echo "   Remove all:    docker-compose down -v"
    echo ""
else
    echo ""
    echo "❌ Failed to start services"
    echo "Check logs: docker-compose logs"
    exit 1
fi
