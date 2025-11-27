#!/bin/bash
set -e

echo "Running constellation-composition-mcp tests..."
cd "$(dirname "$0")/.."

# Run pytest with coverage
python -m pytest tests/ \
    --cov=src/constellation_composition_mcp \
    --cov-report=html \
    --cov-report=term \
    -v

echo ""
echo "Tests complete! Coverage report in htmlcov/index.html"
