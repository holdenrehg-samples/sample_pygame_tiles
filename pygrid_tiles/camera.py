from typing import List, Tuple

from pygrid_tiles.grid import Grid


class Camera:
    """
    The cross section of the map that is currently visible to the user.

    For example, you can imagine a structure below where the map in a multi
    dimensional array of tile and the camera renders a subsection of that
    overall map to the user. If this was a platformer and x represents the
    player then as they move left or right the camera shifts and renders a
    new section of the overall map.

        map
        |-----------------------|
        |                       |
        |      camera           |
        |      |--------|       |
        |      |        |       |
        |      |   x    |       |
        |      |        |       |
        |      |--------|       |
        |                       |
        |                       |
        |-----------------------|
    """

    def __init__(self, position: List[int], size: List[int]):
        self.position = position
        self.size = size
        self.buffer = 100

    def in_focus(self, coordinate: Tuple[int]):
        """Check if a given element is in focus of the camera."""

        left_bound = self.position[0]
        top_bound = self.position[1]
        right_bound = self.position[0] + self.size[0]
        bottom_bound = self.position[1] + self.size[1]

        return (
            coordinate[0] >= left_bound - self.buffer
            and coordinate[0] <= right_bound + self.buffer
            and coordinate[1] >= top_bound - self.buffer
            and coordinate[1] <= bottom_bound + self.buffer
        )
