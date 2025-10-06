# Use Python 3.8 slim as base image
FROM python:3.8-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install PyTorch CPU version (smaller than GPU version)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install dependencies in multiple steps for better layer caching
COPY requirements.txt .

# Remove torch from requirements since we installed it separately
RUN grep -v "^torch" requirements.txt > requirements_no_torch.txt

# Install core dependencies first
RUN pip install --no-cache-dir \
    fastapi==0.115.0 \
    uvicorn[standard]==0.32.0 \
    pydantic==2.9.2 \
    pydantic-settings==2.1.0 \
    transformers

# Install remaining dependencies
RUN pip install --no-cache-dir -r requirements_no_torch.txt

# Final stage
FROM python:3.8-slim

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV WORKERS=4
ENV PORT=8000

# Expose port
EXPOSE ${PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Start Gunicorn with uvicorn workers
CMD gunicorn app.main:app \
    --bind 0.0.0.0:${PORT} \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers ${WORKERS} \
    --timeout 120 \
    --keep-alive 5 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
