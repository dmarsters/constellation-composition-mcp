"""
Constellation Composition MCP Server

Maps astronomical constellation patterns to compositional parameters for image generation.
Translates star positions, magnitudes, and mythological narratives into visual guidance.
"""

from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any, Literal, Tuple
from enum import Enum
import httpx
import json
import math
import numpy as np

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
# PHASE 2.6 - CONSTELLATION PARAMETER SPACE & RHYTHMIC PRESETS
# ============================================================================
#
# Maps constellation aesthetics to a normalized 5D parameter space enabling:
# - Smooth trajectories between constellation states (Phase 1A)
# - Rhythmic oscillation between aesthetic poles (Phase 2.6)
# - Multi-domain composition with other Lushy aesthetic servers (Tier 4D)
# - Attractor visualization prompt generation (Phase 2.7)
#
# Parameters capture the visual qualities that vary across constellations:
# stellar_density     : Sparse isolated stars → dense rich star fields
# geometric_regularity: Organic flowing forms → precise geometric patterns
# luminance_contrast  : Even dim glow → extreme bright/dark contrast
# narrative_intensity : Quiet contemplation → dramatic mythic action
# spatial_extent      : Compact intimate → sprawling panoramic

CONSTELLATION_PARAMETER_NAMES = [
    "stellar_density",       # 0.0 = sparse (Cancer) → 1.0 = dense (Scorpius)
    "geometric_regularity",  # 0.0 = organic/flowing → 1.0 = geometric/precise
    "luminance_contrast",    # 0.0 = even/dim → 1.0 = extreme contrast
    "narrative_intensity",   # 0.0 = contemplative → 1.0 = dramatic/violent
    "spatial_extent"         # 0.0 = compact/intimate → 1.0 = sprawling/panoramic
]

# Canonical constellation states anchoring the morphospace
# Each maps a representative constellation to normalized [0.0, 1.0] coordinates
CONSTELLATION_CANONICAL_STATES = {
    "orion_grandeur": {
        "stellar_density": 0.85,
        "geometric_regularity": 0.70,
        "luminance_contrast": 0.90,
        "narrative_intensity": 0.85,
        "spatial_extent": 0.90,
        "source_constellation": "Orion",
        "description": "Commanding hourglass, multiple brilliant stars, hunter's dramatic stance"
    },
    "lyra_intimacy": {
        "stellar_density": 0.30,
        "geometric_regularity": 0.75,
        "luminance_contrast": 0.95,
        "narrative_intensity": 0.45,
        "spatial_extent": 0.20,
        "source_constellation": "Lyra",
        "description": "Compact parallelogram dominated by Vega's brilliance, musical melancholy"
    },
    "cassiopeia_rhythm": {
        "stellar_density": 0.45,
        "geometric_regularity": 0.85,
        "luminance_contrast": 0.65,
        "narrative_intensity": 0.55,
        "spatial_extent": 0.50,
        "source_constellation": "Cassiopeia",
        "description": "Rhythmic W zigzag, bright even pattern, regal punishment"
    },
    "scorpius_sweep": {
        "stellar_density": 0.90,
        "geometric_regularity": 0.25,
        "luminance_contrast": 0.85,
        "narrative_intensity": 0.95,
        "spatial_extent": 0.85,
        "source_constellation": "Scorpius",
        "description": "Sinuous curved tail with bright red Antares, deadly beauty"
    },
    "cancer_subtlety": {
        "stellar_density": 0.25,
        "geometric_regularity": 0.35,
        "luminance_contrast": 0.15,
        "narrative_intensity": 0.20,
        "spatial_extent": 0.25,
        "source_constellation": "Cancer",
        "description": "Faint compact cluster, quiet persistence, subtle presence"
    },
    "cygnus_symmetry": {
        "stellar_density": 0.50,
        "geometric_regularity": 0.95,
        "luminance_contrast": 0.70,
        "narrative_intensity": 0.50,
        "spatial_extent": 0.60,
        "source_constellation": "Cygnus",
        "description": "Perfect cross / Northern Cross, balanced four-fold symmetry, graceful flight"
    },
    "aquarius_flow": {
        "stellar_density": 0.55,
        "geometric_regularity": 0.20,
        "luminance_contrast": 0.40,
        "narrative_intensity": 0.35,
        "spatial_extent": 0.75,
        "source_constellation": "Aquarius",
        "description": "Cascading dispersed flow, water pouring downward, gentle abundance"
    }
}

