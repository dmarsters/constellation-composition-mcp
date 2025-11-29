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

## Author
Dal Marsters - Lushy.app
