## pygame_tiles

Experimenting with a scrolling tile system implementation in pygame. This demo loads in a sample tilemap created in [Tiled](https://www.mapeditor.org/).

![screenshot](https://github.com/holdenrehg-samples/sample_pygame_tiles/blob/main/assets/screenshot.png?raw=true)

### Requirements

I developed this using python `3.8.10` and [Pipenv](https://pipenv.pypa.io/en/latest/).

### Setting up

**Create the virtual environment.**

```shell
$ python3 -m venv venv
```

**Initialize the virtual environment.**

```shell
$ source venv/bin/activate
```

**Install pip dependencies.**

```shell
(venv) $ pipenv install
```

### Running a demo

```shell
(venv) $ python pygrid_tiles/demo/main.py
```

Once running, use the arrow keys to navigate around the map. You will see coordinates of the camera position in the top right corner of the screen.

### How's it work?

The gist of the demo is loading in the Tiled files and passing those to a `World` class which handles rendering of the tilemap.

```python
import pygame
from pygrid_tiles import imports
from pygrid_tiles.camera import Camera
from pygrid_tiles.world import World

ASSETS_PATH = "pygrid_tiles/demo"
TILESET_PATH = f"{ASSETS_PATH}/ocean-tileset.tsx"
TILEMAP_PATH = f"{ASSETS_PATH}/ocean.tmx"


def main():
    pygame.init()
    pygame.display.init()

    screen_w, screen_h = 1280, 960
    screen = pygame.display.set_mode((screen_w, screen_h))
    camera = Camera([0, 0], [screen_w, screen_h])
    camera_momentum = 6

    # Generate the game world...
    # --------------------------

    world = None
    with open(TILEMAP_PATH) as map_file:
        world = World(
            imports.from_tiled(
                map_file,
                base_dir=ASSETS_PATH
            )
        )

    # Run the game...
    # ---------------

    running = True

    try:
        while running:

            ...

            world.render(screen, camera)

    except pygame.error:
        pass

    finally:
        pygame.quit()
        raise SystemExit
```

---

**`pygrid_tiles.Camera`**

```python
class Camera:
    def __init__(position: List[int], size: List[int]): ...
    def in_focus(coordinate: Tuple[int]) -> bool: ...
```

Represents what is "in view" when running the game. It's a subsection of the entire map or world. Contains a position coordinate and size.

By using the posiion and size, we can create rectangular bounds for the camera and check if any given coordinate or tile is within bounds of the camera. This speeds up rendering significantly when dealing with large maps.

**`pygrid_tiles.World`**

```python
class World:
    def __init__(tile_map: pygrid_tiles.TileMap): ...
    def render(screen: pygame.Surface, camera: pygrid_tiles.Camera): ...
```

Handles storing and rendering the TileMap. This is essentially the glue between our camera and our map.

**`pygrid_tiles.TileMap`**

```python
class TileMap:
    def __init__(
        size: Tuple[int],
        tile_size: Tuple[int],
        layers: Dict={},
        tile_set: Dict={}
    ): ...
```

Stores all of the data that's extracted from the Tiled exports includes each layer, the tileset reference, and size dimensions.

**`pygrid_tiles.imports.from_tiled(map_file, base_dir) -> pygrid_tiles.grid.TileMap`**

Handles loading in the map from the Tiled exports into a `TileMap` object. The Tiled export consists of a `.tmx` map file which all of the layers and layout of tiles, a `.tsx` file which defines the tileset, and a spritesheet `.png` which the actual individual tile assets.
