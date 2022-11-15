import pygame as pg
import sys

WHITE = (255, 255, 255)


class Settings:
    def __init__(self):
        self.screen_width = 846
        self.screen_height = 937
        self.maze = pg.transform.scale(
            pg.image.load("./assets/pacman_map.jpg"),
            (self.screen_width, self.screen_height),
        )
        self.pacman = None

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.pacman.target_direction = "UP"
                elif event.key == pg.K_DOWN:
                    self.pacman.target_direction = "DOWN"
                elif event.key == pg.K_LEFT:
                    self.pacman.target_direction = "LEFT"
                elif event.key == pg.K_RIGHT:
                    self.pacman.target_direction = "RIGHT"
