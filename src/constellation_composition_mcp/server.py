"""
Constellation Composition MCP Server

Maps astronomical constellation patterns to compositional parameters for image generation.
Translates star positions, magnitudes, and mythological narratives into visual guidance.
"""

from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
import httpx
import json
import math

# Initialize MCP server
mcp = FastMCP("constellation_composition_mcp")

# ============================================================================
# CONSTELLATION DATA
# ============================================================================

# IAU 88 official constellations with metadata
CONSTELLATIONS = {
    "Andromeda": {
        "abbr": "And",
        "genitive": "Andromedae",
        "story": "Chained princess rescued by Perseus",
        "theme": "Sacrifice, rescue, beauty in chains",
        "visual_character": "Linear with graceful curves, horizontal spread",
        "brightness_profile": "moderate_to_bright",
        "star_count_visual": 7,
        "shape": "elongated_linear"
    },
    "Aquarius": {
        "abbr": "Aqr",
        "genitive": "Aquarii",
        "story": "Water bearer pouring from celestial jar",
        "theme": "Flow, abundance, giving",
        "visual_character": "Cascading downward flow, dispersed",
        "brightness_profile": "moderate",
        "star_count_visual": 8,
        "shape": "dispersed_cascade"
    },
    "Aquila": {
        "abbr": "Aql",
        "genitive": "Aquilae",
        "story": "Eagle carrying Zeus's thunderbolts",
        "theme": "Power, divine messenger, soaring",
        "visual_character": "Wings spread wide, central bright star",
        "brightness_profile": "very_bright_center",
        "star_count_visual": 6,
        "shape": "symmetric_wings"
    },
    "Aries": {
        "abbr": "Ari",
        "genitive": "Arietis",
        "story": "Golden fleece ram",
        "theme": "Courage, sacrifice, precious treasure",
        "visual_character": "Compact curved form, ram's horn",
        "brightness_profile": "bright",
        "star_count_visual": 4,
        "shape": "compact_curved"
    },
    "Cancer": {
        "abbr": "Cnc",
        "genitive": "Cancri",
        "story": "Crab sent by Hera to distract Hercules",
        "theme": "Persistence, protective shell",
        "visual_character": "Compact cluster, crab body",
        "brightness_profile": "faint_with_cluster",
        "star_count_visual": 5,
        "shape": "compact_central"
    },
    "Canis Major": {
        "abbr": "CMa",
        "genitive": "Canis Majoris",
        "story": "Greater hunting dog following Orion",
        "theme": "Loyalty, hunting, companionship",
        "visual_character": "Compact with brilliant Sirius, dynamic stance",
        "brightness_profile": "extremely_bright_star",
        "star_count_visual": 8,
        "shape": "compact_dynamic"
    },
    "Capricornus": {
        "abbr": "Cap",
        "genitive": "Capricorni",
        "story": "Sea-goat with fish tail",
        "theme": "Duality, earth and water, ambition",
        "visual_character": "Triangular form, goat's head to fish tail",
        "brightness_profile": "moderate",
        "star_count_visual": 7,
        "shape": "triangular"
    },
    "Cassiopeia": {
        "abbr": "Cas",
        "genitive": "Cassiopeiae",
        "story": "Vain queen bound to throne",
        "theme": "Pride, punishment, eternal vigilance",
        "visual_character": "Distinctive W or M shape, highly recognizable",
        "brightness_profile": "bright",
        "star_count_visual": 5,
        "shape": "w_zigzag"
    },
    "Centaurus": {
        "abbr": "Cen",
        "genitive": "Centauri",
        "story": "Wise centaur, teacher of heroes",
        "theme": "Wisdom, healing, mentorship",
        "visual_character": "Large spread, bow-wielding stance",
        "brightness_profile": "very_bright",
        "star_count_visual": 11,
        "shape": "large_complex"
    },
    "Cygnus": {
        "abbr": "Cyg",
        "genitive": "Cygni",
        "story": "Swan, Zeus in disguise, Northern Cross",
        "theme": "Transformation, grace, divine deception",
        "visual_character": "Perfect cross or swan in flight",
        "brightness_profile": "bright_cross",
        "star_count_visual": 6,
        "shape": "cross_symmetric"
    },
    "Gemini": {
        "abbr": "Gem",
        "genitive": "Geminorum",
        "story": "Twin brothers Castor and Pollux",
        "theme": "Brotherhood, duality, eternal bond",
        "visual_character": "Twin parallel figures, two bright stars",
        "brightness_profile": "two_bright_stars",
        "star_count_visual": 8,
        "shape": "parallel_twins"
    },
    "Leo": {
        "abbr": "Leo",
        "genitive": "Leonis",
        "story": "Nemean lion slain by Hercules",
        "theme": "Courage, royalty, invincibility",
        "visual_character": "Sickle for head/mane, triangle for body",
        "brightness_profile": "very_bright",
        "star_count_visual": 9,
        "shape": "sickle_triangle"
    },
    "Lyra": {
        "abbr": "Lyr",
        "genitive": "Lyrae",
        "story": "Orpheus's lyre",
        "theme": "Music, art, lost love",
        "visual_character": "Compact parallelogram, small but bright",
        "brightness_profile": "extremely_bright_star",
        "star_count_visual": 5,
        "shape": "compact_parallelogram"
    },
    "Orion": {
        "abbr": "Ori",
        "genitive": "Orionis",
        "story": "Great hunter with belt and sword",
        "theme": "Hunting prowess, tragic death, grandeur",
        "visual_character": "Hourglass with distinctive belt, large and commanding",
        "brightness_profile": "multiple_bright_stars",
        "star_count_visual": 10,
        "shape": "hourglass_belt"
    },
    "Pegasus": {
        "abbr": "Peg",
        "genitive": "Pegasi",
        "story": "Winged horse sprung from Medusa's blood",
        "theme": "Inspiration, flight, poetic achievement",
        "visual_character": "Great square with extended lines for head/legs",
        "brightness_profile": "bright_square",
        "star_count_visual": 9,
        "shape": "square_extended"
    },
    "Perseus": {
        "abbr": "Per",
        "genitive": "Persei",
        "story": "Hero who slew Medusa",
        "theme": "Heroism, clever strategy, reflection",
        "visual_character": "Curved chain from Cassiopeia, Medusa's head",
        "brightness_profile": "bright",
        "star_count_visual": 8,
        "shape": "curved_chain"
    },
    "Sagittarius": {
        "abbr": "Sgr",
        "genitive": "Sagittarii",
        "story": "Centaur archer aiming at Scorpius",
        "theme": "Aim, philosophy, adventure",
        "visual_character": "Teapot shape, pointing toward galactic center",
        "brightness_profile": "bright",
        "star_count_visual": 10,
        "shape": "teapot"
    },
    "Scorpius": {
        "abbr": "Sco",
        "genitive": "Scorpii",
        "story": "Scorpion that killed Orion",
        "theme": "Danger, deadly beauty, revenge",
        "visual_character": "Curved tail with stinger, bright red heart",
        "brightness_profile": "very_bright_red",
        "star_count_visual": 12,
        "shape": "curved_tail"
    },
    "Taurus": {
        "abbr": "Tau",
        "genitive": "Tauri",
        "story": "Bull form of Zeus, Pleiades sisters",
        "theme": "Strength, passion, pursuit",
        "visual_character": "V-shaped face, Pleiades cluster",
        "brightness_profile": "bright_with_cluster",
        "star_count_visual": 8,
        "shape": "v_shaped"
    },
    "Ursa Major": {
        "abbr": "UMa",
        "genitive": "Ursae Majoris",
        "story": "Great bear, transformed Callisto, Big Dipper",
        "theme": "Transformation, eternal circling, guidance",
        "visual_character": "Dipper shape, circumpolar, never setting",
        "brightness_profile": "bright",
        "star_count_visual": 7,
        "shape": "dipper"
    },
    "Ursa Minor": {
        "abbr": "UMi",
        "genitive": "Ursae Minoris",
        "story": "Little bear, contains North Star",
        "theme": "Guidance, steadfastness, eternal pivot",
        "visual_character": "Small dipper, Polaris at tail",
        "brightness_profile": "bright_pole_star",
        "star_count_visual": 7,
        "shape": "small_dipper"
    },
    "Virgo": {
        "abbr": "Vir",
        "genitive": "Virginis",
        "story": "Maiden of harvest, justice, or purity",
        "theme": "Harvest, innocence, justice",
        "visual_character": "Y-shaped figure, large sprawling",
        "brightness_profile": "very_bright",
        "star_count_visual": 9,
        "shape": "y_shaped"
    }
}

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ResponseFormat(str, Enum):
    """Output format for responses."""
    MARKDOWN = "markdown"
    JSON = "json"


