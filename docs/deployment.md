# Deployment Guide - AI-as-Me

## Story 12.4: 部署文档

### Prerequisites

- Python 3.10+
- pip
- Git

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/your-repo/ai-as-me.git
cd ai-as-me

# 2. Install dependencies
pip install -e .

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings

# 4. Initialize database
mkdir -p data

# 5. Start web dashboard
python -m ai_as_me.cli_main serve
```

### Docker Deployment

```bash
# Build image
docker build -t ai-as-me:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/config:/app/config \
  --env-file .env \
  --name ai-as-me \
  ai-as-me:latest
```

### Configuration

See [environment-variables.md](environment-variables.md) for all configuration options.

### Verification

```bash
# Check health
curl http://localhost:8000/api/health

# Access dashboard
open http://localhost:8000

# View API docs
open http://localhost:8000/docs
```

### Troubleshooting

**Port already in use:**
```bash
# Change port in config/settings.yaml
api:
  port: 8001
```

**Database permission error:**
```bash
chmod 755 data/
```

### Production Deployment

1. Use environment variables for secrets
2. Enable HTTPS
3. Configure CORS properly
4. Set up monitoring
5. Regular backups of data/ directory
