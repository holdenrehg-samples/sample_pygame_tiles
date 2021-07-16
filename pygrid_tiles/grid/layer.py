from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

from .point import Point
from .tile import Tile


@dataclass
class Layer:
    id: int
    tiles: List[List[Tile]]
    coordinate_map: Optional[Dict[Point, Tile]] = None

    def __post_init__(self):
        self.initialize_coordinate_map()

    def initialize_coordinate_map(self):
        """Generate a map of cartesian coordinate points to tiles from the `tiles` 2d array."""
        self.coordinate_map = {}
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                self.coordinate_map[Point(x, y)] = tile

    def find(self, point: Union[Tuple[int], Point]):
        point = Point.parse(point)
        if point not in self.coordinate_map:
            raise Exception(f"Cannot find point {point} in layer {self.id}.")
        return self.coordinate_map[point]
