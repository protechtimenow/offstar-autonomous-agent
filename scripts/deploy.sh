#!/bin/bash

# OffStar Autonomous Agent - Deployment Script
# Usage: ./scripts/deploy.sh [environment]

set -e

ENVIRONMENT=${1:-production}
echo "🚀 Deploying OffStar to $ENVIRONMENT environment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from template..."
    cp .env.template .env
    echo "📝 Please edit .env file with your configuration!"
    exit 1
fi

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Health check
echo "🏥 Running health checks..."
if docker exec offstar-agent python -m offstar.cli.main health; then
    echo "✅ OffStar is healthy and running!"
else
    echo "❌ Health check failed!"
    docker-compose logs offstar
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo "📊 Grafana dashboard: http://localhost:3000"
echo "📈 Prometheus: http://localhost:9090"
echo "🤖 OffStar agent: http://localhost:8080"

# Show running containers
echo "🐳 Running containers:"
docker-compose ps