import pygame as pg
from timer import *


class Pacman:
    def __init__(self, screen, graph, settings):
        self.node = None
        self.screen = screen
        self.graph = graph
        self.settings = settings
        self.node = self.graph.nodes[len(self.graph.nodes) - 4]
        self.target = self.node.neighbors["LEFT"]
        self.x = self.node.x
        self.y = self.node.y
        self.move_speed = 0.5
        self.direction = "LEFT"
        self.target_direction = "LEFT"
        self.onNode = True
        self.radius = 20
        self.spritesheet = Spritesheet("./assets/images/pacman-spritesheet.png")
        self.images = {"LEFT": None, "RIGHT": None, "DOWN": None, "UP": None}
        self.setImages()
        self.deadImages = []
        self.setDeadImages()
        self.dead_timer = Timer(self.deadImages, is_loop=False)
        self.image = self.left_timer.image()
        self.dead = False
        self.lives = 3
        self.lives_x = 780
        self.score_from_death = 0
        self.index = 0

    def setDeadImages(self):
        self.deadImages = self.spritesheet.images_at(
            [
                (0, 193, 32, 32),
                (33, 193, 32, 32),
                (65, 193, 32, 32),
                (97, 193, 32, 32),
                (129, 193, 32, 32),
                (161, 193, 32, 32),
                (193, 193, 32, 32),
                (225, 193, 32, 32),
                (257, 193, 32, 32),
                (289, 193, 32, 32),
                (321, 193, 32, 32),
            ]
        )

    def setImages(self):
        self.images["LEFT"] = self.spritesheet.images_at(
            [(0, 0, 32, 32), (0, 33, 32, 32)], colorkey=(255, 255, 255)
        )
        self.images["RIGHT"] = self.spritesheet.images_at(
            [(33, 0, 32, 32), (33, 33, 32, 32)], colorkey=(255, 255, 255)
        )
        self.images["DOWN"] = self.spritesheet.images_at(
            [(65, 0, 32, 32), (65, 33, 32, 32)], colorkey=(255, 255, 255)
        )
        self.images["UP"] = self.spritesheet.images_at(
            [(97, 0, 32, 32), (97, 33, 32, 32)], colorkey=(255, 255, 255)
        )

        self.left_timer = Timer(self.images["LEFT"])
        self.right_timer = Timer(self.images["RIGHT"])
        self.down_timer = Timer(self.images["DOWN"])
        self.up_timer = Timer(self.images["UP"])

    def move(self):
        self.change_direction()
        self.update_node()
        self.teleport_node()

        if self.direction == "UP" and self.node.neighbors["UP"] is not None:
            self.y += self.move_speed * -1
            self.x = self.node.x
            self.target = self.node.neighbors["UP"]
        if self.direction == "DOWN" and self.node.neighbors["DOWN"] is not None:
            self.y += self.move_speed * 1
            self.x = self.node.x
            self.target = self.node.neighbors["DOWN"]
        if self.direction == "LEFT" and self.node.neighbors["LEFT"] is not None:
            self.x += self.move_speed * -1
            self.y = self.node.y
            self.target = self.node.neighbors["LEFT"]
        if self.direction == "RIGHT" and self.node.neighbors["RIGHT"] is not None:
            self.x += self.move_speed * 1
            self.y = self.node.y
            self.target = self.node.neighbors["RIGHT"]

        # print(self.x, ", ", self.y)

    def update_node(self):
        for node in self.graph.nodes:
            if node.circle.collidepoint(self.x, self.y):
                self.node = node
                self.onNode = True
                break
            else:
                self.onNode = False

    def change_direction(self):
        if self.onNode:
            self.direction = self.target_direction

        # allows you to turn around
        if self.target and self.target.neighbors[self.target_direction] == self.node:
            self.direction = self.target_direction
            temp = self.node
            self.node = self.target
            self.target = temp

    def teleport_node(self):
        if self.x < 1 and self.direction == "LEFT":
            self.x = self.graph.node_right.x
            self.node = self.graph.node_right

        if self.x > 845 and self.direction == "RIGHT":
            self.x = self.graph.node_left.x
            self.node = self.graph.node_left

    def draw(self):
        if self.dead:
            self.image = self.dead_timer.image()
            self.direction = "STOP"
            if self.dead_timer.is_expired():
                self.dead_timer.index = 0
                self.reset()
        elif self.direction == "LEFT":
            self.image = self.left_timer.image()
        elif self.direction == "RIGHT":
            self.image = self.right_timer.image()
        elif self.direction == "DOWN":
            self.image = self.down_timer.image()
        elif self.direction == "UP":
            self.image = self.up_timer.image()

        rect = self.image.get_rect()
        rect.left = self.x - 16
        rect.top = self.y - 16
        self.screen.blit(self.image, rect)

        # pg.draw.circle(self.screen, (255, 255, 0), (self.x, self.y), self.radius)

    def drawLives(self, framerate):
        if self.lives == 0:
            self.settings.game.game_over = True
            self.settings.game.playable = False

            if self.settings.game.game_over_frame == 0:
                self.settings.game.game_over_frame = framerate

            if self.settings.game.game_over_frame + 800 == framerate:
                self.settings.game.cur_menu = "menu"
                self.settings.game.fullReset()

        if self.lives > 0:
            image = self.images["LEFT"][0]
            rect = image.get_rect()
            rect.left = self.lives_x
            rect.top = 947
            self.screen.blit(image, rect)

        if self.lives > 1:
            image2 = self.images["LEFT"][0]
            rect2 = image2.get_rect()
            rect2.left = self.lives_x - 32
            rect2.top = 947
            self.screen.blit(image2, rect2)

        if self.lives > 2:
            image3 = self.images["LEFT"][0]
            rect3 = image3.get_rect()
            rect3.left = self.lives_x - 64
            rect3.top = 947
            self.screen.blit(image3, rect3)

    def reset(self):
        if self.lives > 0:
            self.lives -= 1
            self.node = self.graph.nodes[len(self.graph.nodes) - 4]
            self.target = None
            self.x = self.node.x
            self.y = self.node.y
            self.direction = "STOP"
            self.target_direction = "STOP"
            self.onNode = True
            self.image = self.left_timer.image()
            self.dead = False
            self.score_from_death = 0

            for ghost in self.settings.ghosts:
                ghost.reset()

        if self.lives == 0:
            self.node = self.graph.nodes[len(self.graph.nodes) - 4]
            self.target = None
            self.x = self.node.x
            self.y = self.node.y
            self.direction = "STOP"
            self.target_direction = "STOP"
            self.onNode = True
            self.image = self.left_timer.image()
            self.dead = False
            self.score_from_death = 0
