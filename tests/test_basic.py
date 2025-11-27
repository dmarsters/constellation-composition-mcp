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
