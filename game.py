import pygame as pg
from settings import *
from graph import Graph
from pacman import Pacman
from pellet import *
from ghost import *
from menu import *
from portal import Portal


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings(self)
        self.size = self.settings.screen_width, self.settings.screen_height
        self.screen = pg.display.set_mode(size=self.size)
        pg.display.set_caption("Pacman")
        self.cur_menu = "menu"

        self.graph = Graph(self.screen)
        self.pacman = Pacman(self.screen, self.graph)
        self.settings.pacman = self.pacman
        self.portals = Portal(self.pacman)

        self.pellets = Pellets(self.graph, self.screen, self.settings)

        self.blinky = Blinky(self.screen, self.graph, self.pacman)
        self.pinky = Pinky(self.screen, self.graph, self.settings)
        self.inkey = Inkey(self.screen, self.graph, self.settings)
        self.clyde = Clyde(self.screen, self.graph, self.settings)

        self.settings.ghosts = [self.blinky, self.pinky, self.inkey, self.clyde]
        self.settings.pellets = self.pellets

        self.menu = Menu(self)

        self.settings.frame_count = 0

    def play(self):
        while True:
            self.screen.fill(BLACK)
            self.settings.check_events()
            if self.cur_menu == "menu":
                self.menu.menu()

            if self.cur_menu == "hs":
                self.menu.highscores()

            if self.cur_menu == "game":
                pg.Surface.blit(self.screen, self.settings.maze, (0, 0))

                self.graph.draw()
                # self.graph.draw_edge()
                self.pellets.drawPellets(self.pacman)
                # self.blinky.draw()
                self.pinky.draw(self.settings.frame_count)
                self.inkey.draw(self.settings.frame_count)
                self.clyde.draw(self.settings.frame_count)
                self.pacman.move()
                # self.blinky.moveAround()
                # self.blinky.move()
                self.pinky.moveAround()
                self.pinky.move()
                self.inkey.moveAround()
                self.inkey.move()
                self.clyde.moveAround()
                self.clyde.move()
                self.portals.drawPortal(self.screen, self.settings.frame_count)
                self.pacman.draw()
                self.settings.draw(self.screen)

                # pg.draw.circle(self.screen, WHITE, (475, 165), 20)

            self.settings.frame_count += 1
            pg.display.update()


def main():
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
