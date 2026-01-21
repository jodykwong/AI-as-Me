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

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Install OpenCode
RUN npm install -g opencode-ai@1.1.3

# Create necessary directories
RUN mkdir -p logs experience inspiration_pool

# Set permissions
RUN chmod 700 soul && chmod 600 soul/*.md

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Run the application
CMD ["python", "-m", "ai_as_me.dashboard"]
