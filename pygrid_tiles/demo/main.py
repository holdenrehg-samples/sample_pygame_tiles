import pygame
import pygame.display
import pygame.event
import pygame.font
import pygame.image
import pygame.key
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
        world = World(imports.from_tiled(map_file, base_dir=ASSETS_PATH))

    # Run the game...
    # ---------------

    running = True

    try:
        while running:
            screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Handle user input...
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_LEFT]:
                camera.position[0] = camera.position[0] - camera_momentum
            if pressed_keys[pygame.K_UP]:
                camera.position[1] = camera.position[1] - camera_momentum
            if pressed_keys[pygame.K_RIGHT]:
                camera.position[0] = camera.position[0] + camera_momentum
            if pressed_keys[pygame.K_DOWN]:
                camera.position[1] = camera.position[1] + camera_momentum

            # Render the tile map world...
            world.render(screen, camera)

            # Display some reference to current camera coordinates...
            font = pygame.font.SysFont(None, 36)
            text = font.render(f"({camera.position[0]}, {camera.position[1]})", False, (255, 255, 255))
            screen.blit(text, (camera.size[0] - text.get_rect().width - 10, 10))

            pygame.display.flip()
    except pygame.error:
        pass
    finally:
        pygame.quit()
        raise SystemExit


main()
