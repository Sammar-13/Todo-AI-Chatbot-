# Use Python 3.11 slim image for a smaller footprint
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for building Python packages and PostgreSQL adapter
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
# We copy src/app to /app/app so that the 'app' package is at the root of PYTHONPATH
COPY src/app /app/app

# Set environment variables
# PYTHONPATH=/app ensures that 'import app' works correctly
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 8000

# Health check using Python's http.client to avoid installing curl
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import http.client; conn = http.client.HTTPConnection('localhost', 8000); conn.request('GET', '/health'); exit(0 if conn.getresponse().status == 200 else 1)" || exit 1

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]