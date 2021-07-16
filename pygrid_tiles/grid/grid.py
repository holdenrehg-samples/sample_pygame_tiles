from dataclasses import dataclass
from typing import Dict, List

from .layer import Layer
from .tile import TileType


@dataclass
class Grid:
    tileset: Dict[int, TileType]
    layers: List[Layer]
