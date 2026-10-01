#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

clear
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}║              🤖 Hamed AI Dashboard                        ║${NC}"
echo -e "${GREEN}║              Android/Termux Installer                     ║${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if running in Termux
if [ ! -d "$HOME/.termux" ]; then
    echo -e "${RED}⚠️  هذا السكريبت مخصص لـ Termux على أندرويد${NC}"
    echo ""
    echo "لتثبيته على الموبايل:"
    echo ""
    echo -e "${BLUE}1. حمّل Termux من:${NC}"
    echo "   https://f-droid.org/packages/com.termux/"
    echo ""
    echo -e "${BLUE}2. افتح Termux واكتب:${NC}"
    echo "   pkg update && pkg install nodejs git"
    echo ""
    echo -e "${BLUE}3. شغّل المشروع:${NC}"
    echo "   git clone <repo-url>"
    echo "   cd hamed"
    echo "   npm install"
    echo "   npm run dev"
    echo ""
    echo -e "${BLUE}4. افتح المتصفح على:${NC}"
    echo "   http://localhost:5173"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ Termux detected${NC}"
echo ""

# Update packages
echo -e "${BLUE}📦 Updating packages...${NC}"
pkg update -y
pkg upgrade -y
echo ""

# Install Node.js if not exists
if ! command -v node &> /dev/null; then
    echo -e "${BLUE}📦 Installing Node.js...${NC}"
    pkg install nodejs -y
    echo ""
fi

# Install Git if not exists
if ! command -v git &> /dev/null; then
    echo -e "${BLUE}📦 Installing Git...${NC}"
    pkg install git -y
    echo ""
fi

echo -e "${GREEN}✓ Node.js version: $(node --version)${NC}"
echo ""

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}📦 Installing project dependencies...${NC}"
    npm install
    echo ""
fi

# Start server
echo -e "${YELLOW}🚀 Starting Hamed AI Dashboard...${NC}"
echo ""
echo -e "${GREEN}✓ Dashboard will be available at:${NC}"
echo -e "${BLUE}  http://localhost:5173${NC}"
echo ""
echo -e "${YELLOW}📱 Open this URL in your mobile browser${NC}"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

# Start dev server with host flag for mobile access
npm run dev -- --host 0.0.0.0
