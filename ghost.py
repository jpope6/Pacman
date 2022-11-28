import pygame as pg
from timer import *
import random


class Ghost:
    def __init__(self, screen, graph, settings, pacman):
        self.screen = screen
        self.graph = graph
        self.x = 0
        self.y = 0
        self.onNode = False
        self.node = None
        self.direction = "STOP"
        self.move_speed = 0.5
        self.spritesheet = Spritesheet("./assets/images/pacman-spritesheet.png")
        self.images = {"LEFT": None, "RIGHT": None, "DOWN": None, "UP": None}
        self.dying_images = self.spritesheet.images_at(
            [(161, 65, 30, 30), (161, 97, 30, 30)]
        )
        self.timer = Timer(self.dying_images)
        self.dead_images = {"LEFT": None, "RIGHT": None, "DOWN": None, "UP": None}
        self.setDeadImages()
        self.settings = settings
        self.pacman = pacman
        self.spawn = False
        self.dying = False
        self.dying_time = 0
        self.dead = False
        self.scores = [200, 400, 800, 1600]
        self.font = pg.font.Font(f"./assets/fonts/PressStart2P-Regular.ttf", 15)
        self.multiplied = False
        self.settings.index = 0
        self.score_checked = False
        self.score = "0"
        self.scoreFromDeath = 0

    def setDeadImages(self):
        self.dead_images["LEFT"] = self.spritesheet.image_at((129, 129, 32, 32))
        self.dead_images["RIGHT"] = self.spritesheet.image_at((129, 161, 32, 32))
        self.dead_images["DOWN"] = self.spritesheet.image_at((129, 97, 32, 32))
        self.dead_images["UP"] = self.spritesheet.image_at((129, 65, 32, 32))

    def dyingAndEaten(self):
        if (
            self.x > self.pacman.x - self.pacman.radius
            and self.x < self.pacman.x + self.pacman.radius
        ) and (
            self.y > self.pacman.y - self.pacman.radius
            and self.y < self.pacman.y + self.pacman.radius
        ):
            if self.dying and not self.dead:
                self.move_speed = 0
                self.dead = True
            if not self.dying:
                self.pacman.dead = True

    def dyingModeTimer(self, time):
        if self.dying_time + 2200 > time:
            self.image = self.dying_images[0]

            if self.dead:
                self.move_speed = 0
            else:
                self.move_speed = 0.25

        if self.dying_time + 2200 <= time and self.dying_time + 3000 > time:
            self.image = self.timer.image()

        if self.dying_time + 3000 == time:
            self.dying = False

            if self.dead:
                self.move_speed = 0
            else:
                self.move_speed = 0.5

            self.score = 200
            self.settings.pellets.dyingSound = False

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
        self.dyingAndEaten()

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

    def incrementScore(self):
        if self.dying and self.dead and not self.multiplied:
            self.settings.score += self.scores[self.settings.index]
            self.settings.index += 1
            self.multiplied = True
        if not self.dying:
            self.settings.index = 0
            self.multiplied = False
            self.score_checked = False

    def drawDead(self):
        if not self.score_checked:
            self.score = str(self.scores[self.settings.index])
            self.score_checked = True

        text = self.font.render(self.score, True, (255, 255, 255))
        text_rec = text.get_rect(center=(self.x, self.y))
        self.image = self.dead_images[self.direction]
        self.screen.blit(text, text_rec)
        self.incrementScore()


class Blinky(Ghost):
    def __init__(self, screen, graph, settings, pacman):
        super().__init__(screen, graph, settings, pacman)
        self.node = self.graph.nodes[len(self.graph.nodes) - 3]
        self.x = self.node.x
        self.y = self.node.y
        self.goal = self.pacman.target
        self.direction_change = True
        self.setImages()
        self.image = self.images["LEFT"]

    def checkOppositeDirection(self, direction):
        if not self.direction_change:
            return False
        if direction == "LEFT" and self.direction == "RIGHT":
            return False
        if direction == "RIGHT" and self.direction == "LEFT":
            return False
        if direction == "DOWN" and self.direction == "UP":
            return False
        if direction == "UP" and self.direction == "DOWN":
            return False

        return True

    def search(self, framerate):
        if not self.onNode:
            return

        directions = ["LEFT", "RIGHT", "UP", "DOWN"]
        number = random.randrange(0, 4)

        if self.node.neighbors[directions[number]]:
            if self.checkOppositeDirection(directions[number]):
                self.direction = directions[number]
                self.direction_change = False
                self.frame_change = framerate

                if directions[number] == "DOWN" or directions[number] == "UP":
                    self.x = self.node.neighbors[directions[number]].x
                elif directions[number] == "RIGHT" or directions[number] == "LEFT":
                    self.y = self.node.neighbors[directions[number]].y

                print(self.direction)
        else:
            self.search(framerate)

    def teleport_node(self):
        if self.x < 1 and self.direction == "LEFT":
            self.x = self.graph.node_right.x
            self.node = self.graph.node_right

        if self.x > 845 and self.direction == "RIGHT":
            self.x = self.graph.node_left.x
            self.node = self.graph.node_left

    def canChangeDirection(self, framerate):
        if self.direction_change == False:
            if self.frame_change + 10 == framerate:
                self.direction_change = True

    def setImages(self):
        self.images["LEFT"] = self.spritesheet.image_at((0, 129, 32, 32))
        self.images["RIGHT"] = self.spritesheet.image_at((0, 161, 32, 32))
        self.images["DOWN"] = self.spritesheet.image_at((0, 97, 32, 32))
        self.images["UP"] = self.spritesheet.image_at((0, 65, 32, 32))

    def draw(self, time):
        if self.dying and not self.dead:
            self.dyingModeTimer(time)
        elif self.direction == "LEFT":
            self.image = self.images["LEFT"]
        elif self.direction == "RIGHT":
            self.image = self.images["RIGHT"]
        elif self.direction == "DOWN":
            self.image = self.images["DOWN"]
        elif self.direction == "UP":
            self.image = self.images["UP"]

        rect = self.image.get_rect()
        rect.left = self.x - 16
        rect.top = self.y - 16
        self.screen.blit(self.image, rect)

    def reset(self):
        self.node = self.graph.nodes[len(self.graph.nodes) - 3]
        self.x = self.node.x
        self.y = self.node.y
        self.goal = self.pacman.target
        self.direction_change = True
        self.direction = "STOP"


