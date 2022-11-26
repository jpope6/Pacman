from settings import *
from timer import Timer


class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.menu_running = True
        self.menu_mouse_pos = (0, 0)

        self.menu_images = [
            pg.transform.rotozoom(
                pg.image.load(f"assets/images/menu_animation/menu_animation{n}.png"),
                0,
                4,
            )
            for n in range(93)
        ]
        self.menu_timer = Timer(self.menu_images)

        self.PLAY_BUTTON = Button(
            image=None,
            pos=(425, 710),
            text_input="Play",
            font=pg.font.Font(f"./assets/fonts/PressStart2P-Regular.ttf", 50),
            base_color="Blue",
            hovering_color="White",
        )

        self.HS_BUTTON = Button(
            image=None,
            pos=(425, 810),
            text_input="High Scores",
            font=pg.font.Font(f"./assets/fonts/PressStart2P-Regular.ttf", 40),
            base_color="Blue",
            hovering_color="White",
        )

        self.BACK_BUTTON = Button(
            image=None,
            pos=(50, 25),
            text_input="Back",
            font=pg.font.Font(f"./assets/fonts/PAC-FONT.ttf", 25),
            base_color="Red",
            hovering_color="White",
        )

    def menu(self):
        self.menu_mouse_pos = pg.mouse.get_pos()
        pac = "PACMAN!"
        color = (255, 255, 0)
        text = pg.font.Font("./assets/fonts/PAC-FONT.ttf", 100).render(pac, True, color)
        text_rec = text.get_rect(center=(425, 100))
        self.screen.blit(text, text_rec)
        pac2 = "999912"
        color2 = (255, 255, 0)
        text2 = pg.font.Font("./assets/fonts/PAC-FONT.ttf", 100).render(
            pac2, True, color2
        )
        text2_rec = text2.get_rect(center=(425, 250))
        self.screen.blit(text2, text2_rec)
        # animation
        self.draw_animation()
        # when mouse is hovering over the play button update it
        for button in [self.PLAY_BUTTON]:
            button.changeColor(self.menu_mouse_pos)
            button.update(screen=self.screen)
        for button in [self.HS_BUTTON]:
            button.changeColor(self.menu_mouse_pos)
            button.update(screen=self.screen)

    def draw_animation(self):
        image = self.menu_timer.image()
        rect = image.get_rect()
        rect.left = 0
        rect.top = 425
        self.screen.blit(image, rect)

    def highscores(self):
        self.screen.fill("black")

        self.menu_mouse_pos = pg.mouse.get_pos()
        hs = "High Scores"
        color = (255, 255, 255)
        text = pg.font.Font(f"./assets/fonts/PressStart2P-Regular.ttf", 30).render(
            hs, True, color
        )
        text_rec = text.get_rect(center=(225, 75))
        self.screen.blit(text, text_rec)
        color1 = "White"
        count = 0
        file = open("highscores.txt")
        line = file.readline
        for line in file:
            text1 = pg.font.Font(f"./assets/fonts/PressStart2P-Regular.ttf", 30).render(
                line, True, color1
            )
            text1_rec = text1.get_rect(center=(225, 150 + 50 * count))
            self.screen.blit(text1, text1_rec)
            count += 1
        file.close()

        for button in [self.BACK_BUTTON]:
            button.changeColor(self.menu_mouse_pos)
            button.update(screen=self.screen)