# Phase 2.6 rhythmic presets - oscillation patterns between canonical states
# Period selection optimized for multi-domain composition:
#   Periods [15, 18, 22, 24, 28] create rich LCM interactions with
#   microscopy [10,16,20,24,30], nuclear [15,18], catastrophe [15,18,20,22,25],
#   diatom [12,15,18,20,30], heraldic [12,16,22,25,30]
CONSTELLATION_RHYTHMIC_PRESETS = {
    "stellar_tide": {
        "state_a": "orion_grandeur",
        "state_b": "cancer_subtlety",
        "pattern": "sinusoidal",
        "num_cycles": 3,
        "steps_per_cycle": 24,
        "description": "Grand spectacle ebbing to quiet subtlety and back — "
                       "the tide between Orion's commanding presence and Cancer's whisper"
    },
    "mythic_pulse": {
        "state_a": "scorpius_sweep",
        "state_b": "lyra_intimacy",
        "pattern": "sinusoidal",
        "num_cycles": 4,
        "steps_per_cycle": 18,
        "description": "Dramatic danger contracting to musical intimacy — "
                       "deadly scorpion yielding to Orpheus's lyre"
    },
    "symmetry_drift": {
        "state_a": "cygnus_symmetry",
        "state_b": "aquarius_flow",
        "pattern": "triangular",
        "num_cycles": 3,
        "steps_per_cycle": 22,
        "description": "Geometric precision dissolving into organic flow — "
                       "the Northern Cross melting into water's cascade"
    },
    "luminance_wave": {
        "state_a": "lyra_intimacy",
        "state_b": "cassiopeia_rhythm",
        "pattern": "sinusoidal",
        "num_cycles": 5,
        "steps_per_cycle": 15,
        "description": "Single blazing point expanding to rhythmic pattern — "
                       "Vega's dominance yielding to Cassiopeia's measured W"
    },
    "narrative_arc": {
        "state_a": "cancer_subtlety",
        "state_b": "scorpius_sweep",
        "pattern": "triangular",
        "num_cycles": 2,
        "steps_per_cycle": 28,
        "description": "Quiet origin building to dramatic climax — "
                       "the classical arc from stillness through danger"
    }
}

# ============================================================================
# PHASE 2.7 - VISUAL VOCABULARY FOR ATTRACTOR VISUALIZATION
# ============================================================================
#
# Maps regions of constellation parameter space to image-generation-ready
# visual vocabulary. Each visual type is a cluster in 5D space with
# associated keywords suitable for Stable Diffusion / ComfyUI / DALL-E.

