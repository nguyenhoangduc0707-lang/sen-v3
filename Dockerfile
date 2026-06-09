# DYT-01 Production Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright (optional, for legacy browser fallback)
RUN pip install playwright && playwright install chromium --with-deps

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 dytuser && chown -R dytuser:dytuser /app
USER dytuser

# Expose port
EXPOSE 8000

# Default command (override in docker-compose or k8s)
CMD ["python", "start.py", "api", "--no-reload", "--host", "0.0.0.0", "--port", "8000"]
