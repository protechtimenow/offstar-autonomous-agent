# OffStar Autonomous Agent - Production Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 offstar && chown -R offstar:offstar /app
USER offstar

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -m offstar.cli.main health || exit 1

# Default command
CMD ["python", "-m", "offstar.cli.main", "demo"]

# Expose port for web interface (future)
EXPOSE 8080