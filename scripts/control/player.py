# player control options

import pygame
from asthetics.map import Map

image_tile_path = "images/figures/"
image_tile_format = ".bmp"


class Player:
    def __init__(self, x: int, y: int, image: str, map: Map):
        self.x = x
        self.y = y
        self.image = image
        self.map = map
        self.hold_up = 0
        self.hold_down = 0
        self.hold_left = 0
        self.hold_right = 0

    def pygame_control_player(self, screen: pygame.Surface):
        """Basic player controls."""
        # render player icon or cursor
        player = pygame.image.load(
            image_tile_path + self.image + image_tile_format
        ).convert()
        player = pygame.transform.scale(
            surface=player, size=(self.map.tile_x_size, self.map.tile_y_size)
        )
        x_pos = self.x * self.map.tile_x_size + self.map.x_shift
        y_pos = self.y * self.map.tile_y_size + self.map.y_shift
        screen.blit(player, (x_pos, y_pos))

        keys = pygame.key.get_pressed()

        # movement in up / down / left / right direction
        self.hold_up = self.handle_movement(
            key_pressed=keys[pygame.K_UP],
            x_dir_tiles=0,
            y_dir_tiles=-1,
            hold_button=self.hold_up,
        )
        self.hold_down = self.handle_movement(
            key_pressed=keys[pygame.K_DOWN],
            x_dir_tiles=0,
            y_dir_tiles=1,
            hold_button=self.hold_down,
        )
        self.hold_left = self.handle_movement(
            key_pressed=keys[pygame.K_LEFT],
            x_dir_tiles=-1,
            y_dir_tiles=0,
            hold_button=self.hold_left,
        )
        self.hold_right = self.handle_movement(
            key_pressed=keys[pygame.K_RIGHT],
            x_dir_tiles=1,
            y_dir_tiles=0,
            hold_button=self.hold_right,
        )

    def handle_movement(
        self, key_pressed: bool, x_dir_tiles: int, y_dir_tiles: int, hold_button: int
    ) -> int:
        """Handling player movement."""
        if key_pressed:
            self.player_tile_movement(
                x_dir_tiles=x_dir_tiles,
                y_dir_tiles=y_dir_tiles,
                hold_button=hold_button,
            )
            return hold_button + 1
        return 0

    def player_tile_movement(
        self, x_dir_tiles: int, y_dir_tiles: int, hold_button: int
    ):
        """Letting player move to the desired tile if allowed."""
        if hold_button == 0 or (hold_button >= 30 and hold_button % 3 == 0):
            x_target = min(max(0, self.x + x_dir_tiles), self.map.map_size_x - 1)
            y_target = min(max(0, self.y + y_dir_tiles), self.map.map_size_y - 1)
            row = self.map.tiles.loc[(x_target, y_target)]
            if not row.empty and row["selectable"]:
                self.x = x_target
                self.y = y_target
            self.map.update_shift(player_x=self.x, player_y=self.y)