class CompositionParameters(BaseModel):
    """Structured composition parameters derived from constellation."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    focal_points: List[Dict[str, float]] = Field(
        description="Primary focal points mapped from brightest stars, with x/y coordinates (0-1) and visual weight"
    )
    visual_flow: Dict[str, Any] = Field(
        description="Directional flow and movement patterns"
    )
    balance: Dict[str, Any] = Field(
        description="Visual balance characteristics"
    )
    spatial_distribution: str = Field(
        description="How elements spread across the frame"
    )
    mythology_themes: List[str] = Field(
        description="Key thematic elements from constellation mythology"
    )
    suggested_elements: Dict[str, List[str]] = Field(
        description="Suggested visual elements organized by category"
    )


class ConstellationSearchInput(BaseModel):
    """Input for searching constellations."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    query: Optional[str] = Field(
        default=None,
        description="Search by constellation name, theme, or visual characteristic (e.g., 'twins', 'hunting', 'cross shape')"
    )
    shape_type: Optional[str] = Field(
        default=None,
        description="Filter by shape: linear, curved, triangular, square, cross, dipper, dispersed, compact, symmetric"
    )
    brightness: Optional[str] = Field(
        default=None,
        description="Filter by brightness: faint, moderate, bright, very_bright, extremely_bright"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for structured data"
    )


