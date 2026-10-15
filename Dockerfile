# syntax=docker/dockerfile:1
# Multi-stage or optimized single-stage production-minded Dockerfile for FastAPI

# Use the official lightweight Python 3.12 slim image
FROM python:3.12-slim

# Prevent Python from writing .pyc files to disc and enable unbuffered terminal logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Set working directory inside container
WORKDIR /app

# Create a dedicated non-root user and group for security
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin appuser

# Install dependencies in a separate layer for efficient Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ ./app/

# Set ownership to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Document that the container listens on port 8000
EXPOSE 8000

# Health check instruction inside container
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Start the Uvicorn ASGI server binding to 0.0.0.0 for external network reachability
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
