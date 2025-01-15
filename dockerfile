# Build stage
FROM python:3.9-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.9-slim

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/

# Create necessary directories
RUN mkdir -p static config

# Copy application files
COPY main.py .
COPY static/index.html static/
COPY config/config.py config/

# Expose Flask port
EXPOSE 5000

# Start Flask app
CMD ["python", "main.py"]