class ConstellationCompositionInput(BaseModel):
    """Input for generating composition from constellation."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True, extra='forbid')
    
    constellation_name: str = Field(
        description="Name of constellation (e.g., 'Orion', 'Cassiopeia', 'Ursa Major')",
        min_length=3,
        max_length=50
    )
    canvas_width: Optional[int] = Field(
        default=1024,
        description="Width of composition canvas in pixels",
        ge=512,
        le=4096
    )
    canvas_height: Optional[int] = Field(
        default=1024,
        description="Height of composition canvas in pixels",
        ge=512,
        le=4096
    )
    include_mythology: bool = Field(
        default=True,
        description="Include mythological themes and narrative elements"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.JSON,
        description="Output format: 'json' for structured parameters or 'markdown' for descriptive guidance"
    )
    
    @field_validator('constellation_name')
    @classmethod
    def validate_constellation(cls, v: str) -> str:
        """Validate constellation name exists."""
        # Try exact match first
        for name in CONSTELLATIONS.keys():
            if v.lower() == name.lower():
                return name
        
        # Try abbreviation match
        for name, data in CONSTELLATIONS.items():
            if v.lower() == data['abbr'].lower():
                return name
        
        # If not found, return original (will be handled in tool)
        return v


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def fetch_constellation_data(constellation_abbr: str) -> Optional[Dict[str, Any]]:
    """
    Fetch constellation line data from d3-celestial repository.
    Returns GeoJSON with star positions and connections.
    """
    url = f"https://cdn.jsdelivr.net/gh/dieghernan/celestial_data@main/data/constellations.lines.min.geojson"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            # Find constellation by abbreviation
            for feature in data.get('features', []):
                if feature.get('properties', {}).get('id') == constellation_abbr:
                    return feature
            
            return None
    except Exception as e:
        return None


def map_constellation_to_composition(
    constellation_name: str,
    metadata: Dict[str, Any],
    geometry_data: Optional[Dict[str, Any]],
    canvas_width: int,
    canvas_height: int,
    include_mythology: bool
) -> CompositionParameters:
    """
    Core deterministic mapping from constellation data to composition parameters.
    This is the zero-LLM-cost layer that handles pure geometric translation.
    """
    
    # Extract visual characteristics
    shape = metadata.get('shape', 'dispersed')
    brightness = metadata.get('brightness_profile', 'moderate')
    
    # Generate focal points based on brightness profile
    focal_points = generate_focal_points(brightness, shape, canvas_width, canvas_height)
    
    # Determine visual flow
    visual_flow = determine_visual_flow(shape, geometry_data)
    
    # Calculate balance characteristics
    balance = calculate_balance(shape, focal_points)
    
    # Determine spatial distribution
    spatial_distribution = determine_spatial_distribution(shape, metadata.get('star_count_visual', 5))
    
    # Extract mythology themes
    mythology_themes = []
    if include_mythology:
        mythology_themes = extract_mythology_themes(metadata)
    
    # Generate suggested elements
    suggested_elements = generate_suggested_elements(metadata, shape, brightness)
    
    return CompositionParameters(
        focal_points=focal_points,
        visual_flow=visual_flow,
        balance=balance,
        spatial_distribution=spatial_distribution,
        mythology_themes=mythology_themes,
        suggested_elements=suggested_elements
    )


def generate_focal_points(
    brightness: str,
    shape: str,
    width: int,
    height: int
) -> List[Dict[str, float]]:
    """Generate focal point positions based on constellation brightness pattern."""
    
    points = []
    
    if 'two_bright_stars' in brightness:
        # Gemini pattern - two equal focal points
        points = [
            {'x': 0.35, 'y': 0.5, 'weight': 0.5},
            {'x': 0.65, 'y': 0.5, 'weight': 0.5}
        ]
    elif 'extremely_bright_star' in brightness:
        # Sirius/Vega pattern - single dominant focal point
        points = [
            {'x': 0.5, 'y': 0.5, 'weight': 1.0},
            {'x': 0.35, 'y': 0.6, 'weight': 0.2},
            {'x': 0.65, 'y': 0.4, 'weight': 0.2}
        ]
    elif 'bright_cross' in brightness or 'cross' in shape:
        # Cygnus pattern - cross focal points
        points = [
            {'x': 0.5, 'y': 0.5, 'weight': 0.5},   # Center
            {'x': 0.5, 'y': 0.3, 'weight': 0.3},   # Top
            {'x': 0.3, 'y': 0.5, 'weight': 0.25},  # Left
            {'x': 0.7, 'y': 0.5, 'weight': 0.25},  # Right
            {'x': 0.5, 'y': 0.7, 'weight': 0.3}    # Bottom
        ]
    elif 'belt' in shape or 'hourglass' in shape:
        # Orion pattern - belt + shoulders/feet
        points = [
            {'x': 0.5, 'y': 0.45, 'weight': 0.4},  # Belt center
            {'x': 0.35, 'y': 0.3, 'weight': 0.35}, # Left shoulder
            {'x': 0.65, 'y': 0.3, 'weight': 0.35}, # Right shoulder
            {'x': 0.35, 'y': 0.7, 'weight': 0.25}, # Left foot
            {'x': 0.65, 'y': 0.7, 'weight': 0.25}  # Right foot
        ]
    elif 'w_zigzag' in shape:
        # Cassiopeia pattern - W shape
        points = [
            {'x': 0.2, 'y': 0.5, 'weight': 0.25},
            {'x': 0.35, 'y': 0.4, 'weight': 0.25},
            {'x': 0.5, 'y': 0.5, 'weight': 0.25},
            {'x': 0.65, 'y': 0.4, 'weight': 0.25},
            {'x': 0.8, 'y': 0.5, 'weight': 0.25}
        ]
    elif 'dipper' in shape:
        # Ursa Major pattern - dipper bowl + handle
        points = [
            {'x': 0.3, 'y': 0.45, 'weight': 0.25},  # Bowl corner
            {'x': 0.45, 'y': 0.45, 'weight': 0.25}, # Bowl corner
            {'x': 0.45, 'y': 0.6, 'weight': 0.25},  # Bowl corner
            {'x': 0.3, 'y': 0.6, 'weight': 0.25},   # Bowl corner
            {'x': 0.55, 'y': 0.5, 'weight': 0.2},   # Handle
            {'x': 0.65, 'y': 0.45, 'weight': 0.2},  # Handle
            {'x': 0.75, 'y': 0.4, 'weight': 0.2}    # Handle end
        ]
    elif 'square' in shape:
        # Pegasus pattern - great square
        points = [
            {'x': 0.35, 'y': 0.35, 'weight': 0.3},
            {'x': 0.65, 'y': 0.35, 'weight': 0.3},
            {'x': 0.65, 'y': 0.65, 'weight': 0.3},
            {'x': 0.35, 'y': 0.65, 'weight': 0.3}
        ]
    elif 'triangular' in shape:
        # Triangle pattern
        points = [
            {'x': 0.5, 'y': 0.3, 'weight': 0.4},
            {'x': 0.35, 'y': 0.65, 'weight': 0.35},
            {'x': 0.65, 'y': 0.65, 'weight': 0.35}
        ]
    elif 'curved' in shape or 'tail' in shape:
        # Curved sweep pattern (Scorpius)
        num_points = 7
        for i in range(num_points):
            t = i / (num_points - 1)
            x = 0.2 + 0.6 * t
            y = 0.5 + 0.2 * math.sin(t * math.pi)
            weight = 0.4 if i < 2 else 0.2
            points.append({'x': x, 'y': y, 'weight': weight})
    elif 'dispersed' in shape:
        # Scattered pattern
        import random
        random.seed(42)  # Deterministic
        for i in range(6):
            points.append({
                'x': 0.2 + random.random() * 0.6,
                'y': 0.2 + random.random() * 0.6,
                'weight': 0.2 + random.random() * 0.2
            })
    else:
        # Default: three-point composition
        points = [
            {'x': 0.5, 'y': 0.35, 'weight': 0.4},
            {'x': 0.35, 'y': 0.65, 'weight': 0.35},
            {'x': 0.65, 'y': 0.65, 'weight': 0.35}
        ]
    
    return points


def determine_visual_flow(shape: str, geometry_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Determine directional flow and movement patterns."""
    
    if 'cascade' in shape or 'dispersed_cascade' in shape:
        return {
            'primary_direction': 'downward',
            'flow_type': 'cascading',
            'movement_quality': 'fluid, dispersing',
            'rhythm': 'irregular, natural flow'
        }
    elif 'wings' in shape or 'symmetric' in shape:
        return {
            'primary_direction': 'horizontal',
            'flow_type': 'bilateral',
            'movement_quality': 'balanced, expansive',
            'rhythm': 'symmetrical'
        }
    elif 'curved' in shape or 'tail' in shape:
        return {
            'primary_direction': 'curved sweep',
            'flow_type': 'sinuous',
            'movement_quality': 'dynamic, flowing',
            'rhythm': 'continuous curve'
        }
    elif 'cross' in shape:
        return {
            'primary_direction': 'radial',
            'flow_type': 'centered',
            'movement_quality': 'stable, anchored',
            'rhythm': 'four-way symmetry'
        }
    elif 'linear' in shape or 'belt' in shape:
        return {
            'primary_direction': 'horizontal',
            'flow_type': 'linear',
            'movement_quality': 'direct, purposeful',
            'rhythm': 'regular spacing'
        }
    elif 'zigzag' in shape or 'w_' in shape:
        return {
            'primary_direction': 'alternating',
            'flow_type': 'zigzag',
            'movement_quality': 'energetic, angular',
            'rhythm': 'rhythmic alternation'
        }
    elif 'dipper' in shape:
        return {
            'primary_direction': 'L-shaped',
            'flow_type': 'segmented',
            'movement_quality': 'contained then extending',
            'rhythm': 'bowl to handle transition'
        }
    else:
        return {
            'primary_direction': 'multi-directional',
            'flow_type': 'balanced',
            'movement_quality': 'stable',
            'rhythm': 'varied'
        }


