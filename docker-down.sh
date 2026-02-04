#!/bin/bash
# Docker shutdown script for Image Gallery

echo "Stopping Image Gallery Docker services..."
echo ""

docker-compose stop

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Services stopped successfully"
    echo ""
    echo "To remove containers and volumes:"
    echo "  docker-compose down -v"
    echo ""
    echo "To restart services:"
    echo "  ./docker-up.sh"
else
    echo ""
    echo "❌ Failed to stop services"
    exit 1
fi
