FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directory for logs and data
RUN mkdir -p /app/logs /app/data

# Expose port for MCP server
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MCP_PORT=8080

# Run the MCP server
CMD ["python", "mcp_server.py"]