CONSTELLATION_VISUAL_TYPES = {
    "celestial_drama": {
        "coords": {
            "stellar_density": 0.85,
            "geometric_regularity": 0.65,
            "luminance_contrast": 0.90,
            "narrative_intensity": 0.90,
            "spatial_extent": 0.85
        },
        "keywords": [
            "dramatic starfield with brilliant focal stars",
            "deep space nebula backdrop with high contrast",
            "heroic celestial figures traced in light",
            "bold star patterns against void black",
            "radiating stellar beams with warm highlights",
            "mythological grandeur at cosmic scale",
            "cinematic night sky composition"
        ]
    },
    "geometric_constellation": {
        "coords": {
            "stellar_density": 0.50,
            "geometric_regularity": 0.90,
            "luminance_contrast": 0.70,
            "narrative_intensity": 0.50,
            "spatial_extent": 0.55
        },
        "keywords": [
            "precise geometric star pattern on dark field",
            "clean constellation lines connecting bright nodes",
            "architectural symmetry in stellar arrangement",
            "mathematical precision of celestial geometry",
            "balanced point-light composition",
            "formal star chart aesthetic",
            "sharp white points on deep indigo"
        ]
    },
    "subtle_deepfield": {
        "coords": {
            "stellar_density": 0.30,
            "geometric_regularity": 0.30,
            "luminance_contrast": 0.20,
            "narrative_intensity": 0.25,
            "spatial_extent": 0.30
        },
        "keywords": [
            "faint scattered stars in soft darkness",
            "quiet deep field with gentle luminosity",
            "sparse points of light in vast emptiness",
            "contemplative night sky with subtle gradients",
            "understated cosmic stillness",
            "diffuse starlight barely visible"
        ]
    },
    "flowing_cascade": {
        "coords": {
            "stellar_density": 0.55,
            "geometric_regularity": 0.20,
            "luminance_contrast": 0.45,
            "narrative_intensity": 0.40,
            "spatial_extent": 0.75
        },
        "keywords": [
            "organic flowing star trails across wide field",
            "cascading stellar streams with soft gradients",
            "fluid arrangement of scattered light points",
            "natural meandering star patterns",
            "wide panoramic celestial landscape",
            "waterfall-like dispersal of starlight"
        ]
    },
    "blazing_jewel": {
        "coords": {
            "stellar_density": 0.35,
            "geometric_regularity": 0.70,
            "luminance_contrast": 0.95,
            "narrative_intensity": 0.50,
            "spatial_extent": 0.25
        },
        "keywords": [
            "single brilliant star dominating compact field",
            "jewel-like point of extreme brightness",
            "intimate concentrated stellar brilliance",
            "diamond-sharp highlight with diffraction spikes",
            "small precise constellation with one dazzling center",
            "gemstone radiance against velvet dark"
        ]
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


class RhythmicPresetInput(BaseModel):
    """Input for applying a rhythmic preset."""
    model_config = ConfigDict(str_strip_whitespace=True)

    preset_name: str = Field(
        description="Name of rhythmic preset: 'stellar_tide', 'mythic_pulse', "
                    "'symmetry_drift', 'luminance_wave', or 'narrative_arc'"
    )

    @field_validator('preset_name')
    @classmethod
    def validate_preset(cls, v: str) -> str:
        if v not in CONSTELLATION_RHYTHMIC_PRESETS:
            available = ", ".join(sorted(CONSTELLATION_RHYTHMIC_PRESETS.keys()))
            raise ValueError(f"Unknown preset '{v}'. Available: {available}")
        return v


class TrajectoryInput(BaseModel):
    """Input for computing trajectory between two constellation states."""
    model_config = ConfigDict(str_strip_whitespace=True)

    state_a: str = Field(
        description="Starting canonical state name (e.g., 'orion_grandeur', 'lyra_intimacy')"
    )
    state_b: str = Field(
        description="Target canonical state name"
    )
    steps: int = Field(
        default=10,
        description="Number of interpolation steps (2-100)",
        ge=2,
        le=100
    )

    @field_validator('state_a', 'state_b')
    @classmethod
    def validate_state(cls, v: str) -> str:
        if v not in CONSTELLATION_CANONICAL_STATES:
            available = ", ".join(sorted(CONSTELLATION_CANONICAL_STATES.keys()))
            raise ValueError(f"Unknown state '{v}'. Available: {available}")
        return v


class AttractorPromptInput(BaseModel):
    """Input for generating image-generation prompts from attractor coordinates."""
    model_config = ConfigDict(str_strip_whitespace=True)

    coordinates: Optional[Dict[str, float]] = Field(
        default=None,
        description="5D parameter coordinates. Keys: stellar_density, geometric_regularity, "
                    "luminance_contrast, narrative_intensity, spatial_extent. Values: 0.0-1.0. "
                    "If omitted, use canonical_state instead."
    )
    canonical_state: Optional[str] = Field(
        default=None,
        description="Name of a canonical state to use as source coordinates"
    )
    mode: Literal["composite", "split_keywords", "descriptive"] = Field(
        default="composite",
        description="'composite' = single blended prompt string, "
                    "'split_keywords' = categorized keyword lists, "
                    "'descriptive' = narrative prompt paragraph"
    )
    strength: float = Field(
        default=1.0,
        description="Blending strength 0.0-1.0 (lower = more neutral vocabulary)",
        ge=0.0,
        le=1.0
    )

    @field_validator('canonical_state')
    @classmethod
    def validate_canonical(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in CONSTELLATION_CANONICAL_STATES:
            available = ", ".join(sorted(CONSTELLATION_CANONICAL_STATES.keys()))
            raise ValueError(f"Unknown state '{v}'. Available: {available}")
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
# PHASE 2.6 - DYNAMICS HELPER FUNCTIONS
# ============================================================================

def _get_state_coordinates(state_name: str) -> Dict[str, float]:
    """Extract parameter coordinates from a canonical state, excluding metadata."""
    state = CONSTELLATION_CANONICAL_STATES[state_name]
    return {p: state[p] for p in CONSTELLATION_PARAMETER_NAMES}


def _generate_oscillation(num_steps: int, num_cycles: float, pattern: str) -> np.ndarray:
    """Generate oscillation interpolation factor [0, 1] over time."""
    t = np.linspace(0, 2 * np.pi * num_cycles, num_steps, endpoint=False)

    if pattern == "sinusoidal":
        return 0.5 * (1.0 + np.sin(t))
    elif pattern == "triangular":
        t_norm = (t / (2 * np.pi)) % 1.0
        return np.where(t_norm < 0.5, 2.0 * t_norm, 2.0 * (1.0 - t_norm))
    elif pattern == "square":
        t_norm = (t / (2 * np.pi)) % 1.0
        return np.where(t_norm < 0.5, 0.0, 1.0)
    else:
        raise ValueError(f"Unknown oscillation pattern: {pattern}")


def _generate_preset_trajectory(preset_config: dict) -> List[Dict[str, float]]:
    """
    Generate a complete Phase 2.6 preset trajectory as list of state dicts.

    Returns one full period (steps_per_cycle states) for use with forced orbit
    integration and Tier 4D multi-domain composition.
    """
    state_a = _get_state_coordinates(preset_config["state_a"])
    state_b = _get_state_coordinates(preset_config["state_b"])

    steps = preset_config["steps_per_cycle"]
    alpha = _generate_oscillation(steps, 1, preset_config["pattern"])

    trajectory = []
    for i in range(steps):
        a = float(alpha[i])
        state = {
            p: (1.0 - a) * state_a[p] + a * state_b[p]
            for p in CONSTELLATION_PARAMETER_NAMES
        }
        trajectory.append(state)

    return trajectory


def _interpolate_states(
    state_a: Dict[str, float],
    state_b: Dict[str, float],
    steps: int
) -> List[Dict[str, float]]:
    """Smooth sinusoidal interpolation between two states (half-period: A → B)."""
    trajectory = []
    for i in range(steps):
        t = i / max(steps - 1, 1)
        # Smooth ease-in-out via cosine interpolation
        alpha = 0.5 * (1.0 - math.cos(t * math.pi))
        state = {
            p: (1.0 - alpha) * state_a[p] + alpha * state_b[p]
            for p in CONSTELLATION_PARAMETER_NAMES
        }
        trajectory.append(state)
    return trajectory


# ============================================================================
# PHASE 2.7 - ATTRACTOR VISUALIZATION HELPERS
# ============================================================================

def _extract_visual_vocabulary(
    coordinates: Dict[str, float],
    strength: float = 1.0
) -> Dict[str, Any]:
    """
    Find nearest visual type and extract weighted keywords from coordinates.

    Uses Euclidean distance in 5D parameter space to find the closest
    visual type, then returns its keywords scaled by strength.
    """
    coord_vec = np.array([coordinates.get(p, 0.5) for p in CONSTELLATION_PARAMETER_NAMES])

    best_type = None
    best_distance = float('inf')

    for type_name, type_data in CONSTELLATION_VISUAL_TYPES.items():
        type_vec = np.array([type_data["coords"][p] for p in CONSTELLATION_PARAMETER_NAMES])
        dist = float(np.linalg.norm(coord_vec - type_vec))
        if dist < best_distance:
            best_distance = dist
            best_type = type_name

    type_data = CONSTELLATION_VISUAL_TYPES[best_type]

    # Scale number of keywords by strength
    n_keywords = max(2, int(len(type_data["keywords"]) * strength))
    keywords = type_data["keywords"][:n_keywords]

    return {
        "nearest_type": best_type,
        "distance": round(best_distance, 4),
        "keywords": keywords,
        "all_keywords": type_data["keywords"],
        "strength": strength
    }


def _generate_composite_prompt(
    coordinates: Dict[str, float],
    strength: float = 1.0
) -> str:
    """
    Generate a single composite image-generation prompt from coordinates.

    Combines visual vocabulary with geometric specifications derived
    from parameter values for explicit, actionable prompts.
    """
    vocab = _extract_visual_vocabulary(coordinates, strength)

    # Build geometric specifications from raw parameter values
    specs = []

    sd = coordinates.get("stellar_density", 0.5)
    if sd > 0.7:
        specs.append("dense rich starfield filling the frame")
    elif sd < 0.3:
        specs.append("sparse isolated points of light with wide spacing")

    gr = coordinates.get("geometric_regularity", 0.5)
    if gr > 0.7:
        specs.append("precise geometric arrangement of stellar elements")
    elif gr < 0.3:
        specs.append("organic flowing placement without rigid structure")

    lc = coordinates.get("luminance_contrast", 0.5)
    if lc > 0.7:
        specs.append("extreme brightness contrast between star and void")
    elif lc < 0.3:
        specs.append("soft even luminosity with minimal contrast")

    ni = coordinates.get("narrative_intensity", 0.5)
    if ni > 0.7:
        specs.append("dramatic mythological atmosphere with dynamic tension")
    elif ni < 0.3:
        specs.append("contemplative quiet mood with meditative stillness")

    se = coordinates.get("spatial_extent", 0.5)
    if se > 0.7:
        specs.append("wide panoramic field of view spanning the heavens")
    elif se < 0.3:
        specs.append("intimate tight framing on compact stellar group")

    # Compose: keywords first, then specifications
    keyword_str = ", ".join(vocab["keywords"])
    spec_str = ", ".join(specs) if specs else ""

    if spec_str:
        return f"{keyword_str}, {spec_str}"
    return keyword_str


def _generate_descriptive_prompt(
    coordinates: Dict[str, float],
    strength: float = 1.0
) -> str:
    """Generate a narrative paragraph prompt from coordinates."""
    vocab = _extract_visual_vocabulary(coordinates, strength)

    sd = coordinates.get("stellar_density", 0.5)
    lc = coordinates.get("luminance_contrast", 0.5)
    ni = coordinates.get("narrative_intensity", 0.5)
    gr = coordinates.get("geometric_regularity", 0.5)
    se = coordinates.get("spatial_extent", 0.5)

    density_word = "rich dense" if sd > 0.6 else "sparse scattered" if sd < 0.4 else "moderate"
    contrast_word = "brilliant high-contrast" if lc > 0.6 else "soft diffuse" if lc < 0.4 else "balanced"
    mood_word = "dramatic and mythic" if ni > 0.6 else "quiet and contemplative" if ni < 0.4 else "measured"
    form_word = "geometrically precise" if gr > 0.6 else "organically flowing" if gr < 0.4 else "naturally balanced"
    scale_word = "expansive panoramic" if se > 0.6 else "intimate compact" if se < 0.4 else "moderately scaled"

    return (
        f"A {scale_word} celestial composition with {density_word} starfield. "
        f"The arrangement is {form_word}, with {contrast_word} luminance "
        f"creating a {mood_word} atmosphere. "
        f"{'. '.join(vocab['keywords'][:3])}."
    )


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
# PHASE 2.6 / 2.7 MCP TOOLS
# ============================================================================

@mcp.tool(
    name="get_server_info",
    annotations={
        "title": "Get Server Info and Capabilities",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def get_server_info() -> str:
    """
    Get server metadata, capabilities, and Phase 2.6/2.7 status.

    Layer 1: Pure reference (0 tokens).

    Returns comprehensive information about the constellation composition
    server including available tools, parameter space dimensions, canonical
    states, rhythmic presets, and visual vocabulary types.
    """
    info = {
        "server": "constellation_composition_mcp",
        "description": "Maps astronomical constellation patterns to compositional "
                       "parameters, rhythmic dynamics, and image generation prompts",
        "version": "2.7.0",
        "constellations_available": len(CONSTELLATIONS),
        "parameter_space": {
            "dimensions": len(CONSTELLATION_PARAMETER_NAMES),
            "parameters": CONSTELLATION_PARAMETER_NAMES,
            "bounds": [0.0, 1.0],
            "canonical_states": len(CONSTELLATION_CANONICAL_STATES)
        },
        "phase_1a_trajectory": {
            "enabled": True,
            "method": "cosine_interpolation",
            "tools": ["compute_constellation_trajectory"]
        },
        "phase_2_6_rhythmic": {
            "enabled": True,
            "presets": {
                name: {
                    "period": cfg["steps_per_cycle"],
                    "pattern": cfg["pattern"],
                    "states": f"{cfg['state_a']} ↔ {cfg['state_b']}"
                }
                for name, cfg in CONSTELLATION_RHYTHMIC_PRESETS.items()
            },
            "all_periods": sorted(set(
                p["steps_per_cycle"] for p in CONSTELLATION_RHYTHMIC_PRESETS.values()
            )),
            "tools": ["list_constellation_presets", "apply_constellation_preset"]
        },
        "phase_2_7_visualization": {
            "enabled": True,
            "visual_types": list(CONSTELLATION_VISUAL_TYPES.keys()),
            "visual_type_count": len(CONSTELLATION_VISUAL_TYPES),
            "prompt_modes": ["composite", "split_keywords", "descriptive"],
            "tools": ["generate_constellation_attractor_prompt"]
        },
        "tier_4d_composition": {
            "compatible": True,
            "domain_id": "constellation",
            "tools": ["get_constellation_coordinates",
                      "get_constellation_domain_registry_config"]
        }
    }
    return json.dumps(info, indent=2)


@mcp.tool(
    name="get_constellation_coordinates",
    annotations={
        "title": "Extract 5D Parameter Coordinates for a Constellation or State",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def get_constellation_coordinates(
    name: str,
    response_format: ResponseFormat = ResponseFormat.JSON
) -> str:
    """
    Extract normalized 5D parameter coordinates for a canonical state or
    constellation name.

    Layer 1: Pure taxonomy lookup (0 tokens).

    If a canonical state name is given (e.g. 'orion_grandeur'), returns its
    exact coordinates. If a constellation name is given (e.g. 'Orion'),
    returns the nearest canonical state's coordinates with distance metric.

    Coordinates are suitable for:
    - Trajectory computation (Phase 1A)
    - Rhythmic composition input (Phase 2.6)
    - Attractor visualization (Phase 2.7)
    - Multi-domain composition (Tier 4D)
    """
    # Direct canonical state lookup
    if name in CONSTELLATION_CANONICAL_STATES:
        state = CONSTELLATION_CANONICAL_STATES[name]
        coords = {p: state[p] for p in CONSTELLATION_PARAMETER_NAMES}
        result = {
            "state_name": name,
            "source_constellation": state.get("source_constellation", ""),
            "description": state.get("description", ""),
            "coordinates": coords,
            "parameter_names": CONSTELLATION_PARAMETER_NAMES,
            "match_type": "exact_canonical"
        }
    else:
        # Try to match constellation name to nearest canonical state
        target_name = None
        for cname in CONSTELLATIONS:
            if name.lower() == cname.lower():
                target_name = cname
                break
            if name.lower() == CONSTELLATIONS[cname]['abbr'].lower():
                target_name = cname
                break

        if not target_name:
            available_states = ", ".join(sorted(CONSTELLATION_CANONICAL_STATES.keys()))
            available_const = ", ".join(sorted(CONSTELLATIONS.keys()))
            return json.dumps({
                "error": f"'{name}' not found",
                "available_canonical_states": available_states,
                "available_constellations": available_const
            }, indent=2)

        # Find canonical state sourced from this constellation
        exact_match = None
        for sname, sdata in CONSTELLATION_CANONICAL_STATES.items():
            if sdata.get("source_constellation", "").lower() == target_name.lower():
                exact_match = sname
                break

        if exact_match:
            state = CONSTELLATION_CANONICAL_STATES[exact_match]
            coords = {p: state[p] for p in CONSTELLATION_PARAMETER_NAMES}
            result = {
                "state_name": exact_match,
                "source_constellation": target_name,
                "description": state.get("description", ""),
                "coordinates": coords,
                "parameter_names": CONSTELLATION_PARAMETER_NAMES,
                "match_type": "constellation_to_canonical"
            }
        else:
            # Infer coordinates from constellation metadata
            meta = CONSTELLATIONS[target_name]
            coords = _infer_coordinates_from_metadata(meta)
            result = {
                "state_name": None,
                "source_constellation": target_name,
                "description": f"Inferred from {target_name} metadata (no canonical state)",
                "coordinates": coords,
                "parameter_names": CONSTELLATION_PARAMETER_NAMES,
                "match_type": "inferred"
            }

    if response_format == ResponseFormat.JSON:
        return json.dumps(result, indent=2)
    else:
        md = f"# Coordinates: {result.get('state_name') or result['source_constellation']}\n\n"
        md += f"**Match type:** {result['match_type']}\n\n"
        md += f"**Description:** {result['description']}\n\n"
        for p in CONSTELLATION_PARAMETER_NAMES:
            val = result['coordinates'][p]
            bar = "█" * int(val * 20)
            md += f"- `{p}`: {val:.2f} {bar}\n"
        return md


@mcp.tool(
    name="list_constellation_presets",
    annotations={
        "title": "List Phase 2.6 Rhythmic Presets",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def list_constellation_presets(
    response_format: ResponseFormat = ResponseFormat.JSON
) -> str:
    """
    List all available Phase 2.6 rhythmic presets with their parameters.

    Layer 1: Pure taxonomy lookup (0 tokens).

    Returns preset names, periods, oscillation patterns, state pairs,
    and descriptions. Presets define temporal oscillation patterns between
    canonical constellation states for rhythmic composition and Tier 4D
    multi-domain limit cycle discovery.
    """
    presets_info = {}
    for name, cfg in CONSTELLATION_RHYTHMIC_PRESETS.items():
        state_a = CONSTELLATION_CANONICAL_STATES[cfg["state_a"]]
        state_b = CONSTELLATION_CANONICAL_STATES[cfg["state_b"]]
        presets_info[name] = {
            "period": cfg["steps_per_cycle"],
            "pattern": cfg["pattern"],
            "num_cycles": cfg["num_cycles"],
            "total_steps": cfg["num_cycles"] * cfg["steps_per_cycle"],
            "state_a": {
                "name": cfg["state_a"],
                "constellation": state_a.get("source_constellation", ""),
                "coordinates": {p: state_a[p] for p in CONSTELLATION_PARAMETER_NAMES}
            },
            "state_b": {
                "name": cfg["state_b"],
                "constellation": state_b.get("source_constellation", ""),
                "coordinates": {p: state_b[p] for p in CONSTELLATION_PARAMETER_NAMES}
            },
            "description": cfg["description"]
        }

    if response_format == ResponseFormat.JSON:
        return json.dumps({
            "presets": presets_info,
            "all_periods": sorted(set(
                p["steps_per_cycle"] for p in CONSTELLATION_RHYTHMIC_PRESETS.values()
            )),
            "parameter_names": CONSTELLATION_PARAMETER_NAMES,
            "count": len(presets_info)
        }, indent=2)
    else:
        md = "# Constellation Rhythmic Presets (Phase 2.6)\n\n"
        for name, info in presets_info.items():
            md += f"## {name}\n\n"
            md += f"**Period:** {info['period']} steps | "
            md += f"**Pattern:** {info['pattern']} | "
            md += f"**Total steps:** {info['total_steps']}\n\n"
            md += f"**Oscillates:** {info['state_a']['name']} "
            md += f"({info['state_a']['constellation']}) ↔ "
            md += f"{info['state_b']['name']} ({info['state_b']['constellation']})\n\n"
            md += f"*{info['description']}*\n\n---\n\n"
        return md


@mcp.tool(
    name="apply_constellation_preset",
    annotations={
        "title": "Apply Rhythmic Preset — Generate Oscillation Sequence",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def apply_constellation_preset(params: RhythmicPresetInput) -> str:
    """
    Apply a Phase 2.6 rhythmic preset, generating a complete oscillation
    sequence over one full period.

    Layer 2: Deterministic sequence generation (0 tokens).

    Returns a trajectory of 5D coordinate states tracing one complete cycle
    of the preset oscillation. This output is directly usable by:
    - Tier 4D integrate_forced_limit_cycle for single-domain orbits
    - Tier 4D integrate_forced_limit_cycle_multi_domain for composition
    - Phase 2.7 generate_constellation_attractor_prompt for keyframe prompts
    """
    cfg = CONSTELLATION_RHYTHMIC_PRESETS[params.preset_name]
    trajectory = _generate_preset_trajectory(cfg)

    return json.dumps({
        "preset_name": params.preset_name,
        "period": cfg["steps_per_cycle"],
        "pattern": cfg["pattern"],
        "state_a": cfg["state_a"],
        "state_b": cfg["state_b"],
        "description": cfg["description"],
        "parameter_names": CONSTELLATION_PARAMETER_NAMES,
        "trajectory": trajectory,
        "trajectory_length": len(trajectory)
    }, indent=2)


@mcp.tool(
    name="compute_constellation_trajectory",
    annotations={
        "title": "Compute Smooth Trajectory Between Two Constellation States",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def compute_constellation_trajectory(params: TrajectoryInput) -> str:
    """
    Compute smooth interpolation trajectory between two canonical states.

    Layer 2: Deterministic interpolation (0 tokens).

    Uses cosine ease-in-out for perceptually smooth transitions. Each step
    includes full 5D coordinates suitable for attractor prompt generation
    or multi-domain composition input.
    """
    coords_a = _get_state_coordinates(params.state_a)
    coords_b = _get_state_coordinates(params.state_b)
    trajectory = _interpolate_states(coords_a, coords_b, params.steps)

    # Compute Euclidean distance between endpoints
    dist = math.sqrt(sum(
        (coords_a[p] - coords_b[p]) ** 2
        for p in CONSTELLATION_PARAMETER_NAMES
    ))

    return json.dumps({
        "state_a": params.state_a,
        "state_b": params.state_b,
        "steps": params.steps,
        "euclidean_distance": round(dist, 4),
        "parameter_names": CONSTELLATION_PARAMETER_NAMES,
        "trajectory": trajectory
    }, indent=2)


@mcp.tool(
    name="generate_constellation_attractor_prompt",
    annotations={
        "title": "Generate Image Prompt from Attractor Coordinates (Phase 2.7)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def generate_constellation_attractor_prompt(params: AttractorPromptInput) -> str:
    """
    Generate image-generation-ready prompts from 5D constellation coordinates.

    Layer 2: Deterministic vocabulary extraction (0 tokens).

    Translates abstract parameter coordinates into concrete visual vocabulary
    suitable for Stable Diffusion, ComfyUI, DALL-E, or Midjourney. Three
    output modes are available:

    - **composite**: Single prompt string combining keywords and geometric specs.
      Best for direct image generation.
    - **split_keywords**: Categorized keyword lists (visual type, specifications,
      parameter descriptors). Best for ComfyUI prompt engineering.
    - **descriptive**: Narrative paragraph prompt. Best for DALL-E / Midjourney.

    Coordinates can be provided directly, or derived from a canonical state name.
    """
    # Resolve coordinates
    if params.coordinates:
        coords = params.coordinates
        # Fill missing params with 0.5 default
        for p in CONSTELLATION_PARAMETER_NAMES:
            if p not in coords:
                coords[p] = 0.5
    elif params.canonical_state:
        state = CONSTELLATION_CANONICAL_STATES[params.canonical_state]
        coords = {p: state[p] for p in CONSTELLATION_PARAMETER_NAMES}
    else:
        return json.dumps({
            "error": "Provide either 'coordinates' dict or 'canonical_state' name"
        })

    vocab = _extract_visual_vocabulary(coords, params.strength)

    if params.mode == "composite":
        prompt = _generate_composite_prompt(coords, params.strength)
        return json.dumps({
            "mode": "composite",
            "prompt": prompt,
            "nearest_visual_type": vocab["nearest_type"],
            "type_distance": vocab["distance"],
            "coordinates": coords
        }, indent=2)

    elif params.mode == "split_keywords":
        # Build categorized keyword sets
        specs = {}
        sd = coords.get("stellar_density", 0.5)
        specs["density"] = (
            "dense rich starfield" if sd > 0.7
            else "sparse isolated stars" if sd < 0.3
            else "moderate star density"
        )
        gr = coords.get("geometric_regularity", 0.5)
        specs["geometry"] = (
            "precise geometric arrangement" if gr > 0.7
            else "organic flowing forms" if gr < 0.3
            else "naturally balanced arrangement"
        )
        lc = coords.get("luminance_contrast", 0.5)
        specs["luminance"] = (
            "extreme brightness contrast" if lc > 0.7
            else "soft even luminosity" if lc < 0.3
            else "moderate contrast"
        )
        ni = coords.get("narrative_intensity", 0.5)
        specs["mood"] = (
            "dramatic mythological atmosphere" if ni > 0.7
            else "contemplative quiet mood" if ni < 0.3
            else "balanced narrative tone"
        )
        se = coords.get("spatial_extent", 0.5)
        specs["scale"] = (
            "wide panoramic field" if se > 0.7
            else "intimate compact framing" if se < 0.3
            else "moderate field of view"
        )

        return json.dumps({
            "mode": "split_keywords",
            "visual_type_keywords": vocab["keywords"],
            "parameter_descriptors": specs,
            "nearest_visual_type": vocab["nearest_type"],
            "type_distance": vocab["distance"],
            "coordinates": coords
        }, indent=2)

    else:  # descriptive
        prompt = _generate_descriptive_prompt(coords, params.strength)
        return json.dumps({
            "mode": "descriptive",
            "prompt": prompt,
            "nearest_visual_type": vocab["nearest_type"],
            "type_distance": vocab["distance"],
            "coordinates": coords
        }, indent=2)


@mcp.tool(
    name="get_constellation_visual_types",
    annotations={
        "title": "List Visual Types and Keywords (Phase 2.7)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def get_constellation_visual_types() -> str:
    """
    List all constellation visual types with their coordinates and keywords.

    Layer 1: Pure taxonomy lookup (0 tokens).

    Returns the complete visual vocabulary catalog used by the attractor
    prompt generator. Each visual type represents a region of the 5D
    constellation parameter space with associated image-generation keywords.
    """
    types_info = {}
    for type_name, type_data in CONSTELLATION_VISUAL_TYPES.items():
        types_info[type_name] = {
            "coordinates": type_data["coords"],
            "keywords": type_data["keywords"],
            "keyword_count": len(type_data["keywords"])
        }

    return json.dumps({
        "visual_types": types_info,
        "count": len(types_info),
        "parameter_names": CONSTELLATION_PARAMETER_NAMES
    }, indent=2)


@mcp.tool(
    name="get_constellation_domain_registry_config",
    annotations={
        "title": "Get Tier 4D Domain Registry Configuration",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def get_constellation_domain_registry_config() -> str:
    """
    Return Tier 4D integration configuration for compositional limit cycles.

    Layer 2: Pure lookup (0 tokens).

    Returns the domain signature for registering with aesthetic-dynamics-core
    multi-domain composition. Includes domain_id, parameter names, preset
    periods, and canonical state coordinates — everything needed for
    integrate_forced_limit_cycle_multi_domain.
    """
    presets = {}
    for name, cfg in CONSTELLATION_RHYTHMIC_PRESETS.items():
        presets[name] = {
            "period": cfg["steps_per_cycle"],
            "pattern": cfg["pattern"],
            "state_a": cfg["state_a"],
            "state_b": cfg["state_b"],
            "trajectory": _generate_preset_trajectory(cfg)
        }

    state_coords = {}
    for sname in CONSTELLATION_CANONICAL_STATES:
        state_coords[sname] = _get_state_coordinates(sname)

    return json.dumps({
        "domain_id": "constellation",
        "display_name": "Constellation Composition",
        "mcp_server": "constellation_composition_mcp",
        "parameter_names": CONSTELLATION_PARAMETER_NAMES,
        "parameter_count": len(CONSTELLATION_PARAMETER_NAMES),
        "canonical_states": state_coords,
        "presets": presets,
        "all_periods": sorted(set(
            p["steps_per_cycle"] for p in CONSTELLATION_RHYTHMIC_PRESETS.values()
        )),
        "visual_types": list(CONSTELLATION_VISUAL_TYPES.keys()),
        "tier_4d_compatible": True
    }, indent=2)


# ============================================================================
# COORDINATE INFERENCE FOR NON-CANONICAL CONSTELLATIONS
# ============================================================================

def _infer_coordinates_from_metadata(meta: Dict[str, Any]) -> Dict[str, float]:
    """
    Infer approximate 5D coordinates from constellation metadata.

    Deterministic heuristic mapping for constellations without a dedicated
    canonical state. Uses brightness_profile, shape, star_count_visual,
    and theme keywords to estimate parameter values.
    """
    # stellar_density from star_count
    star_count = meta.get("star_count_visual", 5)
    stellar_density = min(1.0, star_count / 12.0)

    # geometric_regularity from shape
    shape = meta.get("shape", "")
    reg_map = {
        "cross": 0.9, "symmetric": 0.85, "square": 0.85, "w_zigzag": 0.8,
        "parallel": 0.75, "dipper": 0.7, "triangular": 0.7,
        "hourglass": 0.65, "v_shaped": 0.6, "sickle": 0.55,
        "compact": 0.5, "curved": 0.3, "dispersed": 0.2, "cascade": 0.15
    }
    geometric_regularity = 0.5
    for key, val in reg_map.items():
        if key in shape:
            geometric_regularity = val
            break

    # luminance_contrast from brightness_profile
    brightness = meta.get("brightness_profile", "moderate")
    bright_map = {
        "extremely_bright": 0.95, "very_bright_red": 0.85, "very_bright": 0.8,
        "multiple_bright": 0.8, "bright_cross": 0.7, "bright_square": 0.7,
        "bright_with_cluster": 0.7, "bright_pole_star": 0.75,
        "two_bright": 0.65, "bright": 0.6, "moderate_to_bright": 0.5,
        "moderate": 0.4, "faint": 0.15
    }
    luminance_contrast = 0.5
    for key, val in bright_map.items():
        if key in brightness:
            luminance_contrast = val
            break

    # narrative_intensity from theme keywords
    theme = meta.get("theme", "").lower()
    intensity_keywords = {
        "danger": 0.9, "death": 0.9, "revenge": 0.85, "punishment": 0.8,
        "power": 0.75, "hunting": 0.7, "courage": 0.7, "heroism": 0.7,
        "sacrifice": 0.65, "passion": 0.65, "rescue": 0.6,
        "transformation": 0.55, "duality": 0.5, "wisdom": 0.4,
        "guidance": 0.35, "music": 0.35, "innocence": 0.3,
        "flow": 0.25, "persistence": 0.2, "steadfastness": 0.2
    }
    narrative_intensity = 0.5
    for kw, val in intensity_keywords.items():
        if kw in theme:
            narrative_intensity = max(narrative_intensity, val)

    # spatial_extent from star_count + shape
    extent_base = min(1.0, star_count / 10.0) * 0.6
    if "large" in shape or "sprawl" in shape:
        extent_base = max(extent_base, 0.8)
    elif "compact" in shape or "small" in shape:
        extent_base = min(extent_base, 0.35)
    elif "dispersed" in shape or "cascade" in shape:
        extent_base = max(extent_base, 0.7)
    spatial_extent = min(1.0, extent_base + 0.15)

    return {
        "stellar_density": round(stellar_density, 2),
        "geometric_regularity": round(geometric_regularity, 2),
        "luminance_contrast": round(luminance_contrast, 2),
        "narrative_intensity": round(narrative_intensity, 2),
        "spatial_extent": round(spatial_extent, 2)
    }


# ============================================================================
# SERVER ENTRY POINT
# ============================================================================

def main():
    """Entry point for running the server."""
    mcp.run()


if __name__ == "__main__":
    main()
