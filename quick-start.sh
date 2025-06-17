#!/bin/bash

# OffStar Quick Start - Live Prototyping Script
# Run this script for immediate OffStar deployment

set -e

echo "🚀 OffStar Quick Start - Live Prototyping Mode"
echo "=============================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

# Create minimal .env for prototyping
echo "📁 Setting up environment..."
cat > .env << EOF
# OffStar Live Prototyping Configuration
PYTHONPATH=/app
LOG_LEVEL=INFO
ENVIRONMENT=development

# API Configuration (add your keys here)
ALCHEMY_API_KEY=your_alchemy_key_here
COINGECKO_API_KEY=your_coingecko_key_here

# Redis Configuration
REDIS_URL=redis://redis:6379

# Agent Configuration
AGENT_NAME=OffStar-Prototype
AGENT_VERSION=1.0.0
MAX_WORKERS=4

# Plugin Configuration
ENABLE_DEFI_PLUGIN=true
ENABLE_WEB_SEARCH=true
ENABLE_BLOCKCHAIN=true

# Development Mode
DEBUG=true
PROTOTYPE_MODE=true
EOF

# Build and run OffStar
echo "🔨 Building OffStar container..."
docker build -t offstar:prototype .

echo "🚀 Starting OffStar in prototype mode..."
docker run -d \
  --name offstar-prototype \
  --env-file .env \
  -p 8080:8080 \
  -v $(pwd)/logs:/app/logs \
  offstar:prototype

# Wait for startup
echo "⏳ Waiting for OffStar to initialize..."
sleep 10

# Test the agent
echo "🧪 Testing OffStar functionality..."
docker exec offstar-prototype python -c "
import asyncio
import sys
sys.path.append('/app')
from offstar.core.agent import OffStarAgent

async def test_agent():
    agent = OffStarAgent()
    await agent.initialize()
    print('✅ OffStar initialized successfully!')
    
    # Test DeFi plugin
    result = await agent.execute_task('defi_health_check', {})
    print(f'✅ DeFi plugin status: {result[\"status\"]}')
    
    return True

if asyncio.run(test_agent()):
    print('🎉 OffStar is ready for live prototyping!')
else:
    print('❌ OffStar initialization failed')
    exit(1)
"

echo ""
echo "🎉 OffStar Live Prototyping Environment Ready!"
echo "=============================================="
echo ""
echo "📊 OffStar Agent: http://localhost:8080"
echo "📁 Logs location: ./logs/"
echo "🐳 Container name: offstar-prototype"
echo ""
echo "⚡ LIVE PROTOTYPING COMMANDS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "# Test DeFi analysis:"
echo "docker exec offstar-prototype python -m offstar.cli.main analyze-protocol --protocol uniswap_v3"
echo ""
echo "# Find yield opportunities:"
echo "docker exec offstar-prototype python -m offstar.cli.main find-yield"
echo ""
echo "# Check system health:"
echo "docker exec offstar-prototype python -m offstar.cli.main health"
echo ""
echo "# Interactive Python shell:"
echo "docker exec -it offstar-prototype python"
echo ""
echo "# View live logs:"
echo "docker logs -f offstar-prototype"
echo ""
echo "# Stop prototype:"
echo "docker stop offstar-prototype && docker rm offstar-prototype"
echo ""
echo "🔥 READY FOR LIVE PROTOTYPING! 🔥"