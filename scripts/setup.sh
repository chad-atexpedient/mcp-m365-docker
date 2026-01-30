#!/bin/bash

# MCP M365 Docker Platform Setup Script

set -e

echo "🚀 Setting up MCP M365 Docker Platform..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs data config

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your Azure credentials!"
else
    echo "✅ .env file already exists"
fi

# Check if credentials are configured
if grep -q "your_client_id_here" .env 2>/dev/null; then
    echo "⚠️  WARNING: Azure credentials not configured in .env file"
    echo "Please edit .env and add your credentials before running docker-compose up"
fi

# Set proper permissions
echo "🔐 Setting permissions..."
chmod +x scripts/*.sh
chmod 755 logs data config

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Azure credentials"
echo "2. Run: docker-compose up -d"
echo "3. Check logs: docker-compose logs -f"
echo ""
echo "For more information, see README.md"
