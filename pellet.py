import pygame as pg
from settings import *
from timer import *
import random


class Pellet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = 10
        self.color = WHITE
        self.radius = 5

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Pellets:
    def __init__(self, graph, screen, settings):
        self.graph = graph
        self.settings = settings
        self.pellet_list = []
        self.node_x_done = []
        self.node_y_done = []
        self.x_list = [50, 475, 200, 287, 650, 745]
        self.y_list = [50, 165, 620, 710, 800]
        self.bigPelletList = [(50, 108), (800, 108), (50, 710), (800, 710)]
        self.screen = screen
        self.addPelletToList()
        self.dyingSound = False

    def pelletEaten(self, pacman, pellet):
        if (
            pellet.x > pacman.x - pacman.radius and pellet.x < pacman.x + pacman.radius
        ) and (
            pellet.y > pacman.y - pacman.radius and pellet.y < pacman.y + pacman.radius
        ):
            if (pellet.x, pellet.y) in self.bigPelletList:
                self.settings.sounds.play_power_up()
                self.dyingSound = True
                for ghost in self.settings.ghosts:
                    ghost.dying = True
                    ghost.dying_time = self.settings.frame_count

            self.pellet_list.remove(pellet)
            self.settings.score += pellet.points
            pacman.score_from_death += pellet.points
            self.settings.prep_score()

            if not self.dyingSound:
                self.settings.sounds.play_waka()

    def addPelletToList(self):
        for node in self.graph.nodes:
            if node.x in self.x_list:
                end = node
                while end.neighbors["RIGHT"] and end not in self.node_x_done:
                    if end.x == 287 and end.y == 350 or end.x == 287 and end.y == 530:
                        break

                    if end.x == 200 and end.y == 435 or end.x == 650 and end.y == 435:
                        break

                    if end.x == 475 and end.y == 350:
                        break

                    self.node_x_done.append(end)
                    end = end.neighbors["RIGHT"]

                    if end.x == 375 and end.y == 710:
                        break

                x = node.x + 28
                y = node.y

                while x < end.x - 26:
                    self.pellet_list.append(Pellet(x, y))
                    x += 30

            if node.y in self.y_list:
                end = node
                while end.neighbors["DOWN"] and end not in self.node_y_done:
                    self.node_y_done.append(end)
                    end = end.neighbors["DOWN"]

                x = node.x
                y = node.y + 28

                while y < end.y - 26:
                    self.pellet_list.append(Pellet(x, y))
                    y += 30

        # special case pellets
        self.pellet_list.append(Pellet(50, 50))
        self.pellet_list.append(Pellet(800, 50))
        self.pellet_list.append(Pellet(50, 255))
        self.pellet_list.append(Pellet(800, 255))
        self.pellet_list.append(Pellet(287, 255))
        self.pellet_list.append(Pellet(375, 255))
        self.pellet_list.append(Pellet(475, 255))
        self.pellet_list.append(Pellet(562, 255))
        self.pellet_list.append(Pellet(375, 50))
        self.pellet_list.append(Pellet(475, 50))
        self.pellet_list.append(Pellet(50, 620))
        self.pellet_list.append(Pellet(800, 620))
        self.pellet_list.append(Pellet(287, 620))
        self.pellet_list.append(Pellet(375, 620))
        self.pellet_list.append(Pellet(475, 620))
        self.pellet_list.append(Pellet(375, 710))
        self.pellet_list.append(Pellet(475, 710))
        self.pellet_list.append(Pellet(105, 710))
        self.pellet_list.append(Pellet(745, 710))
        self.pellet_list.append(Pellet(50, 800))
        self.pellet_list.append(Pellet(200, 800))
        self.pellet_list.append(Pellet(287, 800))
        self.pellet_list.append(Pellet(375, 800))
        self.pellet_list.append(Pellet(475, 800))
        self.pellet_list.append(Pellet(567, 800))
        self.pellet_list.append(Pellet(650, 800))
        self.pellet_list.append(Pellet(50, 890))
        self.pellet_list.append(Pellet(800, 890))
        self.pellet_list.append(Pellet(800, 800))

        self.pellet_list.append(BigPellet(50, 108))
        self.pellet_list.append(BigPellet(800, 108))
        self.pellet_list.append(BigPellet(50, 710))
        self.pellet_list.append(BigPellet(800, 710))

    def drawPellets(self, pacman):
        for pellet in self.pellet_list:
            if (
                pellet.x == 650
                and pellet.y == 168
                or pellet.x == 200
                and pellet.y == 168
            ):
                self.pellet_list.remove(pellet)

            if (
                pellet.x == 50
                and pellet.y == 108
                or pellet.x == 800
                and pellet.y == 108
            ):
                if pellet.radius == 5:
                    self.pellet_list.remove(pellet)

            pellet.draw(self.screen)
            self.pelletEaten(pacman, pellet)

    def reset(self):
        self.pellet_list = []
        self.node_x_done = []
        self.node_y_done = []
        self.x_list = [50, 475, 200, 287, 650, 745]
        self.y_list = [50, 165, 620, 710, 800]
        self.bigPelletList = [(50, 108), (800, 108), (50, 710), (800, 710)]
        self.addPelletToList()
        self.dyingSound = False


class BigPellet(Pellet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = 15


class Fruit(Pellet):
    def __init__(self, settings):
        super().__init__(427, 530)
        self.points = 500

        self.images = []
        self.settings = settings
        self.spritesheet = Spritesheet("./assets/images/pacman-spritesheet.png")
        self.setImages()
        self.index = random.randint(0, 5)
        self.spawn = False
        self.spawn_frame = 0
        self.eaten = False
        self.frame_eaten = 0
        self.font = pg.font.Font(f"./assets/fonts/PressStart2P-Regular.ttf", 15)

    def setImages(self):
        self.images = self.spritesheet.images_at(
            [
                (257, 129, 32, 32),
                (289, 129, 32, 32),
                (321, 129, 32, 32),
                (257, 161, 32, 32),
                (289, 161, 32, 32),
                (321, 161, 32, 32),
            ],
            colorkey=(255, 255, 255),
        )

    def turnOnFruit(self, framerate):
        if random.randint(0, 3000) == 0 and not self.spawn:
            self.spawn_frame = framerate
            self.spawn = True

        if self.spawn and self.spawn_frame + 2500 == framerate:
            self.spawn = False

    def fruitEaten(self, pacman, framerate):
        if (
            (self.x > pacman.x - pacman.radius and self.x < pacman.x + pacman.radius)
            and (
                self.y > pacman.y - pacman.radius and self.y < pacman.y + pacman.radius
            )
            and not self.eaten
        ):
            self.settings.score += self.points
            self.settings.prep_score()
            self.frame_eaten = framerate
            self.eaten = True

            self.settings.sounds.play_fruit()

    def draw(self, screen, framerate):
        self.turnOnFruit(framerate)
        self.fruitEaten(self.settings.pacman, framerate)

        if self.spawn:
            image = self.images[self.index]
            rect = image.get_rect()
            rect.left = self.x - 16
            rect.top = self.y - 16
            screen.blit(image, rect)

        if self.eaten:
            text = self.font.render(str(self.points), True, (255, 255, 255))
            text_rec = text.get_rect(center=(self.x, self.y))
            screen.blit(text, text_rec)
            self.spawn = False

            if self.frame_eaten + 500 == framerate:
                self.eaten = False

    def reset(self):
        self.spawn = False
        self.index = random.randint(0, 5)
        self.spawn_frame = 0
