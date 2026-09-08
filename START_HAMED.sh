#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print header
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}║              🤖 Hamed AI Dashboard                        ║${NC}"
echo -e "${GREEN}║         Multi-Agent Business Operating System             ║${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed!${NC}"
    echo ""
    echo "Please install Node.js first:"
    echo "https://nodejs.org/"
    echo ""
    echo "Or use a package manager:"
    echo "  macOS: brew install node"
    echo "  Ubuntu/Debian: sudo apt install nodejs npm"
    echo "  Fedora: sudo dnf install nodejs npm"
    echo ""
    exit 1
fi

# Check Node version
echo -e "${GREEN}✓ Node.js found${NC}"
node --version
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}📦 Installing dependencies...${NC}"
    echo ""
    npm install
    if [ $? -ne 0 ]; then
        echo ""
        echo -e "${RED}❌ Failed to install dependencies${NC}"
        exit 1
    fi
    echo ""
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
    echo ""
fi

# Start the development server
echo -e "${YELLOW}🚀 Starting Hamed AI Dashboard...${NC}"
echo ""
echo "The dashboard will open automatically in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

# Open browser after 3 seconds (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    (sleep 3 && open http://localhost:5173) &
# Open browser after 3 seconds (Linux)
elif [[ "$OSTYPE" == "linux"* ]]; then
    (sleep 3 && xdg-open http://localhost:5173) &
fi

# Start the dev server
npm run dev
