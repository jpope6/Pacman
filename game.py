import pygame as pg
from settings import *


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.size = self.settings.screen_width, self.settings.screen_height
        self.screen = pg.display.set_mode(size=self.size)
        pg.display.set_caption("Pacman")

    def play(self):
        while True:
            self.settings.check_events()
            pg.Surface.blit(self.screen, self.settings.maze, (0, 0))

            pg.draw.circle(self.screen, WHITE, (200, 170), 20)

            pg.display.update()


def main():
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
