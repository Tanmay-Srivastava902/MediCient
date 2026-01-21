#!/bin/bash
# Quick setup script for Medicient demo

echo "========================================"
echo "  MEDICIENT QUICK SETUP"
echo "========================================"
echo ""

# Check if MySQL is running
echo "Checking MySQL..."
if systemctl is-active --quiet mysql; then
    echo "✅ MySQL is running"
else
    echo "⚠️  MySQL is not running"
    echo "Starting MySQL..."
    sudo systemctl start mysql
fi

echo ""
echo "Making demo executable..."
chmod +x demo_simple.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the demo:"
echo "  python3 demo_simple.py"
echo ""
