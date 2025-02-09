# map-related functions

from typing import List
import pandas as pd
import pygame

from parameters import X_RES, Y_RES, TILE_X_SIZE, TILE_Y_SIZE

image_tile_path = "images/tiles/"
image_tile_format = ".bmp"
map_df = pd.read_csv("data/maps/0_tiles.csv", index_col=0, sep=";")


class Map:
    def __init__(self):
        self.tiles: pd.DataFrame = pd.DataFrame()
        self.tile_x_size = TILE_X_SIZE
        self.tile_y_size = TILE_Y_SIZE
        self.map_size_x = 0
        self.map_size_y = 0
        self.x_shift = 0
        self.y_shift = 0

    def load_map(self, map_path: str) -> List[List[str]]:
        """Loading a map from the given map path."""
        map_loaded = []
        with open(map_path) as f:
            s = f.read().replace(" ", "")
            map_rows = s.split("\n")
            map_loaded = [row.split(",") for row in map_rows]
        return map_loaded

    def prepare_map(self, map_path: str):
        """Preparing the map."""
        map_loaded = self.load_map(map_path)
        self.map_size_y = len(map_loaded)
        self.map_size_x = len(map_loaded[0]) if map_loaded else 0
        self.update_shift()
        tiles = []
        for y, row in enumerate(map_loaded):
            for x, tile_type in enumerate(row):
                tiles.append(
                    [
                        x,
                        y,
                        tile_type,
                        map_df.loc[tile_type, "selectable"],
                        map_df.loc[tile_type, "walkable"],
                    ]
                )
        self.tiles = pd.DataFrame(
            tiles, columns=["x", "y", "tile_type", "selectable", "walkable"]
        )
        self.tiles.set_index(["x", "y"], inplace=True)

    def update_tile_size(self, tile_x_size: int, tile_y_size: int):
        """Updating tile sizes."""
        self.tile_x_size = tile_x_size
        self.tile_y_size = tile_y_size

    def update_shift(
        self,
        player_x: int | None = None,
        player_y: int | None = None,
        centered_on_player: bool = False,
    ):
        """Updating shift level to keep player on map."""
        # center map if screen is larger than map
        if X_RES >= self.map_size_x * self.tile_x_size:
            self.x_shift = (X_RES - self.map_size_x * self.tile_x_size) / 2

        # keep player always on screen
        elif player_x is not None:
            # keep player in screen if player scrolls over displayed map
            if not centered_on_player:
                if player_x * self.tile_x_size + self.x_shift < 0:
                    self.x_shift = -player_x * self.tile_x_size
                elif (
                    player_x * self.tile_x_size + self.x_shift + self.tile_x_size
                    > X_RES
                ):
                    self.x_shift = (
                        -player_x * self.tile_x_size + X_RES - self.tile_x_size
                    )
            # keep player in the middle of the screen
            else:
                self.x_shift = (
                    -player_x * self.tile_x_size + (X_RES - self.tile_x_size) / 2
                )
            self.x_shift = max(
                min(0, self.x_shift), -self.map_size_x * self.tile_x_size + X_RES
            )

        # center map if screen is larger than map
        if Y_RES >= self.map_size_y * self.tile_y_size:
            self.y_shift = (Y_RES - self.map_size_y * self.tile_y_size) / 2

        # keep player always on screen
        elif player_y is not None:
            # keep player in screen if player scrolls over displayed map
            if not centered_on_player:
                if player_y * self.tile_y_size + self.y_shift <= 0:
                    self.y_shift = -player_y * self.tile_y_size
                elif (
                    player_y * self.tile_y_size + self.y_shift + self.tile_y_size
                    > Y_RES
                ):
                    self.y_shift = (
                        -player_y * self.tile_y_size + Y_RES - self.tile_y_size
                    )
            # keep player in the middle of the screen
            else:
                self.y_shift = (
                    -player_y * self.tile_y_size + (Y_RES - self.tile_y_size) / 2
                )
            self.y_shift = max(
                min(0, self.y_shift), -self.map_size_y * self.tile_y_size + Y_RES
            )

    def pygame_display_map(self, screen: pygame.Surface):
        """Displaying a map on the pygame screen."""
        tile_dict = {}
        for idx, row in self.tiles.iterrows():
            if row["tile_type"] not in tile_dict:
                # only load the images we need for each frame
                tile_dict[row["tile_type"]] = pygame.image.load(
                    image_tile_path
                    + map_df.loc[row["tile_type"], "name"]
                    + image_tile_format
                ).convert()
                tile_dict[row["tile_type"]] = pygame.transform.scale(
                    surface=tile_dict[row["tile_type"]],
                    size=(self.tile_x_size, self.tile_y_size),
                )
            x, y = idx
            x_pos = x * self.tile_x_size + self.x_shift
            y_pos = y * self.tile_y_size + self.y_shift
            screen.blit(tile_dict[row["tile_type"]], (x_pos, y_pos))