def calculate_balance(shape: str, focal_points: List[Dict[str, float]]) -> Dict[str, Any]:
    """Calculate visual balance characteristics."""
    
    # Calculate center of mass
    total_weight = sum(p['weight'] for p in focal_points)
    center_x = sum(p['x'] * p['weight'] for p in focal_points) / total_weight
    center_y = sum(p['y'] * p['weight'] for p in focal_points) / total_weight
    
    # Determine balance type
    if abs(center_x - 0.5) < 0.1 and abs(center_y - 0.5) < 0.1:
        balance_type = 'centered'
    elif abs(center_x - 0.5) < 0.1:
        balance_type = 'vertically_centered'
    elif abs(center_y - 0.5) < 0.1:
        balance_type = 'horizontally_centered'
    else:
        balance_type = 'asymmetric'
    
    # Check symmetry
    is_symmetric = 'symmetric' in shape or 'cross' in shape or 'square' in shape
    
    return {
        'balance_type': balance_type,
        'center_of_mass': {'x': center_x, 'y': center_y},
        'symmetry': 'symmetric' if is_symmetric else 'asymmetric',
        'stability': 'high' if balance_type == 'centered' else 'dynamic'
    }


def determine_spatial_distribution(shape: str, star_count: int) -> str:
    """Determine how elements spread across frame."""
    
    if 'compact' in shape:
        return 'clustered_central'
    elif 'dispersed' in shape or 'cascade' in shape:
        return 'scattered_wide'
    elif 'linear' in shape or 'belt' in shape:
        return 'linear_arrangement'
    elif star_count <= 5:
        return 'minimal_sparse'
    elif star_count >= 10:
        return 'complex_dense'
    else:
        return 'moderate_distributed'


