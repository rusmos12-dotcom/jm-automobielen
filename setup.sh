#!/bin/bash
# JM Automobielen - One-click GitHub setup
# Run this in Terminal: cd ~/Desktop/jm\ automobielen && bash setup.sh

set -e

echo "🚗 JM Automobielen - GitHub Setup"
echo "=================================="

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "Installing GitHub CLI..."
    brew install gh
fi

# Check if logged in
if ! gh auth status &> /dev/null; then
    echo "Please log in to GitHub:"
    gh auth login
fi

# Initialize git repo
echo "Initializing Git repository..."
git init
git add -A
git commit -m "Initial commit: JM Automobielen automated website"

# Create GitHub repo (public, so GitHub Pages works for free)
echo "Creating GitHub repository..."
gh repo create jm-automobielen --public --source=. --push

# Enable GitHub Pages
echo "Enabling GitHub Pages..."
gh api repos/$(gh api user --jq .login)/jm-automobielen/pages \
  --method POST \
  --field source='{"branch":"main","path":"/"}' 2>/dev/null || echo "Pages may already be enabled"

echo ""
echo "✅ Done! Your site will be live in ~1 minute at:"
echo "   https://$(gh api user --jq .login).github.io/jm-automobielen/"
echo ""
echo "The scraper will run automatically every hour via GitHub Actions."
echo "You can also trigger it manually: Actions → Sync Instagram → Run workflow"
