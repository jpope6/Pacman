import pygame as pg
from timer import *


class Ghost:
    def __init__(self, screen, graph, settings):
        self.screen = screen
        self.graph = graph
        self.x = 0
        self.y = 0
        self.onNode = False
        self.node = None
        self.direction = "STOP"
        self.move_speed = 0.5
        self.images = {"LEFT": None, "RIGHT": None, "DOWN": None, "UP": None}
        self.spritesheet = Spritesheet("./assets/images/pacman-spritesheet.png")
        self.settings = settings
        self.spawn = False

    def update_node(self):
        for node in self.graph.nodes:
            if node.x == self.x and node.y == self.y and not self.onNode:
                self.node = node
                self.onNode = True
                break
            else:
                self.onNode = False

    def change_direction(self):
        if self.onNode:
            self.direction = self.target_direction

    def move(self):
        self.update_node()

        if self.direction == "UP" and self.node.neighbors["UP"] is not None:
            self.y += self.move_speed * -1
            self.target = self.node.neighbors["UP"]
        if self.direction == "DOWN" and self.node.neighbors["DOWN"] is not None:
            self.y += self.move_speed * 1
            self.target = self.node.neighbors["DOWN"]
        if self.direction == "LEFT" and self.node.neighbors["LEFT"] is not None:
            self.x += self.move_speed * -1
            self.target = self.node.neighbors["LEFT"]
        if self.direction == "RIGHT" and self.node.neighbors["RIGHT"] is not None:
            self.x += self.move_speed * 1
            self.target = self.node.neighbors["RIGHT"]


class Blinky(Ghost):
    def __init__(self, screen, graph, pacman):
        super().__init__(screen, graph, pacman)
        self.node = self.graph.nodes[len(self.graph.nodes) - 3]
        self.x = 335
        self.y = 435
        self.pacman = pacman
        self.goal = self.pacman.target

    def moveToPacman(self):
        pass

    def draw(self):
        pg.draw.rect(
            self.screen, (255, 0, 0), pg.Rect(self.x - 15, self.y - 15, 30, 30)
        )


class Pinky(Ghost):
    def __init__(self, screen, graph, settings):
        super().__init__(screen, graph, settings)
        self.node = self.graph.nodes[len(self.graph.nodes) - 3]
        self.x = 365
        self.y = 460
        self.setImages()
        self.image = self.images["LEFT"]

    def setImages(self):
        self.images["LEFT"] = self.spritesheet.image_at((33, 129, 32, 32))
        self.images["RIGHT"] = self.spritesheet.image_at((33, 161, 32, 32))
        self.images["DOWN"] = self.spritesheet.image_at((33, 97, 32, 32))
        self.images["UP"] = self.spritesheet.image_at((33, 65, 32, 32))

    def spawnToNode(self):
        if self.settings.score >= 100 and self.spawn == False:
            if self.y > 420:
                self.direction = "UP"
                self.y -= self.move_speed
            elif self.x < 375:
                self.direction = "RIGHT"
                self.x += self.move_speed
            elif self.x == 425 and self.y > 350:
                self.direction = "UP"
                self.y -= self.move_speed

                if self.x == self.node.x and self.y == self.node.y:
                    self.spawn = True

    def moveAround(self):
        self.spawnToNode()

        if (self.x, self.y) == (425, 350):
            self.direction = "LEFT"

        if (self.x, self.y) == (287.5, 350):
            self.direction = "DOWN"

        if (self.x, self.y) == (287.5, 435):
            self.direction = "LEFT"

        if (self.x, self.y) == (200, 435):
            self.direction = "DOWN"

        if (self.x, self.y) == (200, 620):
            self.direction = "LEFT"

        if (self.x, self.y) == (50, 620):
            self.direction = "DOWN"

        if (self.x, self.y) == (50, 710):
            self.direction = "RIGHT"

        if (self.x, self.y) == (105, 710):
            self.direction = "DOWN"

        if (self.x, self.y) == (105, 800):
            self.direction = "LEFT"

        if (self.x, self.y) == (50, 800):
            self.direction = "DOWN"

        if (self.x, self.y) == (50, 890):
            self.direction = "RIGHT"

        if (self.x, self.y) == (800, 890):
            self.direction = "UP"

        if (self.x, self.y) == (800, 800):
            self.direction = "LEFT"

        if (self.x, self.y) == (745, 800):
            self.direction = "UP"

        if (self.x, self.y) == (745, 710):
            self.direction = "RIGHT"

        if (self.x, self.y) == (800, 710):
            self.direction = "UP"

        if (self.x, self.y) == (800, 620):
            self.direction = "LEFT"

        if (self.x, self.y) == (650, 620):
            self.direction = "UP"

        if (self.x, self.y) == (650, 255):
            self.direction = "RIGHT"

        if (self.x, self.y) == (800, 255):
            self.direction = "UP"

        if (self.x, self.y) == (800, 50):
            self.direction = "LEFT"

        if (self.x, self.y) == (475, 50):
            self.direction = "DOWN"

        if (self.x, self.y) == (475, 165):
            self.direction = "LEFT"

        if (self.x, self.y) == (375, 165):
            self.direction = "UP"

        if (self.x, self.y) == (375, 50):
            self.direction = "LEFT"

        if (self.x, self.y) == (50, 50):
            self.direction = "DOWN"

        if (self.x, self.y) == (50, 255):
            self.direction = "RIGHT"

        if (self.x, self.y) == (200, 255):
            self.direction = "DOWN"

    def draw(self):
        if self.direction == "LEFT":
            self.image = self.images["LEFT"]
        if self.direction == "RIGHT":
            self.image = self.images["RIGHT"]
        if self.direction == "DOWN":
            self.image = self.images["DOWN"]
        if self.direction == "UP":
            self.image = self.images["UP"]

        rect = self.image.get_rect()
        rect.left = self.x - 16
        rect.top = self.y - 16
        self.screen.blit(self.image, rect)


