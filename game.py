import pygame as pg
from settings import *
from graph import Graph
from pacman import Pacman
from pellet import *


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.size = self.settings.screen_width, self.settings.screen_height
        self.screen = pg.display.set_mode(size=self.size)
        pg.display.set_caption("Pacman")

        self.graph = Graph(self.screen)
        self.pacman = Pacman(self.screen, self.graph)
        self.settings.pacman = self.pacman

        self.pellets = Pellets(self.graph, self.screen)

    def play(self):
        while True:
            self.settings.check_events()
            pg.Surface.blit(self.screen, self.settings.maze, (0, 0))

            self.graph.draw()
            # self.graph.draw_edge()
            self.pellets.pelletEaten(self.pacman)
            self.pellets.drawPellets()
            self.pacman.draw()
            self.pacman.move()

            # pg.draw.circle(self.screen, WHITE, (475, 165), 20)

            pg.display.update()


def main():
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
