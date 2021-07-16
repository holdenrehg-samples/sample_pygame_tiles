import pygame
from pygrid_tiles.camera import Camera
from pygrid_tiles.grid import TileMap


class World:
    """
    Represents all of the elements in a world.

    A world may be the entire game, in the case of a small game, or
    it may be section. For example, it may make sense to segment
    each level or biome in a game into a World.

    The World object acts as the glue between the mapping and camera elements
    into a single interface.
    """

    def __init__(self, tile_map: TileMap):
        self.map = tile_map

    @property
    def size(self):
        return self.map.size_px

    def render(self, screen: pygame.Surface, camera: Camera):
        """Render this world to the screen."""
        for layer_level, layer in enumerate(self.map.layers.values()):
            for coordinates, tile_id in layer.items():
                if int(tile_id):
                    # pixel specific x, y
                    x = coordinates[0] * self.map.tile_size[0]
                    y = (coordinates[1] * self.map.tile_size[1]) + (layer_level * self.map.tile_size[1])

                    # tranformed x, y to account for isometric shape
                    render_x = (x - y) / 2
                    render_y = (x + y) / 4

                    if camera.in_focus((render_x, render_y)):
                        screen.blit(
                            self.map.tile_set[int(tile_id)],
                            (
                                render_x - camera.position[0],
                                render_y - camera.position[1],
                            ),
                        )