class Pinky(Ghost):
    def __init__(self, screen, graph, settings, pacman):
        super().__init__(screen, graph, settings, pacman)
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
        if self.pacman.score_from_death >= 100 and self.spawn == False:
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

    def reset(self):
        self.node = self.graph.nodes[len(self.graph.nodes) - 3]
        self.x = 365
        self.y = 460
        self.image = self.images["LEFT"]
        self.spawn = False
        self.direction = "STOP"

    def moveAround(self):
        self.spawnToNode()

        if (self.x, self.y) == (425, 350):
            self.direction = "LEFT"

        if (self.x, self.y) == (287, 350):
            self.direction = "DOWN"

        if (self.x, self.y) == (287, 435):
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

    def draw(self, time):
        if self.dying and not self.dead:
            self.dyingModeTimer(time)
        elif self.direction == "LEFT":
            self.image = self.images["LEFT"]
        elif self.direction == "RIGHT":
            self.image = self.images["RIGHT"]
        elif self.direction == "DOWN":
            self.image = self.images["DOWN"]
        elif self.direction == "UP":
            self.image = self.images["UP"]

        rect = self.image.get_rect()
        rect.left = self.x - 16
        rect.top = self.y - 16
        self.screen.blit(self.image, rect)


class Inkey(Ghost):
    def __init__(self, screen, graph, settings, pacman):
        super().__init__(screen, graph, settings, pacman)
        self.node = self.graph.nodes[len(self.graph.nodes) - 3]
        self.x = 425
        self.y = 460
        self.setImages()
        self.image = self.images["UP"]

    def spawnToNode(self):
        if self.pacman.score_from_death >= 50 and self.spawn == False:
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

    def draw(self, time):
        if self.dying:
            self.dyingModeTimer(time)
        elif self.direction == "LEFT":
            self.image = self.images["LEFT"]
        elif self.direction == "RIGHT":
            self.image = self.images["RIGHT"]
        elif self.direction == "DOWN":
            self.image = self.images["DOWN"]
        elif self.direction == "UP":
            self.image = self.images["UP"]

        rect = self.image.get_rect()
        rect.left = self.x - 16
        rect.top = self.y - 16
        self.screen.blit(self.image, rect)

    def reset(self):
        self.node = self.graph.nodes[len(self.graph.nodes) - 3]
        self.x = 425
        self.y = 460
        self.image = self.images["UP"]
        self.spawn = False
        self.direction = "STOP"

    def moveAround(self):
        self.spawnToNode()

        if (self.x, self.y) == (425, 350):
            self.direction = "RIGHT"

        if (self.x, self.y) == (567, 350):
            self.direction = "DOWN"

        if (self.x, self.y) == (567, 435):
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


class Clyde(Inkey):
    def __init__(self, screen, graph, settings, pacman):
        super().__init__(screen, graph, settings, pacman)
        self.x = 485
        self.image = self.images["RIGHT"]

    def setImages(self):
        self.images["LEFT"] = self.spritesheet.image_at((97, 129, 32, 32))
        self.images["RIGHT"] = self.spritesheet.image_at((97, 161, 32, 32))
        self.images["DOWN"] = self.spritesheet.image_at((97, 97, 32, 32))
        self.images["UP"] = self.spritesheet.image_at((97, 65, 32, 32))

    def spawnToNode(self):
        if self.pacman.score_from_death >= 10 and self.spawn == False:
            if self.y > 420:
                self.direction = "UP"
                self.y -= self.move_speed
            elif self.x > 425:
                self.direction = "LEFT"
                self.x -= self.move_speed
            elif self.x == 425 and self.y > 350:
                self.direction = "UP"
                self.y -= self.move_speed

                if self.x == self.node.x and self.y == self.node.y:
                    self.spawn = True

    def reset(self):
        self.node = self.graph.nodes[len(self.graph.nodes) - 3]
        self.x = 485
        self.y = 460
        self.image = self.images["RIGHT"]
        self.spawn = False
        self.direction = "STOP"
