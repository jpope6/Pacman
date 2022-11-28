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
        self.pacman = Pacman(self.screen, self.graph, self.settings)
        self.settings.pacman = self.pacman
        self.portals = Portal(self.pacman)

        self.pellets = Pellets(self.graph, self.screen, self.settings)
        self.fruit = Fruit(self.settings)
        self.settings.fruit = self.fruit

        self.blinky = Blinky(self.screen, self.graph, self.settings, self.pacman)
        self.pinky = Pinky(self.screen, self.graph, self.settings, self.pacman)
        self.inkey = Inkey(self.screen, self.graph, self.settings, self.pacman)
        self.clyde = Clyde(self.screen, self.graph, self.settings, self.pacman)

        self.settings.ghosts = [self.blinky, self.pinky, self.inkey, self.clyde]
        self.settings.pellets = self.pellets

        self.menu = Menu(self)
        self.playable = False

        self.game_over = False
        self.won = False
        self.game_over_frame = 0
        self.won_frame = 0

        self.settings.frame_count = 0

    def fullReset(self):
        for ghost in self.settings.ghosts:
            ghost.reset()

        self.menu.check_for_high_score()
        self.pacman.reset()
        self.pellets.reset()
        self.settings.reset(self.screen)
        self.pacman.lives = 3
        self.game_over = False
        self.settings.frame_count = 0
        self.fruit.reset()

    def play(self):
        while True:
            self.screen.fill(BLACK)
            self.settings.check_events()
            if self.cur_menu == "menu":
                self.menu.menu()

            if self.cur_menu == "hs":
                self.menu.highscores()

            if self.cur_menu == "game":
                cur_frame = 0
                if not self.settings.sound_playing:
                    self.settings.sounds.play_startup()
                    cur_frame = self.settings.frame_count
                    self.settings.sound_playing = True

                if cur_frame + 2000 == self.settings.frame_count:
                    self.playable = True
                    self.blinky.direction = "LEFT"

                pg.Surface.blit(self.screen, self.settings.maze, (0, 0))

                self.graph.draw()
                self.graph.draw_edge()
                self.pellets.drawPellets(self.pacman)

                if len(self.pellets.pellet_list) == 0 and not self.won:
                    self.playable = False
                    self.won_frame = self.settings.frame_count
                    self.won = True

                # self.pinky.draw(self.settings.frame_count)
                # self.inkey.draw(self.settings.frame_count)
                # self.clyde.draw(self.settings.frame_count)

                for ghost in self.settings.ghosts:
                    if ghost.dead:
                        ghost.drawDead(self.settings.frame_count)
                    else:
                        ghost.incrementScore()
                        ghost.draw(self.settings.frame_count)

                if self.playable:
                    self.pacman.move()
                    # self.blinky.moveAround()
                    self.blinky.search(self.settings.frame_count)
                    self.blinky.canChangeDirection(self.settings.frame_count)
                    self.blinky.move(self.settings.frame_count)
                    self.blinky.teleport_node()
                    self.pinky.moveAround()
                    self.pinky.move(self.settings.frame_count)
                    self.inkey.moveAround()
                    self.inkey.move(self.settings.frame_count)
                    self.clyde.moveAround()
                    self.clyde.move(self.settings.frame_count)
                    self.portals.drawPortal(self.screen, self.settings.frame_count)
                    self.fruit.draw(self.screen, self.settings.frame_count)

                if self.game_over:
                    text = self.settings.font.render("GAME OVER", True, (255, 255, 255))
                    text_rec = text.get_rect(
                        center=(self.settings.screen_width / 2, 530)
                    )
                    self.screen.blit(text, text_rec)

                if self.won:
                    text = self.settings.font.render("YOU WIN", True, (255, 255, 255))
                    text_rec = text.get_rect(
                        center=(self.settings.screen_width / 2, 530)
                    )
                    self.screen.blit(text, text_rec)

                    if self.won_frame + 800 == self.settings.frame_count:
                        self.fullReset()
                        self.cur_menu = "menu"
                        self.won = False

                self.pacman.draw()
                self.pacman.drawLives(self.settings.frame_count)
                self.settings.draw(self.screen)

                # pg.draw.circle(self.screen, WHITE, (475, 165), 20)
            self.settings.frame_count += 1
            pg.display.update()


def main():
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