def extract_mythology_themes(metadata: Dict[str, Any]) -> List[str]:
    """Extract key themes from constellation mythology."""
    
    story = metadata.get('story', '').lower()
    theme = metadata.get('theme', '').lower()
    
    themes = []
    
    # Parse explicit theme
    if theme:
        themes.extend([t.strip() for t in theme.split(',')])
    
    # Add implied themes from story
    if 'rescue' in story or 'save' in story:
        themes.append('heroic rescue')
    if 'hunt' in story or 'prey' in story:
        themes.append('the hunt')
    if 'transform' in story:
        themes.append('transformation')
    if 'death' in story or 'kill' in story or 'slay' in story:
        themes.append('mortality')
    if 'eternal' in story or 'immortal' in story:
        themes.append('eternity')
    if 'love' in story:
        themes.append('love and loss')
    if 'wisdom' in story or 'teacher' in story:
        themes.append('wisdom')
    if 'punishment' in story:
        themes.append('divine punishment')
    
    return themes[:5]  # Limit to top 5


def generate_suggested_elements(
    metadata: Dict[str, Any],
    shape: str,
    brightness: str
) -> Dict[str, List[str]]:
    """Generate concrete visual element suggestions."""
    
    suggestions = {
        'subjects': [],
        'lighting': [],
        'atmosphere': [],
        'color_palette': []
    }
    
    # Subject suggestions based on story
    story = metadata.get('story', '').lower()
    if 'hunt' in story:
        suggestions['subjects'] = ['figures in pursuit', 'dynamic poses', 'animals', 'weapons']
    elif 'rescue' in story:
        suggestions['subjects'] = ['hero and victim', 'chains or bonds', 'triumphant pose']
    elif 'music' in story or 'lyre' in story:
        suggestions['subjects'] = ['musical instruments', 'flowing fabric', 'contemplative pose']
    elif 'wisdom' in story:
        suggestions['subjects'] = ['scroll or book', 'teaching gesture', 'attentive students']
    else:
        suggestions['subjects'] = ['primary figure', 'supporting elements', 'narrative props']
    
    # Lighting based on brightness
    if 'extremely_bright' in brightness:
        suggestions['lighting'] = ['dramatic key light', 'high contrast', 'star-like highlights', 'radiating glow']
    elif 'two_bright' in brightness:
        suggestions['lighting'] = ['dual light sources', 'balanced illumination', 'twin highlights']
    elif 'bright_cross' in brightness:
        suggestions['lighting'] = ['four-point lighting', 'symmetrical illumination', 'centered highlight']
    else:
        suggestions['lighting'] = ['even lighting', 'gentle highlights', 'soft shadows']
    
    # Atmosphere based on shape
    if 'cascade' in shape:
        suggestions['atmosphere'] = ['flowing mist', 'falling elements', 'vertical movement']
    elif 'curved' in shape or 'tail' in shape:
        suggestions['atmosphere'] = ['swirling smoke', 'curved lines', 'dynamic energy']
    elif 'symmetric' in shape or 'cross' in shape:
        suggestions['atmosphere'] = ['balanced composition', 'architectural elements', 'formal symmetry']
    else:
        suggestions['atmosphere'] = ['natural environment', 'organic forms', 'irregular shapes']
    
    # Color palette suggestions
    theme = metadata.get('theme', '').lower()
    if 'water' in theme or 'flow' in theme:
        suggestions['color_palette'] = ['blues', 'teals', 'silver', 'flowing gradients']
    elif 'fire' in theme or 'power' in theme:
        suggestions['color_palette'] = ['reds', 'oranges', 'golds', 'warm tones']
    elif 'death' in theme or 'darkness' in theme:
        suggestions['color_palette'] = ['deep purples', 'blacks', 'dark blues', 'somber tones']
    elif 'wisdom' in theme or 'healing' in theme:
        suggestions['color_palette'] = ['greens', 'soft golds', 'earth tones', 'balanced hues']
    else:
        suggestions['color_palette'] = ['starlight whites', 'night sky blues', 'cosmic purples', 'celestial palette']
    
    return suggestions


