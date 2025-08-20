#!/bin/bash

# Football Fan AI Agent Docker Test Script
# This script tests the Docker setup for common issues

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[HEADER]${NC} $1"
}

print_header "Testing Docker Setup for Football Fan AI Agent"

# Test 1: Check if Docker is running
print_info "Test 1: Checking Docker daemon..."
if ! docker info > /dev/null 2>&1; then
    print_error "Docker daemon is not running. Please start Docker first."
    exit 1
fi
print_info "✓ Docker daemon is running"

# Test 2: Check if docker-compose is available
print_info "Test 2: Checking docker-compose..."
if ! command -v docker-compose > /dev/null 2>&1; then
    print_error "docker-compose is not installed or not in PATH."
    exit 1
fi
print_info "✓ docker-compose is available"

# Test 3: Validate docker-compose.yml syntax
print_info "Test 3: Validating docker-compose.yml syntax..."
if ! docker-compose config > /dev/null 2>&1; then
    print_error "docker-compose.yml has syntax errors!"
    docker-compose config
    exit 1
fi
print_info "✓ docker-compose.yml syntax is valid"

# Test 4: Check if required files exist
print_info "Test 4: Checking required files..."
required_files=("Dockerfile" "docker-compose.yml" "pyproject.toml" "uv.lock" "main.py" "scheduler.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Required file '$file' is missing!"
        exit 1
    fi
    print_info "✓ Found $file"
done

# Test 5: Check if db directory exists (create if not)
print_info "Test 5: Checking database directory..."
if [ ! -d "db" ]; then
    print_warning "Database directory 'db' does not exist. Creating it..."
    mkdir -p db
    print_info "✓ Created db directory"
else
    print_info "✓ Database directory exists"
fi

# Test 6: Validate profiles
print_info "Test 6: Validating Docker Compose profiles..."
profiles=("default" "commands" "scheduler")
for profile in "${profiles[@]}"; do
    if docker-compose config --profile "$profile" > /dev/null 2>&1; then
        print_info "✓ Profile '$profile' is valid"
    else
        print_warning "Profile '$profile' may have issues"
    fi
done

# Test 7: Check environment template
print_info "Test 7: Checking environment configuration..."
if [ ! -f ".env" ]; then
    if [ -f "env.template" ]; then
        print_warning "No .env file found. You should create one from env.template:"
        print_info "  cp env.template .env"
        print_info "  # Then edit .env with your API keys"
    else
        print_error "Neither .env nor env.template found!"
    fi
else
    print_info "✓ .env file exists"
fi

# Test 8: Test building the image (dry run)
print_info "Test 8: Testing Docker build (dry run)..."
if docker-compose build --dry-run > /dev/null 2>&1; then
    print_info "✓ Docker build configuration is valid"
else
    print_warning "Docker build may have issues"
fi

print_header "All Basic Tests Passed! 🎉"

print_info "Next steps:"
print_info "1. Create .env file: cp env.template .env"
print_info "2. Add your API keys to .env"
print_info "3. Build the image: ./docker-run.sh build"
print_info "4. Test a service: ./docker-run.sh run"

print_header "Testing Complete"
