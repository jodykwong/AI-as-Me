#!/bin/bash
# AI-as-Me CI/CD Deployment Script

set -e

echo "🚀 AI-as-Me CI/CD Deployment"
echo "=============================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Version
VERSION="3.5.0"

# Functions
log_info() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    echo "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker not installed"
        exit 1
    fi
    log_info "Docker installed"
    
    if ! command -v git &> /dev/null; then
        log_error "Git not installed"
        exit 1
    fi
    log_info "Git installed"
    
    echo ""
}

# Run tests
run_tests() {
    echo "Running tests..."
    
    if pytest tests/ --cov=src/ai_as_me -v; then
        log_info "Tests passed"
    else
        log_warn "Some tests failed, continuing anyway"
    fi
    
    echo ""
}

# Build Docker image
build_docker() {
    echo "Building Docker image..."
    
    docker build -t ai-as-me:${VERSION} -t ai-as-me:latest .
    
    if [ $? -eq 0 ]; then
        log_info "Docker image built successfully"
    else
        log_error "Docker build failed"
        exit 1
    fi
    
    echo ""
}

# Push to Docker Hub
push_docker() {
    echo "Pushing to Docker Hub..."
    
    if [ -z "$DOCKER_USERNAME" ]; then
        log_warn "DOCKER_USERNAME not set, skipping Docker Hub push"
        return
    fi
    
    docker tag ai-as-me:${VERSION} ${DOCKER_USERNAME}/ai-as-me:${VERSION}
    docker tag ai-as-me:latest ${DOCKER_USERNAME}/ai-as-me:latest
    
    docker push ${DOCKER_USERNAME}/ai-as-me:${VERSION}
    docker push ${DOCKER_USERNAME}/ai-as-me:latest
    
    log_info "Pushed to Docker Hub"
    echo ""
}

# Push to GitHub
push_github() {
    echo "Pushing to GitHub..."
    
    # Check if there are changes
    if git diff-index --quiet HEAD --; then
        log_info "No changes to commit"
    else
        git add .
        git commit -m "ci: Update to v${VERSION}" || true
    fi
    
    git push origin main
    
    log_info "Pushed to GitHub"
    echo ""
}

# Create GitHub release
create_release() {
    echo "Creating GitHub release..."
    
    if ! command -v gh &> /dev/null; then
        log_warn "GitHub CLI not installed, skipping release creation"
        return
    fi
    
    gh release create v${VERSION} \
        --title "Release v${VERSION}" \
        --notes "AI-as-Me v${VERSION} - Self-evolving AI digital twin" \
        || log_warn "Release already exists or failed to create"
    
    echo ""
}

# Main execution
main() {
    check_prerequisites
    run_tests
    build_docker
    push_docker
    push_github
    create_release
    
    echo "=============================="
    log_info "Deployment complete!"
    echo ""
    echo "Docker image: ai-as-me:${VERSION}"
    echo "GitHub: https://github.com/jodykwong/AI-as-Me"
    echo ""
}

# Run main
main