def format_composition_markdown(
    constellation_name: str,
    metadata: Dict[str, Any],
    params: CompositionParameters
) -> str:
    """Format composition parameters as markdown."""
    
    md = f"# Constellation Composition: {constellation_name}\n\n"
    
    md += f"**Story:** {metadata.get('story', 'N/A')}\n\n"
    md += f"**Themes:** {metadata.get('theme', 'N/A')}\n\n"
    md += f"**Visual Character:** {metadata.get('visual_character', 'N/A')}\n\n"
    
    md += "## Focal Points\n\n"
    for i, point in enumerate(params.focal_points, 1):
        md += f"{i}. Position: ({point['x']:.2f}, {point['y']:.2f}) - Weight: {point['weight']:.2f}\n"
    
    md += "\n## Visual Flow\n\n"
    for key, value in params.visual_flow.items():
        md += f"- **{key.replace('_', ' ').title()}:** {value}\n"
    
    md += "\n## Balance\n\n"
    md += f"- **Type:** {params.balance['balance_type']}\n"
    md += f"- **Center of Mass:** ({params.balance['center_of_mass']['x']:.2f}, {params.balance['center_of_mass']['y']:.2f})\n"
    md += f"- **Symmetry:** {params.balance['symmetry']}\n"
    md += f"- **Stability:** {params.balance['stability']}\n"
    
    md += f"\n## Spatial Distribution\n\n"
    md += f"{params.spatial_distribution.replace('_', ' ').title()}\n"
    
    if params.mythology_themes:
        md += f"\n## Mythology Themes\n\n"
        for theme in params.mythology_themes:
            md += f"- {theme.title()}\n"
    
    md += "\n## Suggested Visual Elements\n\n"
    for category, elements in params.suggested_elements.items():
        md += f"### {category.replace('_', ' ').title()}\n\n"
        for elem in elements:
            md += f"- {elem}\n"
        md += "\n"
    
    return md


