#!/bin/bash
# Image Gallery - Quick Launch Script
# This script starts the Flask development server

echo "=================================="
echo "  Image Gallery Application"
echo "  Starting Development Server..."
echo "=================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found"
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Check if dependencies are installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if database exists
if [ ! -f "image_gallery.db" ]; then
    echo "Database not found, initializing..."
    python3 init_db.py
fi

echo ""
echo "=================================="
echo "✓ All checks passed!"
echo "=================================="
echo ""
echo "Starting Flask server..."
echo ""
echo "📱 Access the application at:"
echo "   http://localhost:5000"
echo ""
echo "🔑 Default Login:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "⚠️  Change the password after first login!"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python3 run.py
