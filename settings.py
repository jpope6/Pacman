import pygame as pg
import sys


class Settings:
    def __init__(self):
        self.screen_width = 846
        self.screen_height = 937
        self.maze = pg.transform.scale(
            pg.image.load("./assets/pacman_map.jpg"),
            (self.screen_width, self.screen_height),
        )

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