class Inkey(Ghost):
    def __init__(self, screen, graph, settings):
        super().__init__(screen, graph, settings)
        self.node = self.graph.nodes[len(self.graph.nodes) - 3]
        self.x = 425
        self.y = 460
        self.setImages()
        self.image = self.images["UP"]

    def spawnToNode(self):
        if self.settings.score >= 50 and self.spawn == False:
            if self.y > self.node.y:
                self.direction = "UP"
                self.y -= self.move_speed

                if self.x == self.node.x and self.y == self.node.y:
                    self.spawn = True

    def setImages(self):
        self.images["LEFT"] = self.spritesheet.image_at((65, 129, 32, 32))
        self.images["RIGHT"] = self.spritesheet.image_at((65, 161, 32, 32))
        self.images["DOWN"] = self.spritesheet.image_at((65, 97, 32, 32))
        self.images["UP"] = self.spritesheet.image_at((65, 65, 32, 32))

    def draw(self):
        if self.direction == "LEFT":
            self.image = self.images["LEFT"]
        if self.direction == "RIGHT":
            self.image = self.images["RIGHT"]
        if self.direction == "DOWN":
            self.image = self.images["DOWN"]
        if self.direction == "UP":
            self.image = self.images["UP"]

        rect = self.image.get_rect()
        rect.left = self.x - 16
        rect.top = self.y - 16
        self.screen.blit(self.image, rect)

    def moveAround(self):
        self.spawnToNode()

        if (self.x, self.y) == (425, 350):
            self.direction = "RIGHT"

        if (self.x, self.y) == (567.5, 350):
            self.direction = "DOWN"

        if (self.x, self.y) == (567.5, 435):
            self.direction = "RIGHT"

        if (self.x, self.y) == (650, 435):
            self.direction = "DOWN"

        if (self.x, self.y) == (650, 620):
            self.direction = "RIGHT"

        if (self.x, self.y) == (800, 620):
            self.direction = "DOWN"

        if (self.x, self.y) == (800, 710):
            self.direction = "LEFT"

        if (self.x, self.y) == (745, 710):
            self.direction = "DOWN"

        if (self.x, self.y) == (745, 800):
            self.direction = "RIGHT"

        if (self.x, self.y) == (800, 800):
            self.direction = "DOWN"

        if (self.x, self.y) == (800, 890):
            self.direction = "LEFT"

        if (self.x, self.y) == (50, 890):
            self.direction = "UP"

        if (self.x, self.y) == (50, 800):
            self.direction = "RIGHT"

        if (self.x, self.y) == (105, 800):
            self.direction = "UP"

        if (self.x, self.y) == (105, 710):
            self.direction = "LEFT"

        if (self.x, self.y) == (50, 710):
            self.direction = "UP"

        if (self.x, self.y) == (50, 620):
            self.direction = "RIGHT"

        if (self.x, self.y) == (200, 620):
            self.direction = "UP"

        if (self.x, self.y) == (200, 255):
            self.direction = "LEFT"

        if (self.x, self.y) == (50, 255):
            self.direction = "UP"

        if (self.x, self.y) == (50, 50):
            self.direction = "RIGHT"

        if (self.x, self.y) == (375, 50):
            self.direction = "DOWN"

        if (self.x, self.y) == (375, 165):
            self.direction = "RIGHT"

        if (self.x, self.y) == (475, 165):
            self.direction = "UP"

        if (self.x, self.y) == (475, 50):
            self.direction = "RIGHT"

        if (self.x, self.y) == (800, 50):
            self.direction = "DOWN"

        if (self.x, self.y) == (800, 255):
            self.direction = "LEFT"

        if (self.x, self.y) == (650, 255):
            self.direction = "DOWN"
