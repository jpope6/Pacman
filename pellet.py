import pygame as pg
from settings import *


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
