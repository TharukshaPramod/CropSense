# Dockerfile (single image for all services; compose overrides command)
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system dependencies including bcrypt requirements
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
       build-essential gcc g++ libgomp1 git ca-certificates \
       pkg-config libffi-dev libssl-dev \
  && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (better cache)
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install Python deps
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

# Ensure data / model directories exist
RUN mkdir -p /app/data/raw /app/data/processed /app/predictor/models /app/common/models

# Expose ports used by services (not strictly required but convenient)
EXPOSE 8001 8002 8003 8004 8501 5672 15672

# Default command (overridden in docker-compose per-service)
CMD ["bash", "-c", "uvicorn data_collector.app:app --host 0.0.0.0 --port 8001"]