def format_search_results_markdown(results: List[Dict[str, Any]]) -> str:
    """Format constellation search results as markdown."""
    
    md = f"# Found {len(results)} Constellation(s)\n\n"
    
    for i, result in enumerate(results, 1):
        md += f"## {i}. {result['name']}\n\n"
        md += f"**Abbreviation:** {result['abbr']}\n\n"
        md += f"**Story:** {result['story']}\n\n"
        md += f"**Themes:** {result['theme']}\n\n"
        md += f"**Visual Character:** {result['visual_character']}\n\n"
        md += f"**Shape:** {result['shape'].replace('_', ' ').title()}\n\n"
        md += f"**Brightness:** {result['brightness_profile'].replace('_', ' ').title()}\n\n"
        md += "---\n\n"
    
    return md


# ============================================================================
# MCP TOOLS
# ============================================================================

@mcp.tool(
    name="search_constellations",
    annotations={
        "title": "Search Constellations by Theme or Characteristics",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def search_constellations(params: ConstellationSearchInput) -> str:
    """
    Search for constellations by name, theme, visual characteristics, or shape.
    
    Useful for discovering which constellations match specific compositional needs
    or thematic requirements. Returns constellation details including mythology,
    visual characteristics, and shape patterns.
    
    Args:
        params (ConstellationSearchInput): Search parameters including:
            - query: Text search for name/theme/characteristic
            - shape_type: Filter by geometric shape
            - brightness: Filter by brightness pattern
            - response_format: Output format (markdown or json)
    
    Returns:
        str: List of matching constellations with their characteristics
    """
    
    results = []
    
    for name, data in CONSTELLATIONS.items():
        match = True
        
        # Text query matching
        if params.query:
            query_lower = params.query.lower()
            searchable = f"{name} {data.get('story', '')} {data.get('theme', '')} {data.get('visual_character', '')}".lower()
            if query_lower not in searchable:
                match = False
        
        # Shape filter
        if params.shape_type and match:
            shape = data.get('shape', '')
            if params.shape_type.lower() not in shape.lower():
                match = False
        
        # Brightness filter
        if params.brightness and match:
            brightness = data.get('brightness_profile', '')
            if params.brightness.lower() not in brightness.lower():
                match = False
        
        if match:
            result = {
                'name': name,
                'abbr': data.get('abbr'),
                'story': data.get('story'),
                'theme': data.get('theme'),
                'visual_character': data.get('visual_character'),
                'shape': data.get('shape'),
                'brightness_profile': data.get('brightness_profile'),
                'star_count': data.get('star_count_visual')
            }
            results.append(result)
    
    if not results:
        return "No constellations found matching your criteria. Try broader search terms."
    
    if params.response_format == ResponseFormat.JSON:
        return json.dumps({'constellations': results, 'count': len(results)}, indent=2)
    else:
        return format_search_results_markdown(results)


@mcp.tool(
    name="generate_constellation_composition",
    annotations={
        "title": "Generate Composition Parameters from Constellation",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def generate_constellation_composition(params: ConstellationCompositionInput) -> str:
    """
    Generate detailed composition parameters mapped from a constellation's geometry and mythology.
    
    Translates astronomical star patterns into practical compositional guidance for image
    generation, including focal point placement, visual flow, balance characteristics,
    and thematic elements derived from constellation mythology.
    
    This uses a deterministic zero-LLM-cost approach for geometric translation,
    making it highly efficient for batch processing and consistent results.
    
    Args:
        params (ConstellationCompositionInput): Configuration including:
            - constellation_name: Name or abbreviation of constellation
            - canvas_width: Target canvas width in pixels (512-4096)
            - canvas_height: Target canvas height in pixels (512-4096)
            - include_mythology: Include mythological themes (boolean)
            - response_format: Output format (json or markdown)
    
    Returns:
        str: Structured composition parameters in requested format, including:
            - focal_points: List of primary visual anchors with positions and weights
            - visual_flow: Directional movement and rhythm patterns
            - balance: Visual balance type and center of mass
            - spatial_distribution: How elements spread across frame
            - mythology_themes: Key thematic elements from constellation story
            - suggested_elements: Concrete suggestions for subjects, lighting, atmosphere, colors
    """
    
    # Find constellation in database
    constellation_name = params.constellation_name
    if constellation_name not in CONSTELLATIONS:
        available = ', '.join(sorted(CONSTELLATIONS.keys()))
        return f"Error: Constellation '{constellation_name}' not found. Available constellations: {available}"
    
    metadata = CONSTELLATIONS[constellation_name]
    abbr = metadata['abbr']
    
    # Attempt to fetch real geometry data (optional enhancement)
    geometry_data = await fetch_constellation_data(abbr)
    
    # Generate composition parameters (deterministic, zero-LLM-cost)
    composition = map_constellation_to_composition(
        constellation_name=constellation_name,
        metadata=metadata,
        geometry_data=geometry_data,
        canvas_width=params.canvas_width,
        canvas_height=params.canvas_height,
        include_mythology=params.include_mythology
    )
    
    # Format response
    if params.response_format == ResponseFormat.JSON:
        result = {
            'constellation': constellation_name,
            'abbreviation': abbr,
            'canvas': {
                'width': params.canvas_width,
                'height': params.canvas_height
            },
            'composition': composition.model_dump()
        }
        return json.dumps(result, indent=2)
    else:
        return format_composition_markdown(constellation_name, metadata, composition)


@mcp.tool(
    name="list_all_constellations",
    annotations={
        "title": "List All Available Constellations",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def list_all_constellations(response_format: ResponseFormat = ResponseFormat.MARKDOWN) -> str:
    """
    List all available constellations with basic information.
    
    Provides a quick overview of all 22 major constellations available in the system,
    including their abbreviations and primary themes. Useful for browsing options
    or understanding the full scope of available compositional patterns.
    
    Args:
        response_format: Output format ('markdown' or 'json')
    
    Returns:
        str: Complete list of constellations with basic metadata
    """
    
    constellation_list = []
    for name, data in sorted(CONSTELLATIONS.items()):
        constellation_list.append({
            'name': name,
            'abbreviation': data.get('abbr'),
            'theme': data.get('theme'),
            'shape': data.get('shape')
        })
    
    if response_format == ResponseFormat.JSON:
        return json.dumps({
            'constellations': constellation_list,
            'total_count': len(constellation_list)
        }, indent=2)
    else:
        md = f"# Available Constellations ({len(constellation_list)})\n\n"
        for item in constellation_list:
            md += f"## {item['name']} ({item['abbreviation']})\n\n"
            md += f"**Theme:** {item['theme']}\n\n"
            md += f"**Shape Pattern:** {item['shape'].replace('_', ' ').title()}\n\n"
            md += "---\n\n"
        return md


# ============================================================================
# SERVER ENTRY POINT
# ============================================================================

def main():
    """Entry point for running the server."""
    mcp.run()


if __name__ == "__main__":
    main()
