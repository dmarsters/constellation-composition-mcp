#!/bin/bash
set -e

# Standard MCP Server Setup Pattern
# Generates all directories and small files automatically
# Large Python files (server.py, test files) should be added manually afterward

PROJECT_NAME="constellation-composition-mcp"
PACKAGE_NAME="constellation_composition_mcp"
DESCRIPTION="MCP server that maps astronomical constellation patterns to compositional parameters"

echo "Creating directory structure for ${PROJECT_NAME}..."

# Create main directories
mkdir -p src/${PACKAGE_NAME}
mkdir -p tests
mkdir -p docs
mkdir -p examples

# Create src package files
echo "Creating package files..."

# __init__.py
cat > src/${PACKAGE_NAME}/__init__.py << 'EOF'
"""Constellation Composition MCP Server.

Maps astronomical constellation patterns to compositional parameters
for image generation.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("constellation-composition-mcp")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["__version__"]
EOF

# __main__.py
cat > src/${PACKAGE_NAME}/__main__.py << 'EOF'
"""Entry point for running constellation-composition-mcp as a module."""

from constellation_composition_mcp.server import main

if __name__ == "__main__":
    main()
EOF

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "constellation-composition-mcp"
version = "0.1.0"
description = "MCP server that maps astronomical constellation patterns to compositional parameters for image generation"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Dal", email = "dal@lushy.ai"}
]
keywords = ["mcp", "constellation", "composition", "image-generation", "astronomy"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "fastmcp>=2.0.0",
    "httpx>=0.27.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]

[project.scripts]
constellation-composition-mcp = "constellation_composition_mcp.server:main"

[project.urls]
Homepage = "https://github.com/yourusername/constellation-composition-mcp"
Repository = "https://github.com/yourusername/constellation-composition-mcp"
Issues = "https://github.com/yourusername/constellation-composition-mcp/issues"

[tool.hatch.build.targets.wheel]
packages = ["src/constellation_composition_mcp"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
pythonpath = ["src"]

[tool.black]
line-length = 100
target-version = ['py310']

[tool.ruff]
line-length = 100
target-version = "py310"
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
EOF

# Create README.md
cat > README.md << 'EOF'
# Constellation Composition MCP Server

MCP server that translates astronomical constellation patterns into compositional parameters for AI image generation.

## Features

- 22 major constellations with geometric and mythological metadata
- Zero-LLM-cost deterministic mapping from star patterns to focal points
- Mythology integration for thematic guidance
- Multiple output formats (JSON and Markdown)
- Canvas scaling from 512x512 to 4096x4096 pixels

## Installation

```bash
pip install -e ".[dev]"
```

## Usage

### As MCP Server

Add to Claude Desktop configuration:

```json
{
  "mcpServers": {
    "constellation-composition": {
      "command": "constellation-composition-mcp"
    }
  }
}
```

### Programmatically

```python
from constellation_composition_mcp.server import (
    generate_constellation_composition,
    search_constellations
)

# Search for constellations
results = await search_constellations(query="hunting")

# Generate composition
composition = await generate_constellation_composition(
    constellation_name="Orion",
    canvas_width=1920,
    canvas_height=1080
)
```

## Available Tools

1. **search_constellations** - Search by theme, shape, or brightness
2. **generate_constellation_composition** - Map constellation to composition parameters
3. **list_all_constellations** - Browse all available constellations

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
./tests/run_tests.sh

# Format code
black src/ tests/
ruff check src/ tests/
```

## Documentation

See `docs/` directory for detailed documentation:
- Architecture overview
- Integration examples
- Constellation database reference

## License

MIT License - See LICENSE file for details
EOF

# Create LICENSE
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 Dal Masters / Lushy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# OS
.DS_Store
Thumbs.db
EOF

# Create test structure
echo "Creating test files..."

# Basic test file
cat > tests/test_basic.py << 'EOF'
"""Basic tests for constellation composition MCP server."""

import pytest
from constellation_composition_mcp.server import CONSTELLATIONS


def test_constellations_loaded():
    """Test that constellation database is loaded."""
    assert len(CONSTELLATIONS) > 0
    assert "Orion" in CONSTELLATIONS


def test_constellation_metadata():
    """Test constellation metadata structure."""
    orion = CONSTELLATIONS["Orion"]
    assert "abbr" in orion
    assert "story" in orion
    assert "theme" in orion
    assert "shape" in orion
    assert orion["abbr"] == "Ori"


@pytest.mark.asyncio
async def test_search_functionality():
    """Test constellation search."""
    # Import will be added after server.py is created
    pass


@pytest.mark.asyncio
async def test_composition_generation():
    """Test composition parameter generation."""
    # Import will be added after server.py is created
    pass
EOF

# Test runner script
cat > tests/run_tests.sh << 'EOF'
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
EOF
chmod +x tests/run_tests.sh

# Create __init__.py for tests
cat > tests/__init__.py << 'EOF'
"""Tests for constellation-composition-mcp."""
EOF

# Create examples
cat > examples/basic_usage.py << 'EOF'
"""Basic usage examples for constellation composition MCP server."""

import asyncio
from constellation_composition_mcp.server import (
    CONSTELLATIONS,
    map_constellation_to_composition
)


async def example_orion():
    """Generate composition from Orion constellation."""
    constellation_name = "Orion"
    metadata = CONSTELLATIONS[constellation_name]
    
    composition = map_constellation_to_composition(
        constellation_name=constellation_name,
        metadata=metadata,
        geometry_data=None,
        canvas_width=1920,
        canvas_height=1080,
        include_mythology=True
    )
    
    print(f"Orion Composition for 1920x1080:")
    print(f"  Focal points: {len(composition.focal_points)}")
    print(f"  Visual flow: {composition.visual_flow['flow_type']}")
    print(f"  Balance: {composition.balance['balance_type']}")
    print(f"  Themes: {', '.join(composition.mythology_themes)}")


if __name__ == "__main__":
    asyncio.run(example_orion())
EOF

# Create docs structure
cat > docs/ARCHITECTURE.md << 'EOF'
# Architecture

## Three-Layer Design

1. **Deterministic Taxonomy** (zero cost)
   - Constellation database with geometric metadata
   - Shape classifications and brightness profiles
   
2. **Structured Parameters** (zero cost)
   - Focal point generation from star positions
   - Visual flow determination
   - Balance calculation
   
3. **Optional LLM Synthesis** (future)
   - Creative interpretation layer
   - Not required for basic functionality

## Cost Optimization

100% deterministic mapping = Zero LLM inference costs
EOF

cat > docs/INTEGRATION.md << 'EOF'
# Integration Guide

## ComfyUI Integration

```python
composition = generate_constellation_composition("Orion", 1920, 1080)
focal_points = composition['focal_points']

# Position nodes at focal points
for i, point in enumerate(focal_points):
    x = point['x'] * 1920
    y = point['y'] * 1080
    # Position element i at (x, y)
```

## Midjourney Integration

Use suggested elements in prompts:

```python
themes = composition['mythology_themes']
lighting = composition['suggested_elements']['lighting']
prompt = f"scene with {lighting[0]}, embodying {themes[0]}"
```
EOF

echo ""
echo "✅ Directory structure created successfully!"
echo ""
echo "Next steps:"
echo "1. Manually add server.py to src/constellation_composition_mcp/"
echo "2. Run ./verify_structure.sh to validate"
echo "3. Run pip install -e '.[dev]' from project root"
echo "4. Run ./tests/run_tests.sh to validate"
echo ""
