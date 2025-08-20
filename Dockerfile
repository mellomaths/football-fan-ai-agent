# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy uv configuration files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv and create virtual environment
RUN uv sync --frozen

# Copy source code
COPY . .

# Create db directory if it doesn't exist
RUN mkdir -p db

# Set permissions
RUN chmod +x main.py

# Activate the virtual environment for all subsequent commands
ENV PATH="/app/.venv/bin:$PATH"

# Create db directory if it doesn't exist
RUN mkdir -p db

# Set permissions
RUN chmod +x main.py

# Expose port (if needed for future web interface)
EXPOSE 8000

# Health check for the scheduler service
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD /app/.venv/bin/python -c "import schedule; print('Health check passed')" || exit 1

# No default CMD - allows flexible entrypoints
# Use docker-compose or docker run with specific commands
