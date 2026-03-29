#!/bin/bash
# Local development helper script for JM Automobielen website

set -e

echo "🚗 JM Automobielen - Local Development"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers (this may take a moment)..."
playwright install chromium --with-deps 2>/dev/null || true

echo ""
echo "✅ Setup complete!"
echo ""
echo "Available commands:"
echo ""
echo "1. Run scraper (incremental - only new posts):"
echo "   python scraper/scrape.py"
echo ""
echo "2. Full scrape (all posts):"
echo "   python scraper/scrape.py --full"
echo ""
echo "3. Start local web server:"
echo "   python -m http.server 8000"
echo "   Then visit: http://localhost:8000"
echo ""
echo "4. View posts data:"
echo "   cat data/posts.json | python -m json.tool"
echo ""
echo "======================================"
echo ""
