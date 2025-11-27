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
