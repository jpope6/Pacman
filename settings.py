import pygame as pg
import sys
from sound import Sound

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Settings:
    def __init__(self, game):
        self.game = game
        self.screen_width = 846
        self.screen_height = 937 + 50
        self.maze = pg.transform.scale(
            pg.image.load("./assets/images/pacman_map.jpg"),
            (self.screen_width, self.screen_height - 50),
        )
        self.pacman = None
        self.score = 0
        self.font = pg.font.Font(f"./assets/fonts/PressStart2P-Regular.ttf", 30)
        self.prep_score()
        self.sounds = Sound()
        self.sound_playing = False
        self.game_over_frame = 0

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.game.menu.PLAY_BUTTON.checkForInput(
                    self.game.menu.menu_mouse_pos
                ):
                    self.game.cur_menu = "game"

                if self.game.menu.HS_BUTTON.checkForInput(
                    self.game.menu.menu_mouse_pos
                ):
                    self.game.cur_menu = "hs"
                if self.game.menu.BACK_BUTTON.checkForInput(
                    self.game.menu.menu_mouse_pos
                ):
                    self.game.cur_menu = "menu"
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.pacman.target_direction = "UP"
                elif event.key == pg.K_DOWN:
                    self.pacman.target_direction = "DOWN"
                elif event.key == pg.K_LEFT:
                    self.pacman.target_direction = "LEFT"
                elif event.key == pg.K_RIGHT:
                    self.pacman.target_direction = "RIGHT"
                elif event.key == pg.K_z:
                    self.game.portals.createPortal1()
                elif event.key == pg.K_x:
                    self.game.portals.createPortal2()

    def prep_score(self):
        score_str = "Score:" + str(self.score)
        self.score_image = self.font.render(score_str, True, WHITE, BLACK)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = 10
        self.score_rect.top = self.screen_height - 40

    def draw(self, screen):
        screen.blit(self.score_image, self.score_rect)

    def reset(self, screen):
        self.score = 0
        self.sound_playing = False
        self.game_over_frame = 0
        self.prep_score()
        self.draw(screen)
