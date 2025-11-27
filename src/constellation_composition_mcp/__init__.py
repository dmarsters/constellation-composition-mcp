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
