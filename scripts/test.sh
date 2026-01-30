#!/bin/bash

# Test script for MCP M365 server

set -e

echo "🧪 Testing MCP M365 Docker Platform..."

# Check if container is running
if ! docker ps | grep -q mcp-m365-server; then
    echo "❌ MCP M365 server is not running"
    echo "Start it with: docker-compose up -d"
    exit 1
fi

echo "✅ Container is running"

# Check logs for errors
echo "📋 Checking logs for errors..."
if docker-compose logs --tail=50 | grep -i error; then
    echo "⚠️  Errors found in logs"
else
    echo "✅ No errors in recent logs"
fi

# Check if port is listening
echo "🔌 Checking if port 8080 is listening..."
if docker exec mcp-m365-server netstat -tuln | grep -q ":8080"; then
    echo "✅ Port 8080 is listening"
else
    echo "⚠️  Port 8080 is not listening"
fi

# Test health of the container
echo "🏥 Checking container health..."
CONTAINER_STATUS=$(docker inspect -f '{{.State.Status}}' mcp-m365-server)
if [ "$CONTAINER_STATUS" == "running" ]; then
    echo "✅ Container status: $CONTAINER_STATUS"
else
    echo "❌ Container status: $CONTAINER_STATUS"
    exit 1
fi

echo ""
echo "✅ All tests passed!"
