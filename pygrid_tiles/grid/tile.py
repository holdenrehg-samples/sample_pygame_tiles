from dataclasses import dataclass
from typing import Tuple


@dataclass
class TileType:
    id: int
    width: int
    height: int
    image: int


@dataclass
class Tile:
    type: int  # TileType.id


class TileMap:
    def __init__(self, size: Tuple[int], tile_size: Tuple[int], layers={}, tile_set={}):
        self.layers = layers
        self.tile_set = tile_set
        self.size = (
            int(size[0]),
            int(size[1]),
        )  # px
        self.tile_size = (
            int(tile_size[0]),
            int(tile_size[1]),
        )

    @property
    def size_px(self):
        return (self.size[0] * self.tile_size[0], self.size[1] * self.tile_size[1])
