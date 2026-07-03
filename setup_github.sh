#!/bin/bash
# GitHub Setup Script for Binance Trading Bot
# Run this script to initialize git and push to GitHub

echo "🚀 Setting up GitHub repository for Binance Trading Bot..."
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Initialize git repository
echo "📁 Initializing Git repository..."
git init

# Add all files
echo "📝 Adding files to Git..."
git add .

# Create .gitignore if not exists
if [ ! -f .gitignore ]; then
    echo "Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# Environment variables
.env
*.env
!.env.example

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Distribution / packaging
dist/
build/
*.egg-info/
.eggs/

# Testing
.pytest_cache/
htmlcov/
.coverage

# Binance
*.pem
credentials.json
EOF
fi

# Initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Binance Futures Testnet Trading Bot

- Complete trading bot implementation
- Market & Limit order support
- BUY/SELL functionality
- Enhanced CLI with interactive mode
- Comprehensive logging
- Input validation
- Error handling
- Documentation
- GitHub Pages site"

# Ask for GitHub username
echo ""
read -p "Enter your GitHub username: " github_username

# Ask for repository name
echo ""
read -p "Enter repository name (default: binance-trading-bot): " repo_name
repo_name=${repo_name:-binance-trading-bot}

# Add remote
echo ""
echo "🔗 Adding GitHub remote..."
git remote add origin "https://github.com/$github_username/$repo_name.git"

# Create branch main
echo "🌿 Creating main branch..."
git branch -M main

# Push to GitHub
echo ""
echo "⬆️  Pushing to GitHub..."
echo "Note: You may need to authenticate with GitHub"
git push -u origin main

echo ""
echo "✅ Done! Your repository is now on GitHub"
echo "🔗 Visit: https://github.com/$github_username/$repo_name"
echo ""
echo "📋 Next steps:"
echo "1. Go to your repository on GitHub"
echo "2. Go to Settings > Pages"
echo "3. Select 'main' branch and '/docs' folder"
echo "4. Save - your website will be live at:"
echo "   https://$github_username.github.io/$repo_name/"
echo ""
echo "🎉 Happy Trading! (On testnet, of course!)"