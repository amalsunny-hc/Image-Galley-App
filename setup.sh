#!/bin/bash
# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo ""
echo "Initializing database..."
python init_db.py

echo ""
echo "Setup complete! To start the application, run:"
echo "  python run.py"
echo ""
echo "Then open http://localhost:5000 in your browser"
