#!/bin/bash
# AI Weekly Digest - Setup Script

echo "🤖 AI Weekly Digest - Setup"
echo "============================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi
echo "✅ Python 3 found"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed"
echo ""

# Create necessary directories
echo "Creating directories..."
mkdir -p data
mkdir -p output
mkdir -p logs
echo "✅ Directories created"
echo ""

# Make scripts executable
echo "Making scripts executable..."
chmod +x generate_weekly_digest.py
chmod +x scripts/*.py
chmod +x setup.sh
echo "✅ Scripts are now executable"
echo ""

# Check for API key
echo "Checking for Anthropic API key..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not found in environment"
    echo ""
    echo "Please set your API key:"
    echo "  export ANTHROPIC_API_KEY='your-api-key-here'"
    echo ""
    echo "Or add it to your shell config (~/.zshrc or ~/.bash_profile):"
    echo "  echo 'export ANTHROPIC_API_KEY=\"your-key\"' >> ~/.zshrc"
    echo ""
else
    echo "✅ API key found"
fi
echo ""

# Setup summary
echo "============================"
echo "✅ Setup Complete!"
echo "============================"
echo ""
echo "Next steps:"
echo ""
echo "1. Set your Anthropic API key (if not already set):"
echo "   export ANTHROPIC_API_KEY='your-api-key-here'"
echo ""
echo "2. Test the system:"
echo "   python3 generate_weekly_digest.py"
echo ""
echo "3. Set up Sunday automation:"
echo "   # Edit com.aiweekly.digest.plist and add your API key"
echo "   nano com.aiweekly.digest.plist"
echo ""
echo "   # Copy to LaunchAgents and load"
echo "   cp com.aiweekly.digest.plist ~/Library/LaunchAgents/"
echo "   launchctl load ~/Library/LaunchAgents/com.aiweekly.digest.plist"
echo ""
echo "For more details, see README.md"
echo ""
