FROM python:3.10-slim

LABEL maintainer="AI-as-Me Team"
LABEL version="3.5.0"
LABEL description="Self-evolving AI digital twin system"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for OpenCode
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY soul/ ./soul/
COPY kanban/ ./kanban/

# Install Python dependencies (without heavy ML libs)
RUN pip install --no-cache-dir \
    fastapi==0.128.0 \
    uvicorn==0.38.0 \
    pydantic==2.12.5 \
    click \
    python-dotenv \
    aiofiles

# Install OpenCode
RUN npm install -g opencode-ai@1.1.3

# Create necessary directories
RUN mkdir -p logs experience inspiration_pool

# Set permissions
RUN chmod 700 soul 2>/dev/null || true

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Run the application
CMD ["uvicorn", "ai_as_me.dashboard.app:app", "--host", "0.0.0.0", "--port", "8080"]
