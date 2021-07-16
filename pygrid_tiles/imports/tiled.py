import csv
import io
from typing import Dict
from xml.etree import ElementTree

import pygame
from pygrid_tiles import utils, TileMap


def from_tiled(map_file, base_dir: str):
    """Import a .tmx map file exported from Tiled."""

    map_tree = ElementTree.fromstring(map_file.read())
    tile_set = _parse_tileset(map_tree, base_dir)

    return TileMap(
        size=(map_tree.attrib["width"], map_tree.attrib["height"]),
        tile_size=(map_tree.attrib["tilewidth"], map_tree.attrib["tileheight"]),
        layers=_parse_layers(tile_set, map_tree),
        tile_set=tile_set,
    )


def _parse_tileset(map_tree: ElementTree, base_dir: str):
    tileset = {}
    tileset_source = map_tree.find("tileset").attrib["source"]

    with open(f"{base_dir}/{tileset_source}") as tileset_file:
        tileset_tree = ElementTree.fromstring(tileset_file.read())

        spritesheet_size = (
            int(int(tileset_tree.attrib["tilecount"]) / int(tileset_tree.attrib["columns"])),
            int(tileset_tree.attrib["columns"]),
        )
        sprite_size = (
            int(tileset_tree.attrib["tilewidth"]),
            int(tileset_tree.attrib["tileheight"]),
        )
        spritesheet_source = tileset_tree.find("image").attrib["source"]
        spritesheet = pygame.image.load(f"{base_dir}/{spritesheet_source}").convert_alpha()

        tile_id = 1
        for y in range(0, spritesheet_size[1]):
            for x in range(0, spritesheet_size[0]):
                rect = pygame.Rect(
                    (
                        x * sprite_size[0],
                        y * sprite_size[1],
                        sprite_size[0],
                        sprite_size[1],
                    )
                )
                image = pygame.Surface(rect.size)
                image.blit(spritesheet, (0, 0), rect)
                image.set_colorkey(0, pygame.RLEACCEL)
                tileset[tile_id] = image
                tile_id += 1

    return tileset


def _parse_layers(tileset: Dict, map_tree: ElementTree):
    layers = {}

    for layer_tree in map_tree.findall("layer"):
        layer = {}
        layer_level = layer_tree.attrib["id"]

        x_offset = 0
        y_offset = 0

        for chunk_tree in layer_tree.find("data").findall("chunk"):
            for y, row in enumerate(filter(None, csv.reader(io.StringIO(chunk_tree.text.strip())))):
                for x, tile_id in enumerate(filter(None, row)):
                    # Theres scenarios where some rows use tailing commas and
                    # other don't, leading to empty tile_id, we can just ignore
                    # those.
                    if not tile_id:
                        continue

                    position = (
                        x + int(chunk_tree.attrib["x"]),
                        y + int(chunk_tree.attrib["y"]),
                    )
                    if position in layer:
                        raise Exception(f"Conflicting tile position {position}, tile={tile_id}")
                    layer[position] = tile_id

                    x_offset = min(x_offset, position[0])
                    y_offset = min(y_offset, position[1])

        layers[layer_level] = {
            (position[0] + abs(x_offset), position[1] + abs(y_offset)): tile_id
            for position, tile_id in layer.items()
        }

    return layers
