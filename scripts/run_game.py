# script to run the game

import pygame
import parameters
from asthetics.map import Map
from control.player import Player
from control.shortcuts import Shortcuts

# pygame setup
pygame.init()
screen = pygame.display.set_mode((parameters.X_RES, parameters.Y_RES))
clock = pygame.time.Clock()
running = True
dt = 0

cursor_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Test Map
test_map = Map()
test_map.prepare_map("data/maps/touch_grass.txt")
player = Player(0, 0, "cursor", test_map)
shortcuts = Shortcuts()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((0, 0, 0))

    test_map.pygame_display_map(screen)
    player.pygame_control_player(screen=screen)
    shortcuts.pygame_shortcuts(screen=screen, map=test_map, player=player)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
