# keyboard shortcuts and options

import pygame
from asthetics.map import Map
from control.player import Player

ZOOM_LEVEL_MIN = 0
ZOOM_LEVEL_MAX = 9


class Shortcuts:
    def __init__(self):
        self.zoom_level = 4
        self.hold_plus = 0
        self.hold_minus = 0

    def pygame_shortcuts(
        self, screen: pygame.Surface, map: Map, player: Player | None = None
    ):
        """Shortcuts and controls for the game."""
        keys = pygame.key.get_pressed()

        # zooming in or out
        self.hold_plus = self.change_zoom(
            map=map,
            player=player,
            zoom_change=1,
            key_pressed=(keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]),
            hold_button=self.hold_plus,
        )
        self.hold_minus = self.change_zoom(
            map=map,
            player=player,
            zoom_change=-1,
            key_pressed=(keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]),
            hold_button=self.hold_minus,
        )

    def change_zoom(
        self,
        map: Map,
        player: Player | None,
        zoom_change: int,
        key_pressed: bool,
        hold_button: int,
    ) -> int:
        """Changing zoom level on map."""
        if key_pressed:
            if hold_button == 0 or (hold_button >= 30 and hold_button % 6 == 0):
                self.zoom_level = min(
                    max(ZOOM_LEVEL_MIN, self.zoom_level + zoom_change), ZOOM_LEVEL_MAX
                )
                self.update_map_tile_size(map=map, player=player)
            return hold_button + 1
        return 0

    def update_map_tile_size(self, map: Map, player: Player | None):
        """Updating size tile on map, zooming in or out."""
        new_tile_size = (self.zoom_level + 1) * 16
        map.update_tile_size(tile_x_size=new_tile_size, tile_y_size=new_tile_size)
        map.update_shift(
            player_x=player.x if player else None,
            player_y=player.y if player else None,
            centered_on_player=True,
        )
